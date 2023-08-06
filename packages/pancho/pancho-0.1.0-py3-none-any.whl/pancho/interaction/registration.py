from ..definitions import contracts
from ..interaction.messages import Event, dump_payload


class EventRegistrator:
    def __init__(self, storage: contracts.EventStorageContract):
        self._storage = storage

    async def register(self, stream: contracts.MessageStream):
        data = []
        filtered = stream.filter(lambda m: isinstance(m, Event))
        for event in filtered:
            data.append(dict(
                id=event.id,
                created_at=event.created_at,
                event_type=type(event).__name__,
                actor_id=event.actor_id,
                context=dump_payload(event)
            ))
        if data:
            await self._storage.insert_many(data)
