import logging
from typing import Any, List
from fastapi import HTTPException
from pydantic import ValidationError
from prisma.errors import PrismaError
from prisma import Prisma
from app.models.category import Category, CategoryUpdate
from app.utils.decorators import handle_service_exceptions
from app.core.logging_config import logger

class CategoryService:
    """
    Service class for managing category operations.
    """

    def __init__(self, prisma_client: Prisma):
        self.prisma = prisma_client

    @handle_service_exceptions
    async def get_categories(self) -> List[Category]:
        categories = await self.prisma.category.find_many()
        if not categories:
            return []
        return [
            Category.model_validate(category.model_dump(mode="python"))
            for category in categories
        ]

    @handle_service_exceptions
    async def insert_category(self, category: Category) -> Category:
        created = await self.prisma.category.create(
            data=category.model_dump(mode="python")
        )
        return Category.model_validate(created.model_dump(mode="python"))

    @handle_service_exceptions
    async def get_category_by_id(self, id: int) -> Category:
        category = await self.prisma.category.find_unique(where={"id": id})
        if not category:
            logger.error("Category not found")
            raise HTTPException(status_code=404, detail="Category not found")
        return Category.model_validate(category.model_dump(mode="python"))

    @handle_service_exceptions
    async def update_category(self, id: int, category: CategoryUpdate) -> Category:
        updated = await self.prisma.category.update(
            where={"id": id}, data=category.model_dump(mode="python")
        )
        if not updated:
            logger.error("Category not found")
            raise HTTPException(status_code=404, detail="Category not found")
        return Category.model_validate(updated.model_dump(mode="python"))

    @handle_service_exceptions
    async def delete_categories(self) -> Any:
        count = await self.prisma.category.delete_many()
        return {"message": f"Deleted {count} categories"}

    @handle_service_exceptions
    async def delete_category(self, id: int) -> Category:
        category = await self.prisma.category.delete(where={"id": id})
        if not category:
            logger.error("Category not found")
            raise HTTPException(status_code=404, detail="Category not found")
        return Category.model_validate(category.model_dump(mode="python"))
