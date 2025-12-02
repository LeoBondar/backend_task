from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path

from app.api.errors.api_error import ErrorCode
from app.api.models.base import ApiResponse
from app.api.operators.schemas import (
    CreateOperatorCommand,
    CreateOperatorResponse,
    GetOperatorsResponse,
    OperatorData,
    UpdateOperatorCommand,
    UpdateOperatorResponse,
)
from app.dependencies.container import AppContainer
from app.use_cases.create_operator import CreateOperatorUseCase
from app.use_cases.update_operator import UpdateOperatorUseCase
from app.views.get_operators import GetOperatorsView

router = APIRouter(prefix="/operators", tags=["operators"])


@router.post("/", status_code=201)
@inject
async def create_operator(
    cmd: CreateOperatorCommand,
    use_case: CreateOperatorUseCase = Depends(Provide[AppContainer.create_operator_use_case]),
) -> ApiResponse[CreateOperatorResponse]:
    result = await use_case(cmd=cmd)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.get("/")
@inject
async def get_operators(
    view: GetOperatorsView = Depends(Provide[AppContainer.get_operators_view]),
) -> ApiResponse[GetOperatorsResponse]:
    result = await view()
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.patch("/{operator_id}")
@inject
async def update_operator(
    cmd: UpdateOperatorCommand,
    operator_id: UUID = Path(),
    use_case: UpdateOperatorUseCase = Depends(Provide[AppContainer.update_operator_use_case]),
) -> ApiResponse[UpdateOperatorResponse]:
    result = await use_case(operator_id=operator_id, cmd=cmd)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Updated")
