from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path

from app.api.errors.api_error import ErrorCode
from app.api.models.base import ApiResponse
from app.api.sources.schemas import (
    CreateSourceCommand,
    CreateSourceResponse,
    GetSourcesResponse,
    SetOperatorWeightCommand,
    SetOperatorWeightResponse,
    SourceDetailData,
)
from app.dependencies.container import AppContainer
from app.use_cases.create_source import CreateSourceUseCase
from app.use_cases.set_operator_weight import SetOperatorWeightUseCase
from app.views.get_source_detail import GetSourceDetailView
from app.views.get_sources import GetSourcesView

router = APIRouter(prefix="/sources", tags=["sources"])


@router.post("/", status_code=201)
@inject
async def create_source(
    cmd: CreateSourceCommand,
    use_case: CreateSourceUseCase = Depends(Provide[AppContainer.create_source_use_case]),
) -> ApiResponse[CreateSourceResponse]:
    result = await use_case(cmd=cmd)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.get("/")
@inject
async def get_sources(
    view: GetSourcesView = Depends(Provide[AppContainer.get_sources_view]),
) -> ApiResponse[GetSourcesResponse]:
    result = await view()
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.get("/{source_id}")
@inject
async def get_source_detail(
    source_id: UUID = Path(),
    view: GetSourceDetailView = Depends(Provide[AppContainer.get_source_detail_view]),
) -> ApiResponse[SourceDetailData]:
    result = await view(source_id=source_id)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.post("/{source_id}/operators")
@inject
async def set_operator_weight(
    cmd: SetOperatorWeightCommand,
    source_id: UUID = Path(),
    use_case: SetOperatorWeightUseCase = Depends(Provide[AppContainer.set_operator_weight_use_case]),
) -> ApiResponse[SetOperatorWeightResponse]:
    result = await use_case(source_id=source_id, cmd=cmd)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Weight set")
