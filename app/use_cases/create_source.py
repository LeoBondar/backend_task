from app.api.sources.schemas import CreateSourceCommand, CreateSourceResponse
from app.domain.models import Source
from app.repositories.uow import UnitOfWork


class CreateSourceUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, cmd: CreateSourceCommand) -> CreateSourceResponse:
        async with self._uow.begin():
            source = Source.create(
                name=cmd.name,
                code=cmd.code,
            )
            await self._uow.source_repository.save(source)

        return CreateSourceResponse(id=source.id, name=source.name, code=source.code)
