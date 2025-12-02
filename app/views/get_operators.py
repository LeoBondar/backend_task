from app.api.operators.schemas import GetOperatorsResponse, OperatorData
from app.repositories.uow import UnitOfWork


class GetOperatorsView:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self) -> GetOperatorsResponse:
        async with self._uow.begin():
            operators = await self._uow.operator_repository.get_all()
            result = []

            for op in operators:
                current_load = await self._uow.operator_repository.get_active_requests_count(op.id)
                result.append(
                    OperatorData(
                        id=op.id,
                        name=op.name,
                        is_active=op.is_active,
                        max_leads=op.max_leads,
                        current_load=current_load,
                    )
                )

        return GetOperatorsResponse(operators=result)
