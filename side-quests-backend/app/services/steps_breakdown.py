import logging
from typing import Any, List
from fastapi import HTTPException
from pydantic import ValidationError
from prisma.errors import PrismaError
from prisma import Prisma
from app.models.step_breakdown import (
    StepBreakdown,
    StepBreakdownCreate,
    StepBreakdownUpdate,
)
from app.utils.decorators import handle_service_exceptions
from app.core.logging_config import logger


class StepBreakdownService:
    """
    Service class for managing StepBreakdown operations.
    """

    def __init__(self, prisma_client: Prisma):
        self.prisma = prisma_client

    @handle_service_exceptions
    async def get_breakdowns_for_step(self, step_id: int) -> List[StepBreakdown]:
        breakdowns = await self.prisma.stepbreakdown.find_many(
            where={"stepsId": step_id}
        )
        if not breakdowns:
            raise HTTPException(
                status_code=404, detail="No breakdowns found for the step"
            )
        return [
            StepBreakdown.model_validate(b.model_dump(mode="python"))
            for b in breakdowns
        ]

    @handle_service_exceptions
    async def get_breakdown_by_id(
        self, step_id: int, breakdown_id: int
    ) -> StepBreakdown:
        breakdown = await self.prisma.stepbreakdown.find_unique(
            where={"id": breakdown_id, "stepsId": step_id}
        )
        if breakdown is None:
            raise HTTPException(status_code=404, detail="Breakdown not found")
        return StepBreakdown.model_validate(breakdown.model_dump(mode="python"))

    @handle_service_exceptions
    async def create_breakdown_for_step(
        self, step_id: int, breakdown: StepBreakdownCreate
    ) -> StepBreakdown:
        created = await self.prisma.stepbreakdown.create(
            data={
                **breakdown.model_dump(mode="python"),
                "step": {"connect": {"id": step_id}},
            }
        )
        return StepBreakdown.model_validate(created.model_dump(mode="python"))

    @handle_service_exceptions
    async def update_breakdown(
        self, step_id: int, breakdown_id: int, breakdown: StepBreakdownUpdate
    ) -> StepBreakdown:
        update_data = breakdown.model_dump(exclude_unset=True)
        updated = await self.prisma.stepbreakdown.update(
            where={"id": breakdown_id, "stepsId": step_id}, data=update_data
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Breakdown not found")
        if updated.stepsId != step_id:
            raise HTTPException(status_code=400, detail="Mismatched step ID")
        return StepBreakdown.model_validate(updated.model_dump(mode="python"))

    @handle_service_exceptions
    async def delete_breakdown(self, step_id: int, breakdown_id: int) -> StepBreakdown:
        deleted = await self.prisma.stepbreakdown.delete(
            where={"id": breakdown_id, "stepsId": step_id}
        )
        if not deleted:
            raise HTTPException(status_code=404, detail="Breakdown not found")
        if deleted.stepsId != step_id:
            raise HTTPException(status_code=400, detail="Mismatched step ID")
        return StepBreakdown.model_validate(deleted.model_dump(mode="python"))

    @handle_service_exceptions
    async def delete_breakdowns_for_step(self, step_id: int) -> Any:
        count = await self.prisma.stepbreakdown.delete_many(where={"stepsId": step_id})
        return {"message": f"Deleted {count} breakdowns for step {step_id}"}
