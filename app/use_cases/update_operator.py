from uuid import UUID

from app.api.operators.schemas import UpdateOperatorCommand, UpdateOperatorResponse
from app.repositories.uow import UnitOfWork


class UpdateOperatorUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, operator_id: UUID, cmd: UpdateOperatorCommand) -> UpdateOperatorResponse:
        async with self._uow.begin():
            operator = await self._uow.operator_repository.get(operator_id)

            if cmd.name is not None:
                operator.name = cmd.name
            if cmd.is_active is not None:
                operator.is_active = cmd.is_active
            if cmd.max_leads is not None:
                operator.max_leads = cmd.max_leads

            await self._uow.operator_repository.save(operator)

        return UpdateOperatorResponse()
