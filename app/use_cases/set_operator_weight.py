from uuid import UUID

from app.api.sources.schemas import SetOperatorWeightCommand, SetOperatorWeightResponse
from app.domain.models import OperatorWeight
from app.repositories.uow import UnitOfWork


class SetOperatorWeightUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, source_id: UUID, cmd: SetOperatorWeightCommand) -> SetOperatorWeightResponse:
        async with self._uow.begin():
            await self._uow.source_repository.get(source_id)
            await self._uow.operator_repository.get(cmd.operator_id)

            existing = await self._uow.operator_weight_repository.get_by_operator_and_source(cmd.operator_id, source_id)

            if existing:
                if cmd.weight == 0:
                    await self._uow.operator_weight_repository.delete(existing)
                else:
                    existing.weight = cmd.weight
            else:
                if cmd.weight > 0:
                    weight = OperatorWeight.create(
                        operator_id=cmd.operator_id,
                        source_id=source_id,
                        weight=cmd.weight,
                    )
                    await self._uow.operator_weight_repository.save(weight)

        return SetOperatorWeightResponse()
