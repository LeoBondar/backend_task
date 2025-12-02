from contextlib import asynccontextmanager
from typing import AsyncGenerator, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db import Database, SessionContext
from app.repositories.lead import ILeadRepository, LeadRepository
from app.repositories.operator import IOperatorRepository, OperatorRepository
from app.repositories.operator_weight import IOperatorWeightRepository, OperatorWeightRepository
from app.repositories.request import IRequestRepository, RequestRepository
from app.repositories.source import ISourceRepository, SourceRepository


class IUnitOfWork(Protocol):
    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self, database: Database, session_context: SessionContext) -> None:
        self._database = database
        self._session_context = session_context

    @property
    def session(self) -> AsyncSession:
        return self._session_context.session

    @asynccontextmanager
    async def begin(self) -> AsyncGenerator[AsyncSession, None]:
        session = None

        if not self._session_context.session:
            session = self._database.session_factory()
            self._session_context.session = session

        if self.session.in_transaction():
            yield self.session
        else:
            try:
                async with self.session.begin():
                    yield self.session
            finally:
                if session:
                    await session.close()
                self._session_context.close_session()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    @property
    def operator_repository(self) -> IOperatorRepository:
        return OperatorRepository(self.session)

    @property
    def lead_repository(self) -> ILeadRepository:
        return LeadRepository(self.session)

    @property
    def source_repository(self) -> ISourceRepository:
        return SourceRepository(self.session)

    @property
    def operator_weight_repository(self) -> IOperatorWeightRepository:
        return OperatorWeightRepository(self.session)

    @property
    def request_repository(self) -> IRequestRepository:
        return RequestRepository(self.session)
