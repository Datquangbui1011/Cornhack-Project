from typing import List
from fastapi import APIRouter, HTTPException, Depends
from app.models.project import Project, ProjectCreate
from app.services.project import ProjectService
from app.db.prisma_connection import get_prisma

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_service():
    return ProjectService(get_prisma())


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
    project: ProjectCreate,
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
