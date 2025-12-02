from uuid import UUID

from app.api.requests.schemas import CloseRequestResponse
from app.repositories.uow import UnitOfWork


class CloseRequestUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, request_id: UUID) -> CloseRequestResponse:
        async with self._uow.begin():
            request = await self._uow.request_repository.get(request_id)
            request.close()

        return CloseRequestResponse()
