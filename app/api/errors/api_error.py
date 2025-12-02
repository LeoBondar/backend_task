from enum import IntEnum

from app.utils.exceptions import BaseAppException


class ErrorCode(IntEnum):
    SUCCESS = 0
    VALIDATION_ERROR = 2000
    INTERNAL_SERVER_ERROR = 5000
    OPERATOR_NOT_FOUND = 3000
    LEAD_NOT_FOUND = 3001
    SOURCE_NOT_FOUND = 3002
    REQUEST_NOT_FOUND = 3003


class ApiError(BaseAppException):
    status_code: int
    message: str | None
    error_code: ErrorCode

    def __init__(
        self,
        status_code: int | None = None,
        error_code: ErrorCode | None = None,
        message: str | None = None,
    ):
        if status_code:
            self.status_code = status_code
        if error_code:
            self.error_code = error_code
        if message:
            self.message = message


class OperatorNotFoundApiError(ApiError):
    status_code = 404
    error_code = ErrorCode.OPERATOR_NOT_FOUND
    message = "Operator not found"


class LeadNotFoundApiError(ApiError):
    status_code = 404
    error_code = ErrorCode.LEAD_NOT_FOUND
    message = "Lead not found"


class SourceNotFoundApiError(ApiError):
    status_code = 404
    error_code = ErrorCode.SOURCE_NOT_FOUND
    message = "Source not found"


class RequestNotFoundApiError(ApiError):
    status_code = 404
    error_code = ErrorCode.REQUEST_NOT_FOUND
    message = "Request not found"
