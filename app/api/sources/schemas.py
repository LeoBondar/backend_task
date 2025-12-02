from uuid import UUID

from pydantic import Field

from app.utils.model import ApiCamelModel


class CreateSourceCommand(ApiCamelModel):
    name: str = Field(min_length=2, max_length=100)
    code: str = Field(min_length=2, max_length=50)


class CreateSourceResponse(ApiCamelModel):
    id: UUID
    name: str
    code: str


class SetOperatorWeightCommand(ApiCamelModel):
    operator_id: UUID
    weight: int = Field(ge=0, le=1000)


class SetOperatorWeightResponse(ApiCamelModel):
    success: bool = True


class OperatorWeightData(ApiCamelModel):
    operator_id: UUID
    operator_name: str
    weight: int


class SourceData(ApiCamelModel):
    id: UUID
    name: str
    code: str


class SourceDetailData(ApiCamelModel):
    id: UUID
    name: str
    code: str
    operators: list[OperatorWeightData]


class GetSourcesResponse(ApiCamelModel):
    sources: list[SourceData]
