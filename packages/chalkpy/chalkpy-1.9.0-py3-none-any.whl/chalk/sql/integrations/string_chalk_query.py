import typing
from typing import Mapping, Optional, Sequence, Union

import sqlalchemy
from polars import from_arrow
from sqlalchemy import text
from sqlalchemy.sql import selectable

from chalk.features import DataFrame, Feature
from chalk.sql import BaseSQLSourceProtocol, IncrementalSettings
from chalk.sql.base.protocols import DBSessionProtocol, StringChalkQueryProtocol
from chalk.sql.integrations.chalk_query import (
    Finalizer,
    _construct_features_df,
    _construct_features_single,
    _resolve_implicit_mappings,
)
from chalk.utils.duration import Duration


class StringChalkQuery(StringChalkQueryProtocol):
    def __init__(
        self,
        session: DBSessionProtocol,
        source: BaseSQLSourceProtocol,
        query: Union[str, selectable.Selectable],
        fields: Mapping[str, Union[Feature, str]],
        args: Optional[Mapping[str, str]],
    ):
        self._finalizer: Optional[Finalizer] = None
        self._session = session
        self._source = source
        self._original_query = query
        self._query = text(query) if isinstance(query, str) else query
        self._fields = fields
        self._args = args
        self._incremental_settings: Optional[Union[IncrementalSettings, bool]] = None
        if args is not None:
            self._query = self._query.bindparams(**args)

    def one_or_none(self):
        self._finalizer = Finalizer.OneOrNone
        return self

    def one(self):
        self._finalizer = Finalizer.One
        return self

    def all(self):
        self._finalizer = Finalizer.All
        return self

    def incremental(self, *, incremental_column: str, lookback_period: Duration = "0s"):
        self._finalizer = Finalizer.All
        self._incremental_settings = IncrementalSettings(
            lookback_period=lookback_period, incremental_column=incremental_column
        )
        return self

    def execute(self):
        return self.execute_internal(expected_features=[])

    def execute_internal(self, *, expected_features: Sequence[Feature]):
        from chalk.sql import SnowflakeSourceImpl

        if isinstance(self._source, SnowflakeSourceImpl) and (
            self._finalizer is None or self._finalizer == Finalizer.All
        ):
            return self._execute_internal_snowflake()
        else:
            return self._execute_internal_sql(expected_features=expected_features)

    def _execute_internal_snowflake(self):
        # this import is safe because the only way we end up here is if we have a valid SnowflakeSource constructed,
        # which already gates this import
        import snowflake.connector

        from chalk.sql import SnowflakeSourceImpl

        source = typing.cast(SnowflakeSourceImpl, self._source)
        with snowflake.connector.connect(
            user=source.user,
            account=source.account_identifier,
            password=source.password,
            warehouse=source.warehouse,
            schema=source.schema,
            database=source.db,
        ) as con:
            return DataFrame(
                from_arrow(con.cursor().execute(self._original_query).fetch_arrow_all()).rename(
                    {k.upper(): v.root_fqn for k, v in self._fields.items()}
                )
            )

    def _execute_internal_sql(self, expected_features: Sequence[Feature]):
        cursor = self._session.execute(self._query)
        assert isinstance(cursor, sqlalchemy.engine.CursorResult)
        fields_normalized = {
            k: Feature.from_root_fqn(v) if isinstance(v, str) else v for (k, v) in self._fields.items()
        }
        self._finalizer = self._finalizer or Finalizer.All

        if self._finalizer == Finalizer.All:
            rows = cursor.all()
            column_mapping = _resolve_implicit_mappings(
                explicit_mappings=self._fields_normalized(),
                expected_features=expected_features,
                tuple_column_names=list(cursor.keys()),
            )

            return _construct_features_df(column_mapping, rows)

        row = None
        if self._finalizer == Finalizer.One:
            row = cursor.one()

        if self._finalizer == Finalizer.First:
            row = cursor.first()

        if self._finalizer == Finalizer.OneOrNone:
            row = cursor.one_or_none()

        column_mapping = _resolve_implicit_mappings(
            explicit_mappings=self._fields_normalized(),
            expected_features=expected_features,
            tuple_column_names=list(cursor.keys()),
        )

        # We only want to run feature_codecs for StringQuerys, not ChalkQuerys, as SqlAlchemy ORM mappings won't run in this case
        return _construct_features_single(column_mapping, row, _coerce_raw_values=True)

    def _fields_normalized(self):
        return {k: Feature.from_root_fqn(v) if isinstance(v, str) else v for (k, v) in self._fields.items()}
