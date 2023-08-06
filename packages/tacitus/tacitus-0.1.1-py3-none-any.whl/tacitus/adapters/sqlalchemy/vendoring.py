import functools
import typing

import sqlalchemy.ext.asyncio
import sqlalchemy.sql

from .obtaining import SqlAlchemyQueryResolver, QueryResultProxy
from .saving import SqlAlchemyMutationResolver
from .registration import Registry
from ...definitions import contracts


class SqlAlchemyVendor(contracts.Vendor):
    def __init__(
        self,
        registry: Registry,
        connection: sqlalchemy.ext.asyncio.AsyncConnection
    ):
        self._registry = registry
        self._connection = connection

    @functools.cached_property
    def _query_resolver(self):
        return SqlAlchemyQueryResolver(
            registry=self._registry,
            connection=self._connection
        )

    @functools.cached_property
    def _mutation_resolver(self):
        return SqlAlchemyMutationResolver(
            registry=self._registry,
            connection=self._connection
        )

    async def get(self, query: contracts.Query | None = None) -> QueryResultProxy | None:
        if query is None:
            return

        data = await self._query_resolver.resolve_query(query)
        total = None

        if query.with_total:
            data, total = data

        return QueryResultProxy(
            data=data,
            total=total
        )

    async def save(self, data: contracts.MutationData) -> typing.NoReturn:
        if data:
            await self._mutation_resolver.resolve(data)


