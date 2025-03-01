import logging
from typing import Any, List
from fastapi import HTTPException
from pydantic import ValidationError
from prisma.errors import PrismaError
from prisma import Prisma
from app.models.project import Project, ProjectCreate, ProjectUpdate
from app.utils.decorators import handle_service_exceptions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class ProjectService:
    """
    Service class for managing project operations.
    """

    def __init__(self, prisma_client: Prisma):
        self.prisma = prisma_client

    @handle_service_exceptions
    async def get_projects(self) -> List[Project]:
        projects = await self.prisma.project.find_many(include={"category": True})
        if not projects:
            return []
        return [
            Project.model_validate(project.model_dump(mode="python"))
            for project in projects
        ]

    @handle_service_exceptions
    async def insert_project(self, project: ProjectCreate) -> Project:
        created = await self.prisma.project.create(
            data=project.model_dump(mode="python"),
            include={"category": True},
        )
        return Project.model_validate(created.model_dump(mode="python"))

    @handle_service_exceptions
    async def get_project_by_id(self, id: int) -> Project:
        project = await self.prisma.project.find_unique(where={"id": id})
        if project is None:
            logger.error("Project not found")
            raise HTTPException(status_code=404, detail="Project not found")
        return Project.model_validate(project.model_dump(mode="python"))

    @handle_service_exceptions
    async def update_project(self, id: int, project: ProjectUpdate) -> Project:
        update_data = project.model_dump(exclude_unset=True)
        updated_project = await self.prisma.project.update(
            where={"id": id},
            data=update_data,
            include={"category": True},
        )
        if not updated_project:
            logger.error("Project not found")
            raise HTTPException(status_code=404, detail="Project not found")
        return Project.model_validate(updated_project.model_dump(mode="python"))

    @handle_service_exceptions
    async def delete_projects(self) -> Any:
        count = await self.prisma.project.delete_many()
        return {"message": f"Deleted {count} projects"}

    @handle_service_exceptions
    async def delete_project(self, id: int) -> Project:
        project = await self.prisma.project.delete(
            where={"id": id}, include={"category": True}
        )
        if not project:
            logger.error("Project not found")
            raise HTTPException(status_code=404, detail="Project not found")
        return Project.model_validate(project.model_dump(mode="python"))
