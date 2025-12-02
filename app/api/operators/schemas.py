from uuid import UUID

from pydantic import Field

from app.utils.model import ApiCamelModel


class CreateOperatorCommand(ApiCamelModel):
    name: str = Field(min_length=2, max_length=100)
    max_leads: int = Field(default=10, ge=1)
    is_active: bool = Field(default=True)


class CreateOperatorResponse(ApiCamelModel):
    id: UUID
    name: str


class UpdateOperatorCommand(ApiCamelModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    max_leads: int | None = Field(default=None, ge=1)
    is_active: bool | None = None


class UpdateOperatorResponse(ApiCamelModel):
    success: bool = True


class OperatorData(ApiCamelModel):
    id: UUID
    name: str
    is_active: bool
    max_leads: int
    current_load: int = 0


class GetOperatorsResponse(ApiCamelModel):
    operators: list[OperatorData]
