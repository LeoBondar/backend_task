from app.api.operators.schemas import CreateOperatorCommand, CreateOperatorResponse
from app.domain.models import Operator
from app.repositories.uow import UnitOfWork


class CreateOperatorUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, cmd: CreateOperatorCommand) -> CreateOperatorResponse:
        async with self._uow.begin():
            operator = Operator.create(
                name=cmd.name,
                max_leads=cmd.max_leads,
                is_active=cmd.is_active,
            )
            await self._uow.operator_repository.save(operator)

        return CreateOperatorResponse(id=operator.id, name=operator.name)
