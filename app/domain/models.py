from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass
class Operator:
    id: UUID
    name: str
    is_active: bool
    max_leads: int
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    @classmethod
    def create(cls, name: str, max_leads: int = 10, is_active: bool = True) -> "Operator":
        return cls(
            id=uuid4(),
            name=name,
            is_active=is_active,
            max_leads=max_leads,
        )


@dataclass
class Lead:
    id: UUID
    external_id: str
    phone: str | None
    email: str | None
    name: str | None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    @classmethod
    def create(
        cls, external_id: str, phone: str | None = None, email: str | None = None, name: str | None = None
    ) -> "Lead":
        return cls(
            id=uuid4(),
            external_id=external_id,
            phone=phone,
            email=email,
            name=name,
        )


@dataclass
class Source:
    id: UUID
    name: str
    code: str
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    @classmethod
    def create(cls, name: str, code: str) -> "Source":
        return cls(
            id=uuid4(),
            name=name,
            code=code,
        )


@dataclass
class OperatorWeight:
    id: UUID
    operator_id: UUID
    source_id: UUID
    weight: int

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    @classmethod
    def create(cls, operator_id: UUID, source_id: UUID, weight: int) -> "OperatorWeight":
        return cls(
            id=uuid4(),
            operator_id=operator_id,
            source_id=source_id,
            weight=weight,
        )


@dataclass
class Request:
    id: UUID
    lead_id: UUID
    source_id: UUID
    operator_id: UUID | None
    message: str | None
    is_active: bool
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    @classmethod
    def create(
        cls, lead_id: UUID, source_id: UUID, operator_id: UUID | None = None, message: str | None = None
    ) -> "Request":
        return cls(
            id=uuid4(),
            lead_id=lead_id,
            source_id=source_id,
            operator_id=operator_id,
            message=message,
            is_active=True,
        )

    def close(self) -> None:
        self.is_active = False

    def assign_operator(self, operator_id: UUID) -> None:
        self.operator_id = operator_id
