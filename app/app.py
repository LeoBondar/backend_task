from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.api.errors.handlers import register_exception_handlers
from app.api.router import init_router
from app.dependencies.container import AppContainer
from app.persistent.db_schemas.tables import init_mappers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_mappers()
    container: AppContainer = app.state.container

    if coro := container.init_resources():
        await coro

    yield

    if coro := container.shutdown_resources():
        await coro


def create_app() -> FastAPI:
    container = AppContainer()
    settings = container.settings()

    app = FastAPI(title=settings.srv.app_name, version="0.1.0", lifespan=lifespan)
    app.state.container = container
    init_router(app)
    register_exception_handlers(app)

    return app
