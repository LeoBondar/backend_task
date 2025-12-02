from uuid import UUID

from app.api.sources.schemas import OperatorWeightData, SourceDetailData
from app.repositories.uow import UnitOfWork


class GetSourceDetailView:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, source_id: UUID) -> SourceDetailData:
        async with self._uow.begin():
            source = await self._uow.source_repository.get(source_id)
            weights = await self._uow.operator_weight_repository.get_by_source(source_id)

            operators_data = []
            for w in weights:
                operator = await self._uow.operator_repository.get(w.operator_id)
                operators_data.append(
                    OperatorWeightData(
                        operator_id=operator.id,
                        operator_name=operator.name,
                        weight=w.weight,
                    )
                )

        return SourceDetailData(
            id=source.id,
            name=source.name,
            code=source.code,
            operators=operators_data,
        )
