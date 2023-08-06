import collections.abc
import typing


class Storage(typing.Protocol):
    async def insert_many(self, data: collections.abc.Iterable[collections.abc.Mapping]): ...
