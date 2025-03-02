from typing import List
from fastapi import APIRouter, HTTPException, Depends
from prisma import Prisma
from app.models.project import Project, ProjectCreate, ProjectUpdate, ProjectFromUser
from app.models.user import User
from app.models.user_project import UserProject
from app.services.project import ProjectService
from app.db.prisma_connection import get_prisma
from app.utils.security import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_service(prisma: Prisma = Depends(get_prisma)):
    return ProjectService(prisma)


@router.get("/user", response_model=List[ProjectFromUser])
async def get_user_projects(
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
):
    return await project_service.get_projects_by_user(current_user.id)


@router.post("/user", response_model=UserProject)
async def insert_project_to_user(
    project_id: int,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
):
    return await project_service.insert_project_to_user(current_user.id, project_id)


@router.get("/", status_code=200, response_model=List[Project])
async def get_projects(service: ProjectService = Depends(get_project_service)):
    return await service.get_projects()


@router.get("/{id}", status_code=200, response_model=Project)
async def get_project(id: int, service: ProjectService = Depends(get_project_service)):
    return await service.get_project_by_id(id)


@router.post("/", status_code=201)
async def create_project(
    project: ProjectCreate, service: ProjectService = Depends(get_project_service)
):
    return await service.insert_project(project)


@router.put("/{id}", status_code=200)
async def update_project(
    id: int,
    project: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
):
    return await service.update_project(id, project)


@router.delete("/", status_code=200)
async def delete_projects(service: ProjectService = Depends(get_project_service)):
    return await service.delete_projects()


@router.delete("/{id}", status_code=200)
async def delete_project(
    id: int, service: ProjectService = Depends(get_project_service)
):
    return await service.delete_project(id)
