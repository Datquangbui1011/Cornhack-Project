import logging
from typing import Any, List, Optional
from fastapi import HTTPException
from pydantic import ValidationError
from app.db.prisma_connection import get_prisma
from prisma.errors import PrismaError
from prisma import Prisma
from app.models.project import Project, ProjectCreate, ProjectUpdate

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
        """
        Initialize the ProjectService with a Prisma client.

        :param prisma_client: An instance of the Prisma client. If not provided,
                              get_prisma() will be used to obtain one.
        """
        self.prisma = prisma_client

    async def get_projects(self) -> List[Project]:
        """
        Retrieve all projects.

        :return: A list of project objects.
        :raises HTTPException: If fetching projects fails.
        """
        try:
            projects = await self.prisma.project.find_many(include={"category": True})
            if projects is None:
                return []
            return [
                Project.model_validate(project.model_dump(mode="python"))
                for project in projects
            ]
        except PrismaError as e:
            logger.error(f"Error fetching projects: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except ValidationError as e:
            logger.error(f"Error validating projects: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Error fetching projects: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def insert_project(self, project: ProjectCreate) -> Project:
        """
        Insert or update a project using the upsert operation.
        The upsert will update an existing project if it exists; otherwise, it will create a new one.
        In the create branch, it uses nested writes to create or connect languages.

        :param project: A ProjectCreate instance with project data.
        :return: The inserted or updated project object.
        :raises HTTPException: If inserting/updating the project fails.
        """
        try:
            project = await self.prisma.project.create(
                data=project.model_dump(mode="python"), include={"category": True}
            )
            return Project.model_validate(project.model_dump(mode="python"))
        except PrismaError as e:
            logger.error(f"Error inserting/updating project: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except ValidationError as e:
            logger.error(f"Error validating project: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Error inserting/updating project: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def get_project_by_id(self, id: int) -> Project:
        """
        Retrieve a single project by its ID.

        :param id: The unique identifier of the project.
        :return: The project object corresponding to the provided ID.
        :raises HTTPException: If the project is not found or the database call fails.
        """
        try:
            project = await self.prisma.project.find_unique(where={"id": id})
            if project is None:
                logger.error("Project not found")
                raise HTTPException(status_code=404, detail="Project not found")
            return Project.model_validate(project.model_dump(mode="python"))
        except PrismaError as e:
            logger.error(f"Error fetching project by ID: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except ValidationError as e:
            logger.error(f"Error validating project by ID: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Error fetching project by ID: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def update_project(self, id: int, project: ProjectUpdate) -> Project:
        """
        Update a project by its ID.

        :param id: The unique identifier of the project to update.
        :param project: A ProjectUpdate instance with updated project data.
        :return: The updated project object.
        :raises HTTPException: If the project is not found or update fails.
        """

        try:
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
        except PrismaError as e:
            logger.error(f"Error updating project: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except ValidationError as e:
            logger.error(f"Error validating project: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Error updating project: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_projects(self) -> Any:
        """
        Delete all projects.

        :return: The deleted project object.
        :raises HTTPException: If deletion fails.
        """
        try:
            count = await self.prisma.project.delete_many()
            return {"message": f"Deleted {count} projects"}
        except PrismaError as e:
            logger.error(f"Error deleting projects: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except ValidationError as e:
            logger.error(f"Error validating projects: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Error deleting projects: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_project(self, id: int) -> Project:
        """
        Delete a project by its ID.

        :param id: The unique identifier of the project to delete.
        :return: The deleted project object.
        :raises HTTPException: If the project is not found or deletion fails.
        """
        try:
            project = await self.prisma.project.delete(
                where={"id": id}, include={"category": True}
            )

            if not project:
                logger.error("Project not found")
                raise HTTPException(status_code=404, detail="Project not found")

            return Project.model_validate(project.model_dump(mode="python"))
        except PrismaError as e:
            logger.error(f"Error deleting project: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except ValidationError as e:
            logger.error(f"Error validating project: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Error deleting project: {e}")
            raise HTTPException(status_code=500, detail=str(e))
