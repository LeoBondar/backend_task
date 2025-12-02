from typing import Protocol
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Source
from app.repositories.exception import RepositoryNotFoundException


class ISourceRepository(Protocol):
    async def get(self, source_id: UUID) -> Source:
        pass

    async def get_by_code(self, code: str) -> Source | None:
        pass

    async def get_all(self) -> list[Source]:
        pass

    async def save(self, source: Source) -> None:
        pass


class SourceRepository(ISourceRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, source_id: UUID) -> Source:
        stmt = select(Source).filter_by(id=source_id)
        source = (await self.session.execute(stmt)).scalar()
        if not source:
            raise RepositoryNotFoundException
        return source

    async def get_by_code(self, code: str) -> Source | None:
        stmt = select(Source).filter_by(code=code)
        return (await self.session.execute(stmt)).scalar()

    async def get_all(self) -> list[Source]:
        stmt = select(Source)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def save(self, source: Source) -> None:
        self.session.add(source)
