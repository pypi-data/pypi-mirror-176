from ..definitions import contracts
from .actor import Actor


class ActorRepository(contracts.ActorRepository):
    async def get(
        self,
        identifier: contracts.IdentifierType
    ) -> Actor: ...

    async def save(
        self,
        identifier: contracts.IdentifierType,
        data: contracts.ActorState
    ) -> bool: ...
