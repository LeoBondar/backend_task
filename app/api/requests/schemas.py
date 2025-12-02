from uuid import UUID

from pydantic import Field

from app.utils.model import ApiCamelModel


class CreateRequestCommand(ApiCamelModel):
    lead_external_id: str = Field(min_length=1, max_length=255)
    source_id: UUID
    lead_phone: str | None = None
    lead_email: str | None = None
    lead_name: str | None = None
    message: str | None = None


class CreateRequestResponse(ApiCamelModel):
    id: UUID
    lead_id: UUID
    source_id: UUID
    operator_id: UUID | None
    is_assigned: bool


class RequestData(ApiCamelModel):
    id: UUID
    lead_id: UUID
    lead_external_id: str
    source_id: UUID
    source_name: str
    operator_id: UUID | None
    operator_name: str | None
    message: str | None
    is_active: bool


class GetRequestsResponse(ApiCamelModel):
    requests: list[RequestData]


class CloseRequestResponse(ApiCamelModel):
    success: bool = True


class LeadRequestData(ApiCamelModel):
    id: UUID
    source_name: str
    operator_name: str | None
    is_active: bool


class LeadData(ApiCamelModel):
    id: UUID
    external_id: str
    phone: str | None
    email: str | None
    name: str | None
    requests: list[LeadRequestData]


class GetLeadsResponse(ApiCamelModel):
    leads: list[LeadData]
