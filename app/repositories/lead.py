from typing import Protocol
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Lead
from app.repositories.exception import RepositoryNotFoundException


class ILeadRepository(Protocol):
    async def get(self, lead_id: UUID) -> Lead:
        pass

    async def get_by_external_id(self, external_id: str) -> Lead | None:
        pass

    async def get_all(self) -> list[Lead]:
        pass

    async def save(self, lead: Lead) -> None:
        pass


class LeadRepository(ILeadRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, lead_id: UUID) -> Lead:
        stmt = select(Lead).filter_by(id=lead_id)
        lead = (await self.session.execute(stmt)).scalar()
        if not lead:
            raise RepositoryNotFoundException
        return lead

    async def get_by_external_id(self, external_id: str) -> Lead | None:
        stmt = select(Lead).filter_by(external_id=external_id)
        return (await self.session.execute(stmt)).scalar()

    async def get_all(self) -> list[Lead]:
        stmt = select(Lead)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def save(self, lead: Lead) -> None:
        self.session.add(lead)
