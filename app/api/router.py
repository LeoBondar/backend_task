from fastapi import APIRouter, FastAPI

from app.api.operators.handlers import router as operators_router
from app.api.requests.handlers import leads_router
from app.api.requests.handlers import router as requests_router
from app.api.sources.handlers import router as sources_router

API_V1_PREFIX = "/api/v1"

root_router = APIRouter()
root_router.include_router(operators_router, prefix=API_V1_PREFIX)
root_router.include_router(sources_router, prefix=API_V1_PREFIX)
root_router.include_router(requests_router, prefix=API_V1_PREFIX)
root_router.include_router(leads_router, prefix=API_V1_PREFIX)


def init_router(app: FastAPI) -> None:
    app.include_router(root_router)
