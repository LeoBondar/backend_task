from typing import Protocol
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Request
from app.repositories.exception import RepositoryNotFoundException


class IRequestRepository(Protocol):
    async def get(self, request_id: UUID) -> Request:
        pass

    async def get_by_lead(self, lead_id: UUID) -> list[Request]:
        pass

    async def get_by_operator(self, operator_id: UUID, only_active: bool = False) -> list[Request]:
        pass

    async def get_all(self) -> list[Request]:
        pass

    async def save(self, request: Request) -> None:
        pass


class RequestRepository(IRequestRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, request_id: UUID) -> Request:
        stmt = select(Request).filter_by(id=request_id)
        request = (await self.session.execute(stmt)).scalar()
        if not request:
            raise RepositoryNotFoundException
        return request

    async def get_by_lead(self, lead_id: UUID) -> list[Request]:
        stmt = select(Request).filter_by(lead_id=lead_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_operator(self, operator_id: UUID, only_active: bool = False) -> list[Request]:
        stmt = select(Request).filter_by(operator_id=operator_id)
        if only_active:
            stmt = stmt.filter_by(is_active=True)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_all(self) -> list[Request]:
        stmt = select(Request)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def save(self, request: Request) -> None:
        self.session.add(request)
