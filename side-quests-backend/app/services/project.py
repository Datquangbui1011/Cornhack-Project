from typing import Any, List
from fastapi import HTTPException
from prisma import Prisma
from app.models.project import Project, ProjectCreate, ProjectUpdate, ProjectFromUser
from app.models.user_project import UserProject
from app.utils.decorators import handle_service_exceptions
from app.core.logging_config import logger
\

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
    async def get_projects_by_user(self, user_id: int) -> List[ProjectFromUser]:
        user_projects = await self.prisma.userproject.find_many(
            where={"userId": user_id},
            include={"project": {"include": {"category": True}}},
        )
        return [
            ProjectFromUser.model_validate(
                {
                    **up.project.model_dump(mode="python", exclude_unset=True),
                    "completed": up.model_dump(
                        mode="python",
                    )["completed"],
                }
            )
            for up in user_projects
        ]

    @handle_service_exceptions
    async def insert_project_to_user(
        self, user_id: int, project_id: int
    ) -> UserProject:
        created = await self.prisma.userproject.create(
            data={"userId": user_id, "projectId": project_id, "completed": False}
        )
        return UserProject.model_validate(created.model_dump(mode="python"))

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
