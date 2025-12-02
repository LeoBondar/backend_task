from typing import Protocol
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Operator, Request
from app.repositories.exception import RepositoryNotFoundException


class IOperatorRepository(Protocol):
    async def get(self, operator_id: UUID) -> Operator:
        pass

    async def get_all(self, only_active: bool = False) -> list[Operator]:
        pass

    async def save(self, operator: Operator) -> None:
        pass

    async def get_active_requests_count(self, operator_id: UUID) -> int:
        pass


class OperatorRepository(IOperatorRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, operator_id: UUID) -> Operator:
        stmt = select(Operator).filter_by(id=operator_id)
        operator = (await self.session.execute(stmt)).scalar()
        if not operator:
            raise RepositoryNotFoundException
        return operator

    async def get_all(self, only_active: bool = False) -> list[Operator]:
        stmt = select(Operator)
        if only_active:
            stmt = stmt.filter_by(is_active=True)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def save(self, operator: Operator) -> None:
        self.session.add(operator)

    async def get_active_requests_count(self, operator_id: UUID) -> int:
        stmt = select(func.count(Request.id)).filter_by(operator_id=operator_id, is_active=True)
        result = await self.session.execute(stmt)
        return result.scalar() or 0
