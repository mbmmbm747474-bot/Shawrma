"""Database-portable column types.

GUID behaves like postgresql.UUID(as_uuid=True) on a real Postgres
connection, but degrades to a plain CHAR(36) string on SQLite (used by the
desktop/demo build, which has no Postgres server to install). PortableJSON
does the same for JSONB -> JSON.

Every model imports these instead of importing UUID/JSONB directly from
sqlalchemy.dialects.postgresql, so the exact same model files work against
either database engine. Which engine you get is determined entirely by
DATABASE_URL (see app/core/config.py and app/core/database.py) - nothing
else needs to change.
"""
from __future__ import annotations

import uuid

from sqlalchemy import CHAR, JSON
from sqlalchemy.dialects.postgresql import JSONB as PG_JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.types import TypeDecorator


class GUID(TypeDecorator):
    """Platform-independent UUID column.

    Stores as Postgres's native UUID type when the dialect is postgresql,
    otherwise as a CHAR(36) string (e.g. on SQLite). Always returns a
    Python uuid.UUID on read, accepts uuid.UUID or a UUID-formatted string
    on write - matches the behavior of UUID(as_uuid=True) that the rest of
    the codebase already expects.
    """

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if dialect.name == "postgresql":
            return str(value)
        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(str(value))
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(str(value))


class PortableJSON(TypeDecorator):
    """JSONB on Postgres, plain JSON (text-serialized) on SQLite/others."""

    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_JSONB())
        return dialect.type_descriptor(JSON())
