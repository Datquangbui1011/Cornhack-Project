import logging
from typing import Any, List
from fastapi import HTTPException
from pydantic import ValidationError
from prisma.errors import PrismaError
from prisma import Prisma
from app.models.steps import Step, StepCreate, StepUpdate, StepsCompleted
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
    async def complete_step(
        self, step_id, user_id, project_id: int, completed: bool
    ) -> StepsCompleted:
        step = await self.prisma.stepscompleted.update(
            where={
                "id": step_id,
                "userproject": {"projectId": project_id, "userId": user_id},
            },
            data={"completed": completed},
            include={"steps": {"include": {"stepbreakdown": True}}},
        )

        return StepsCompleted.model_validate(
            {
                **step.steps.model_dump(mode="python"),
                "completed": step.model_dump(mode="python")["completed"],
            }
        )

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
