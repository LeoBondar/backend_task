import random
from dataclasses import dataclass
from uuid import UUID

from app.api.requests.schemas import CreateRequestCommand, CreateRequestResponse
from app.domain.models import Lead, Request
from app.repositories.uow import UnitOfWork


@dataclass
class OperatorCandidate:
    operator_id: UUID
    weight: int
    current_load: int
    max_leads: int


class CreateRequestUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, cmd: CreateRequestCommand) -> CreateRequestResponse:
        async with self._uow.begin():
            lead = await self._get_or_create_lead(cmd)

            source = await self._uow.source_repository.get(cmd.source_id)

            operator_id = await self._select_operator(source.id)

            request = Request.create(
                lead_id=lead.id,
                source_id=source.id,
                operator_id=operator_id,
                message=cmd.message,
            )
            await self._uow.request_repository.save(request)

        return CreateRequestResponse(
            id=request.id,
            lead_id=lead.id,
            source_id=source.id,
            operator_id=operator_id,
            is_assigned=operator_id is not None,
        )

    async def _get_or_create_lead(self, cmd: CreateRequestCommand) -> Lead:
        lead = await self._uow.lead_repository.get_by_external_id(cmd.lead_external_id)
        if lead:
            return lead

        lead = Lead.create(
            external_id=cmd.lead_external_id,
            phone=cmd.lead_phone,
            email=cmd.lead_email,
            name=cmd.lead_name,
        )
        await self._uow.lead_repository.save(lead)
        return lead

    async def _select_operator(self, source_id: UUID) -> UUID | None:
        weights = await self._uow.operator_weight_repository.get_by_source(source_id)
        if not weights:
            return None

        candidates: list[OperatorCandidate] = []

        for w in weights:
            operator = await self._uow.operator_repository.get(w.operator_id)
            if not operator.is_active:
                continue

            current_load = await self._uow.operator_repository.get_active_requests_count(operator.id)

            if current_load >= operator.max_leads:
                continue

            candidates.append(
                OperatorCandidate(
                    operator_id=operator.id,
                    weight=w.weight,
                    current_load=current_load,
                    max_leads=operator.max_leads,
                )
            )

        if not candidates:
            return None

        return self._weighted_random_choice(candidates)

    def _weighted_random_choice(self, candidates: list[OperatorCandidate]) -> UUID:
        total_weight = sum(c.weight for c in candidates)
        r = random.uniform(0, total_weight)

        cumulative = 0
        for candidate in candidates:
            cumulative += candidate.weight
            if r <= cumulative:
                return candidate.operator_id

        return candidates[-1].operator_id
