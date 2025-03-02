from fastapi import APIRouter, Depends
from typing import List
from app.models.steps import Step, StepCreate, StepUpdate, StepsCompleted
from app.models.user import User
from app.services.steps import StepsService
from app.db.prisma_connection import get_prisma
from prisma import Prisma

from app.utils.security import get_current_user

router = APIRouter(prefix="/steps", tags=["Steps"])


def get_steps_service(prisma: Prisma = Depends(get_prisma)) -> StepsService:
    return StepsService(prisma)


@router.get("/", response_model=List[Step])
async def read_steps(service: StepsService = Depends(get_steps_service)):
    return await service.get_steps()


@router.get("/user", response_model=List[StepsCompleted])
async def read_steps_by_project_user(
    project_id: int,
    current_user: User = Depends(get_current_user),
    service: StepsService = Depends(get_steps_service),
):
    return await service.get_steps_by_project_user(project_id, current_user.id)


@router.put("/complete/{id}", response_model=StepsCompleted)
async def complete_step(
    id: int,
    completed: bool,
    project_id: int,
    service: StepsService = Depends(get_steps_service),
    current_user: User = Depends(get_current_user),
):
    return await service.complete_step(id, current_user.id, project_id, completed)


@router.post("/", response_model=Step)
async def create_step(
    step: StepCreate, service: StepsService = Depends(get_steps_service)
):
    return await service.insert_step(step)


# @router.put("/{id}", response_model=Steps)
# async def update_step(
#     id: int, step: StepUpdate, service: StepsService = Depends(get_steps_service)
# ):
#     return await service.update_step(id, step)


@router.delete("/{id}", response_model=Step)
async def delete_step(id: int, service: StepsService = Depends(get_steps_service)):
    return await service.delete_step(id)


@router.delete("/", response_model=List[Step])
async def delete_all_steps(service: StepsService = Depends(get_steps_service)):
    return await service.delete_all_steps()
