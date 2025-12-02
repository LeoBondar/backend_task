from uuid import UUID as PyUUID

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text, TypeDecorator
from sqlalchemy.dialects.sqlite import CHAR

from app.domain.models import Lead, Operator, OperatorWeight, Request, Source
from app.persistent.db_schemas.base import mapper_registry


class UUIDString(TypeDecorator):
    impl = CHAR(36)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return PyUUID(value)
        return value


operator_table = Table(
    "operators",
    mapper_registry.metadata,
    Column("id", UUIDString(), primary_key=True),
    Column("name", String(255), nullable=False),
    Column("is_active", Boolean, nullable=False, default=True),
    Column("max_leads", Integer, nullable=False, default=10),
    Column("created_at", DateTime, nullable=False),
)

lead_table = Table(
    "leads",
    mapper_registry.metadata,
    Column("id", UUIDString(), primary_key=True),
    Column("external_id", String(255), nullable=False, unique=True),
    Column("phone", String(50), nullable=True),
    Column("email", String(255), nullable=True),
    Column("name", String(255), nullable=True),
    Column("created_at", DateTime, nullable=False),
)

source_table = Table(
    "sources",
    mapper_registry.metadata,
    Column("id", UUIDString(), primary_key=True),
    Column("name", String(255), nullable=False),
    Column("code", String(100), nullable=False, unique=True),
    Column("created_at", DateTime, nullable=False),
)

operator_weight_table = Table(
    "operator_weights",
    mapper_registry.metadata,
    Column("id", UUIDString(), primary_key=True),
    Column("operator_id", UUIDString(), ForeignKey("operators.id"), nullable=False),
    Column("source_id", UUIDString(), ForeignKey("sources.id"), nullable=False),
    Column("weight", Integer, nullable=False),
)

request_table = Table(
    "requests",
    mapper_registry.metadata,
    Column("id", UUIDString(), primary_key=True),
    Column("lead_id", UUIDString(), ForeignKey("leads.id"), nullable=False),
    Column("source_id", UUIDString(), ForeignKey("sources.id"), nullable=False),
    Column("operator_id", UUIDString(), ForeignKey("operators.id"), nullable=True),
    Column("message", Text, nullable=True),
    Column("is_active", Boolean, nullable=False, default=True),
    Column("created_at", DateTime, nullable=False),
)


def init_mappers() -> None:
    mapper_registry.map_imperatively(Operator, operator_table)
    mapper_registry.map_imperatively(Lead, lead_table)
    mapper_registry.map_imperatively(Source, source_table)
    mapper_registry.map_imperatively(OperatorWeight, operator_weight_table)
    mapper_registry.map_imperatively(Request, request_table)
