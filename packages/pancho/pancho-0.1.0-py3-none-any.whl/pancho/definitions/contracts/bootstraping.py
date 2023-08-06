import typing
from ext.zorge import contracts as zorge_contracts


class DependencyRegistry:
    def register_uow(
        self,
        instance: zorge_contracts.DependencyBindingInstance,
        contract: zorge_contracts.DependencyBindingContract
    ) -> typing.NoReturn: ...

    def register_connection_context(
        self,
        open_callback: typing.Callable,
        close_callback: typing.Callable,
        contract: zorge_contracts.DependencyBindingContract
    ) -> typing.NoReturn: ...

    def register_storage_bucket(
        self,
        instance: zorge_contracts.DependencyBindingInstance,
        contract: zorge_contracts.DependencyBindingContract
    ) -> typing.NoReturn: ...

    def register_storage(
        self,
        instance: zorge_contracts.DependencyBindingInstance,
        contract: zorge_contracts.DependencyBindingContract
    ) -> typing.NoReturn: ...

    def register_repository(
        self,
        instance: zorge_contracts.DependencyBindingInstance,
        scope: typing.Literal['instance', 'global'] = 'instance'
    ) -> typing.NoReturn: ...

    def get_container(
        self
    ) -> zorge_contracts.DependencyContainer:
        ...
