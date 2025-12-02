from app.api.sources.schemas import GetSourcesResponse, SourceData
from app.repositories.uow import UnitOfWork


class GetSourcesView:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self) -> GetSourcesResponse:
        async with self._uow.begin():
            sources = await self._uow.source_repository.get_all()
            result = [SourceData(id=s.id, name=s.name, code=s.code) for s in sources]

        return GetSourcesResponse(sources=result)
