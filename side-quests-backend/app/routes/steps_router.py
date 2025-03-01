from fastapi import APIRouter, Depends
from typing import List
from app.models.steps import Steps, StepCreate, StepUpdate
from app.services.steps import StepsService
from app.db.prisma_connection import get_prisma
from prisma import Prisma

router = APIRouter(prefix="/steps", tags=["Steps"])


def get_steps_service(prisma: Prisma = Depends(get_prisma)) -> StepsService:
    return StepsService(prisma)


@router.get("/", response_model=List[Steps])
async def read_steps(service: StepsService = Depends(get_steps_service)):
    return await service.get_steps()


@router.post("/", response_model=Steps)
async def create_step(
    step: StepCreate, service: StepsService = Depends(get_steps_service)
):
    return await service.insert_step(step)


@router.get("/{id}", response_model=Steps)
async def read_step_by_id(id: int, service: StepsService = Depends(get_steps_service)):
    return await service.get_step_by_id(id)


@router.put("/{id}", response_model=Steps)
async def update_step(
    id: int, step: StepUpdate, service: StepsService = Depends(get_steps_service)
):
    return await service.update_step(id, step)


@router.delete("/{id}", response_model=Steps)
async def delete_step(id: int, service: StepsService = Depends(get_steps_service)):
    return await service.delete_step(id)


@router.delete("/", response_model=List[Steps])
async def delete_all_steps(service: StepsService = Depends(get_steps_service)):
    return await service.delete_all_steps()
