import collections.abc
import typing

from ext.zorge.di.container import DependencyContainer
from ext.zorge import contracts as zorge_contracts
from ..definitions import contracts
from ..identity.factory import UUIDIdentifierFactory
from ..interaction.factory import InteractionFactory
from ..interaction.registration import EventRegistrator


class DependencyRegistry:
    def __init__(
        self,
        dc: zorge_contracts.DependencyContainer | None = None,
        identifier_factory: contracts.IdentifierFactory = UUIDIdentifierFactory,
        interaction_factory: contracts.InteractionFactory = InteractionFactory,
    ):
        self._dc = dc or DependencyContainer()
        self._dc.register_contractual_dependency(
            instance=identifier_factory,
            contract=contracts.IdentifierFactory
        )
        self._dc.register_contractual_dependency(
            instance=interaction_factory,
            contract=contracts.InteractionFactory
        )

    def register_event_registrator(
        self,
        storage_bucket: zorge_contracts.DependencyBindingContract,
        instance: zorge_contracts.DependencyBindingInstance = EventRegistrator
    ):
        self._dc.register_contractual_dependency(
            instance=instance,
            contract=contracts.EventRegistrator
        )
        self.register_storage_bucket(
            instance=storage_bucket,
            contract=contracts.EventStorageContract
        )

    def register_uow(
        self,
        instance: zorge_contracts.DependencyBindingInstance,
        contract: zorge_contracts.DependencyBindingContract
    ):
        self._dc.register_contractual_dependency(
            instance=instance,
            contract=contract
        )

    def register_connection_context(
        self,
        open_callback: typing.Callable,
        close_callback: typing.Callable,
        contract: zorge_contracts.DependencyBindingContract
    ):
        self._dc.register_instance_singleton(
            instance=open_callback,
            contract=contract,
        )
        self._dc.register_shutdown_callback(
            callback=close_callback,
            contract=contract,
        )

    def register_storage_bucket(
        self,
        instance: zorge_contracts.DependencyBindingInstance,
        contract: zorge_contracts.DependencyBindingContract
    ):
        self._dc.register_contractual_dependency(
            instance=instance,
            contract=contract
        )

    def register_storage(
        self,
        instance: zorge_contracts.DependencyBindingInstance,
        contract: zorge_contracts.DependencyBindingContract
    ):
        self._dc.register_contractual_dependency(
            instance=instance,
            contract=contract
        )

    def register_message_context(
        self,
        instance: zorge_contracts.DependencyBindingInstance,
        contract: zorge_contracts.DependencyBindingContract
    ):
        self._dc.register_contractual_dependency(
            instance=instance,
            contract=contract
        )

    def register_repository(
        self,
        instance: zorge_contracts.DependencyBindingInstance,
        scope: typing.Literal['instance', 'global'] = 'instance'
    ):
        _map = {
            'instance': zorge_contracts.DependencyBindingScope.INSTANCE,
            'global': zorge_contracts.DependencyBindingScope.GLOBAL
        }
        self._dc.register_selfish_dependency(
            instance=instance,
            singleton_scope=_map[scope]
        )

    def get_container(self) -> DependencyContainer:
        return self._dc
