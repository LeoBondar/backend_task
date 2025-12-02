from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.settings import DatabaseSettings
from app.utils.common import Singleton


class Database:
    def __init__(self, settings: DatabaseSettings):
        self._settings = settings
        self._engine = self._create_engine()

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            expire_on_commit=False,
        )

    def _create_engine(self) -> AsyncEngine:
        return create_async_engine(self._settings.url, echo=self._settings.echo)

    async def shutdown(self) -> None:
        await self._engine.dispose()


class SessionContext(metaclass=Singleton):
    _session: ContextVar[AsyncSession | None] = ContextVar("session", default=None)

    @property
    def session(self) -> AsyncSession:
        current_session = self._session.get()
        return current_session

    @session.setter
    def session(self, session: AsyncSession) -> None:
        current_session = self._session.get()
        if current_session is not None:
            return
        self._session.set(session)

    def close_session(self) -> None:
        self._session.set(None)
