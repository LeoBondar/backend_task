from functools import partial

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.requests import Request

from app.api.errors.api_error import ApiError, ErrorCode
from app.api.models.base import ApiResponse


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApiError, partial(api_exception_handler))
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)


async def api_exception_handler(request: Request, exc: ApiError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(ApiResponse(message=exc.message, error_code=exc.error_code, result=None)),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            ApiResponse(
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                message="Internal Server Error",
                result=None,
            )
        ),
    )


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(ApiResponse(error_code=ErrorCode.VALIDATION_ERROR, message=f"{exc}", result=None)),
    )
