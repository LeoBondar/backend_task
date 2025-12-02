from app.api.requests.schemas import GetLeadsResponse, LeadData, LeadRequestData
from app.repositories.uow import UnitOfWork


class GetLeadsView:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self) -> GetLeadsResponse:
        async with self._uow.begin():
            leads = await self._uow.lead_repository.get_all()
            result = []

            for lead in leads:
                requests = await self._uow.request_repository.get_by_lead(lead.id)
                requests_data = []

                for req in requests:
                    source = await self._uow.source_repository.get(req.source_id)
                    operator_name = None
                    if req.operator_id:
                        operator = await self._uow.operator_repository.get(req.operator_id)
                        operator_name = operator.name

                    requests_data.append(
                        LeadRequestData(
                            id=req.id,
                            source_name=source.name,
                            operator_name=operator_name,
                            is_active=req.is_active,
                        )
                    )

                result.append(
                    LeadData(
                        id=lead.id,
                        external_id=lead.external_id,
                        phone=lead.phone,
                        email=lead.email,
                        name=lead.name,
                        requests=requests_data,
                    )
                )

        return GetLeadsResponse(leads=result)
