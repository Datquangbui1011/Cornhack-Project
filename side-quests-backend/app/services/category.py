import logging
from typing import Any, List, Optional
from fastapi import HTTPException
from pydantic import ValidationError
from app.db.prisma_connection import get_prisma
from prisma.errors import PrismaError
from prisma import Prisma
from app.models.category import Category, CategoryUpdate

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class CategoryService:
    """
    Service class for managing category operations.
    """

    def __init__(self, prisma_client: Prisma):
        """
        Initialize the CategoryService with a Prisma client.

        :param prisma_client: An instance of the Prisma client. If not provided,
                              get_prisma() will be used to obtain one.
        """
        self.prisma = prisma_client

    async def get_categories(self) -> List[Category]:
        """
        Retrieve all categories.

        :return: A list of category objects.
        :raises HTTPException: If fetching categories fails.
        """
        try:
            categories = await self.prisma.category.find_many()
            if not categories:
                return []
            return [
                Category.model_validate(category.model_dump(mode="python"))
                for category in categories
            ]
        except PrismaError as e:
            logger.error(f"Error fetching categories: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except ValidationError as e:
            logger.error(f"Error validating categories: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Error fetching categories: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def insert_category(self, category: Category) -> Category:

        try:
            category = await self.prisma.category.create(
                data=category.model_dump(mode="python")
            )
            return Category.model_validate(category.model_dump(mode="python"))
        except PrismaError as e:
            logger.error(f"Error inserting category: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except ValidationError as e:
            logger.error(f"Error validating category: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Error inserting category: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def get_category_by_id(self, id: int) -> Category:
        """
        Retrieve a category by its ID.

        :param id: The unique identifier of the category to retrieve.
        :return: The category object.
        :raises HTTPException: If the category is not found.
        """
        try:
            category = await self.prisma.category.find_unique(where={"id": id})
            if not category:
                logger.error("Category not found")
                raise HTTPException(status_code=404, detail="Category not found")
            return Category.model_validate(category.model_dump(mode="python"))
        except PrismaError as e:
            logger.error(f"Error fetching category: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except ValidationError as e:
            logger.error(f"Error validating category: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Error fetching category: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def update_category(self, id: int, category: CategoryUpdate) -> Category:
        """
        Update a category by its ID.

        :param id: The unique identifier of the category to update.
        :param category: A categoryUpdate instance with updated category data.
        :return: The updated category object.
        :raises HTTPException: If the category is not found or update fails.
        """

        try:
            category = await self.prisma.category.update(
                where={"id": id},
                data=category.model_dump(mode="python"),
            )
            if not category:
                logger.error("Category not found")
                raise HTTPException(status_code=404, detail="Category not found")
            return Category.model_validate(category.model_dump(mode="python"))
        except PrismaError as e:
            logger.error(f"Error updating category: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except ValidationError as e:
            logger.error(f"Error validating category: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Error updating category: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_categories(self) -> Any:
        """
        Delete all categories.

        :return: The deleted category object.
        :raises HTTPException: If deletion fails.
        """
        try:
            count = await self.prisma.category.delete_many()
            return {"message": f"Deleted {count} categories"}
        except PrismaError as e:
            logger.error(f"Error deleting categories: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except ValidationError as e:
            logger.error(f"Error validating categories: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Error deleting categories: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_category(self, id: int) -> Category:
        """
        Delete a category by its ID.

        :param id: The unique identifier of the category to delete.
        :return: The deleted category object.
        :raises HTTPException: If the category is not found or deletion fails.
        """
        try:
            category = await self.prisma.category.delete(where={"id": id})
            if not category:
                logger.error("Category not found")
                raise HTTPException(status_code=404, detail="Category not found")
            return category.model_validate(category.model_dump(mode="python"))
        except PrismaError as e:
            logger.error(f"Error deleting category: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except ValidationError as e:
            logger.error(f"Error validating category: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Error deleting category: {e}")
            raise HTTPException(status_code=500, detail=str(e))
