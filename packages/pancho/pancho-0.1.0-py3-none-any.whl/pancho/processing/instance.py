import typing

from ext.zorge.contracts import DependencyContainer
from ..definitions import contracts
from ..interaction.messages import UnexpectedError
from .generic import MessageStream, MessageCollector, ProcessorSettings


class Processor(contracts.Processor):
    def __init__(
        self,
        dependency_container: DependencyContainer,
        message_actor_map: contracts.MessageActorMap,
        actor_repository_map: contracts.ActorRepositoryMap,
        settings: ProcessorSettings
    ):
        self._dependency_container = dependency_container
        self._message_actor_map = message_actor_map
        self._actor_repository_map = actor_repository_map
        self._settings = settings
        self._message_collector = MessageCollector()
        self._uow_instance = None
        self._dependency_provider = None
        self._interaction_factory: contracts.InteractionFactory | None = None
        self._identity_map = {}

    async def __aenter__(self) -> 'Processor':
        self._dependency_provider = self._dependency_container.get_provider()

        self._interaction_factory = typing.cast(
            contracts.InteractionFactory,
            await self._dependency_provider.resolve(contracts.InteractionFactory)
        )

        if self._settings.uow:
            self._uow_instance = await self._dependency_provider.resolve(self._settings.uow)
            await self._uow_instance.begin()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._settings.register_events:
            await self._register_events()

        if self._settings.auto_commit and not exc_type:
            await self.commit()

        if self._settings.uow:
            await getattr(
                self._uow_instance,
                'rollback' if exc_type or self._message_collector.get_stream().has_exception_event() else 'commit'
            )()

        await self._dependency_provider.shutdown()

    def get_message_stream(self) -> MessageStream:
        return self._message_collector.get_stream()

    async def receive(self, *messages: contracts.Message):
        self._message_collector.extend(messages)
        while message := self._message_collector.pop():
            for actor_contract in self._message_actor_map.get(type(message), ()):
                try:
                    actor = await self._get_actor(actor_contract, message.actor_id)
                    events = actor.__receive__(
                        message=message,
                        context=await self._get_context(actor, message)
                    )
                    self._message_collector.extend(events)
                except Exception as e:
                    self._message_collector.extend(
                        self._interaction_factory.get_event_producer(
                            actor_id=message.actor_id,
                            context=dict(
                                message=str(e)
                            )
                        ).bind(
                            event_contract=typing.cast(contracts.Event, UnexpectedError),
                        ).get()
                    )
                    if self._settings.uow:
                        raise e

    async def commit(self):
        for actor, repository in self._identity_map.values():
            try:
                await repository.save(
                    identifier=actor.__identifier__(),
                    data=actor.__state__()
                )
            except Exception as e:
                self._message_collector.extend(
                    self._interaction_factory.get_event_producer(
                        actor_id=actor.__identifier__(),
                        context=dict(
                            message=str(e)
                        )
                    ).bind(
                        event_contract=typing.cast(contracts.Event, UnexpectedError)
                    ).get()
                )
                if self._settings.uow:
                    raise e

    async def _register_events(self):
        registrator = await self._dependency_provider.resolve(contracts.EventRegistrator)
        if registrator:
            await registrator.register(self._message_collector.get_stream())

    async def shutdown(self):
        await self._dependency_provider.shutdown()

    async def _get_context(
        self,
        actor: contracts.Actor,
        message: contracts.Message
    ) -> contracts.MessageContext:
        context_contract = actor.__message_context_map__.get(type(message))
        if context_contract:
            context = await self._dependency_provider.resolve(context_contract)
            return await context(message)

    async def _get_actor(
        self,
        actor_contract: type[contracts.Actor],
        actor_id: contracts.IdentifierType | None
    ) -> contracts.Actor:
        if actor_id not in self._identity_map:
            repository = await self._dependency_provider.resolve(
                self._actor_repository_map.get(actor_contract)
            )
            actor = await repository.get(actor_id)

            if not actor_id:
                return actor
            self._identity_map[actor_id] = (actor, repository)

        return self._identity_map[actor_id][0]
