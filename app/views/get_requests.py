from app.api.requests.schemas import GetRequestsResponse, RequestData
from app.repositories.uow import UnitOfWork


class GetRequestsView:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self) -> GetRequestsResponse:
        async with self._uow.begin():
            requests = await self._uow.request_repository.get_all()
            result = []

            for req in requests:
                lead = await self._uow.lead_repository.get(req.lead_id)
                source = await self._uow.source_repository.get(req.source_id)

                operator_name = None
                if req.operator_id:
                    operator = await self._uow.operator_repository.get(req.operator_id)
                    operator_name = operator.name

                result.append(
                    RequestData(
                        id=req.id,
                        lead_id=lead.id,
                        lead_external_id=lead.external_id,
                        source_id=source.id,
                        source_name=source.name,
                        operator_id=req.operator_id,
                        operator_name=operator_name,
                        message=req.message,
                        is_active=req.is_active,
                    )
                )

        return GetRequestsResponse(requests=result)
