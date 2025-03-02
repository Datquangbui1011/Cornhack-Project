from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List
from app.models.step_breakdown import (
    StepBreakdown,
    StepBreakdownCreate,
    StepBreakdownUpdate,
)
from app.services.steps_breakdown import StepBreakdownService
from app.db.prisma_connection import (
    get_prisma,
)  # Dependency that returns a Prisma client
from prisma import Prisma

router = APIRouter(prefix="/steps/{step_id}/stepbreakdown", tags=["StepBreakdown"])


def get_step_breakdown_service(
    prisma: Prisma = Depends(get_prisma),
) -> StepBreakdownService:
    return StepBreakdownService(prisma)


@router.get("/", response_model=List[StepBreakdown])
async def get_breakdowns(
    step_id: int = Path(..., description="The ID of the step"),
    service: StepBreakdownService = Depends(get_step_breakdown_service),
):
    return await service.get_breakdowns_for_step(step_id)


@router.get("/{breakdown_id}", response_model=StepBreakdown)
async def get_breakdown(
    step_id: int = Path(..., description="The ID of the step"),
    breakdown_id: int = Path(..., description="The ID of the breakdown"),
    service: StepBreakdownService = Depends(get_step_breakdown_service),
):
    return await service.get_breakdown_by_id(step_id, breakdown_id)


@router.post("/", response_model=StepBreakdown)
async def create_breakdown(
    breakdown: StepBreakdownCreate,
    step_id: int = Path(..., description="The ID of the step"),
    service: StepBreakdownService = Depends(get_step_breakdown_service),
):
    return await service.create_breakdown_for_step(step_id, breakdown)


@router.put("/{breakdown_id}", response_model=StepBreakdown)
async def update_breakdown(
    breakdown: StepBreakdownUpdate,
    step_id: int = Path(..., description="The ID of the step"),
    breakdown_id: int = Path(..., description="The ID of the breakdown"),
    service: StepBreakdownService = Depends(get_step_breakdown_service),
):
    return await service.update_breakdown(step_id, breakdown_id, breakdown)


@router.delete("/{breakdown_id}", response_model=StepBreakdown)
async def delete_breakdown(
    step_id: int = Path(..., description="The ID of the step"),
    breakdown_id: int = Path(..., description="The ID of the breakdown"),
    service: StepBreakdownService = Depends(get_step_breakdown_service),
):
    return await service.delete_breakdown(step_id, breakdown_id)


@router.delete("/", response_model=List[StepBreakdown])
async def delete_breakdowns_for_step(
    step_id: int = Path(..., description="The ID of the step"),
    service: StepBreakdownService = Depends(get_step_breakdown_service),
):
    return await service.delete_breakdowns_for_step(step_id)
