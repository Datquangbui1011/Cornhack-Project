import logging
from typing import Any, List
from fastapi import HTTPException
from pydantic import ValidationError
from prisma.errors import PrismaError
from prisma import Prisma
from app.models.steps import (
    Step,
    StepCompletedTable,
    StepCreate,
    StepUpdate,
    StepsCompleted,
)
from app.utils.decorators import handle_service_exceptions
from app.core.logging_config import logger


class StepsService:
    """
    Service class for managing Steps operations.
    """

    def __init__(self, prisma_client: Prisma):
        self.prisma = prisma_client

    @handle_service_exceptions
    async def get_steps(self) -> List[Step]:
        steps_list = await self.prisma.steps.find_many(include={"stepbreakdown": True})
        if not steps_list:
            return []
        return [
            Step.model_validate(step.model_dump(mode="python")) for step in steps_list
        ]

    @handle_service_exceptions
    async def get_steps_by_project_user(
        self, project_id: int, user_id: int
    ) -> List[StepsCompleted]:
        steps_list = await self.prisma.stepscompleted.find_many(
            where={
                "userproject": {
                    "projectId": project_id,
                    "userId": user_id,
                }
            },
            include={"steps": {"include": {"stepbreakdown": True}}},
        )
        if not steps_list:
            return []
        return [
            StepsCompleted.model_validate(
                {
                    **step.steps.model_dump(mode="python"),
                    "completed": step.model_dump(mode="python")["completed"],
                }
            )
            for step in steps_list
        ]

    @handle_service_exceptions
    async def create_stepsCompleted(
        self, project_id: int, step_ids: list[int], user_id: int
    ) -> dict[str, Any]:

        user_project = await self.prisma.userproject.find_first(
            where={"userId": user_id, "projectId": project_id}
        )

        if not user_project:
            raise ValueError(
                "UserProject not found for the given user and project IDs."
            )

        # Prepare data for bulk creation
        data = [
            {
                "stepsId": step_id,  # Directly referencing step ID
                "userProjectId": user_project.id,  # Directly referencing userProject ID
                "completed": False,
            }
            for step_id in step_ids
        ]

        # Perform the bulk creation
        results = await self.prisma.stepscompleted.create_many(data=data)
        return {"message": "StepsCompleted created successfully", "results": results}

    @handle_service_exceptions
    async def complete_step(
        self, step_id: int, user_id: int, project_id: int, completed: bool
    ) -> Any:
        # Get the UserProject ID from userId and projectId
        user_project = await self.prisma.userproject.find_unique(
            where={
                "userId_projectId": {  # Name of the composite key
                    "userId": user_id,
                    "projectId": project_id,
                }
            }
        )

        if not user_project:
            raise HTTPException(status_code=404, detail="User project not found")

        # Now update StepsCompleted using the UserProject ID
        step = await self.prisma.stepscompleted.update(
            where={
                "userProjectId_stepsId": {  # Composite key of StepsCompleted
                    "userProjectId": user_project.id,  # Use the UserProject ID
                    "stepsId": step_id,
                }
            },
            data={"completed": completed},
            include={"steps": {"include": {"stepbreakdown": True}}},
        )

        return {"message": "Step completed successfully"}

    @handle_service_exceptions
    async def insert_step(self, step: StepCreate) -> Step:
        # Use connectOrCreate for nested step breakdowns if provided
        data = {
            **step.model_dump(mode="python"),
            "stepbreakdown": {
                "connectOrCreate": [
                    {
                        "where": {"description": breakdown.description},
                        "create": {"description": breakdown.description},
                    }
                    for breakdown in step.stepbreakdown or []
                ]
            },
        }
        created_step = await self.prisma.steps.create(
            data=data, include={"stepbreakdown": True}
        )
        return Step.model_validate(created_step.model_dump(mode="python"))

    @handle_service_exceptions
    async def get_step_by_id(self, id: int) -> Step:
        step = await self.prisma.steps.find_unique(
            where={"id": id}, include={"stepbreakdown": True}
        )
        if step is None:
            raise HTTPException(status_code=404, detail="Step not found")
        return Step.model_validate(step.model_dump(mode="python"))

    @handle_service_exceptions
    async def update_step(self, id: int, step: StepUpdate) -> Step:
        update_data = step.model_dump(exclude_unset=True)
        updated_step = await self.prisma.steps.update(
            where={"id": id},
            data=update_data,
            include={"stepbreakdown": True},
        )
        if not updated_step:
            raise HTTPException(status_code=404, detail="Step not found")
        return Step.model_validate(updated_step.model_dump(mode="python"))

    @handle_service_exceptions
    async def delete_step(self, id: int) -> Step:
        step = await self.prisma.steps.delete(
            where={"id": id}, include={"stepbreakdown": True}
        )
        if not step:
            raise HTTPException(status_code=404, detail="Step not found")
        return Step.model_validate(step.model_dump(mode="python"))

    @handle_service_exceptions
    async def delete_all_steps(self) -> Any:
        count = await self.prisma.steps.delete_many()
        return {"message": f"Deleted {count} steps"}
