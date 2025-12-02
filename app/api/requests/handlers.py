from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path

from app.api.errors.api_error import ErrorCode
from app.api.models.base import ApiResponse
from app.api.requests.schemas import (
    CloseRequestResponse,
    CreateRequestCommand,
    CreateRequestResponse,
    GetLeadsResponse,
    GetRequestsResponse,
)
from app.dependencies.container import AppContainer
from app.use_cases.close_request import CloseRequestUseCase
from app.use_cases.create_request import CreateRequestUseCase
from app.views.get_leads import GetLeadsView
from app.views.get_requests import GetRequestsView

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("/", status_code=201)
@inject
async def create_request(
    cmd: CreateRequestCommand,
    use_case: CreateRequestUseCase = Depends(Provide[AppContainer.create_request_use_case]),
) -> ApiResponse[CreateRequestResponse]:
    result = await use_case(cmd=cmd)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.get("/")
@inject
async def get_requests(
    view: GetRequestsView = Depends(Provide[AppContainer.get_requests_view]),
) -> ApiResponse[GetRequestsResponse]:
    result = await view()
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.post("/{request_id}/close")
@inject
async def close_request(
    request_id: UUID = Path(),
    use_case: CloseRequestUseCase = Depends(Provide[AppContainer.close_request_use_case]),
) -> ApiResponse[CloseRequestResponse]:
    result = await use_case(request_id=request_id)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Closed")


leads_router = APIRouter(prefix="/leads", tags=["leads"])


@leads_router.get("/")
@inject
async def get_leads(
    view: GetLeadsView = Depends(Provide[AppContainer.get_leads_view]),
) -> ApiResponse[GetLeadsResponse]:
    result = await view()
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")
