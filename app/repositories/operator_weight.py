from typing import Protocol
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import OperatorWeight


class IOperatorWeightRepository(Protocol):
    async def get_by_source(self, source_id: UUID) -> list[OperatorWeight]:
        pass

    async def get_by_operator_and_source(self, operator_id: UUID, source_id: UUID) -> OperatorWeight | None:
        pass

    async def save(self, weight: OperatorWeight) -> None:
        pass

    async def delete(self, weight: OperatorWeight) -> None:
        pass


class OperatorWeightRepository(IOperatorWeightRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_source(self, source_id: UUID) -> list[OperatorWeight]:
        stmt = select(OperatorWeight).filter_by(source_id=source_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_operator_and_source(self, operator_id: UUID, source_id: UUID) -> OperatorWeight | None:
        stmt = select(OperatorWeight).filter_by(operator_id=operator_id, source_id=source_id)
        return (await self.session.execute(stmt)).scalar()

    async def save(self, weight: OperatorWeight) -> None:
        self.session.add(weight)

    async def delete(self, weight: OperatorWeight) -> None:
        await self.session.delete(weight)
