from typing import List
from fastapi import APIRouter, HTTPException, Depends
from prisma import Prisma
from app.models.category import Category, CategoryUpdate
from app.services.category import CategoryService
from app.db.prisma_connection import get_prisma

router = APIRouter(prefix="/categories", tags=["Categories"])


def get_category_service(prisma: Prisma = Depends(get_prisma)):
    """
    Dependency injection function to get a CategoryService instance.

    :param prisma: A Prisma client instance.
    :return: A CategoryService instance.
    """

    return CategoryService(prisma)


@router.get("/", status_code=200, response_model=List[Category])
async def get_categories(service: CategoryService = Depends(get_category_service)):
    return await service.get_categories()


@router.get("/{id}", status_code=200, response_model=Category)
async def get_category(
    id: int, service: CategoryService = Depends(get_category_service)
):
    return await service.get_category_by_id(id)


@router.post("/", status_code=201, response_model=Category)
async def create_category(
    category: CategoryUpdate, service: CategoryService = Depends(get_category_service)
):
    return await service.insert_category(category)


@router.put("/{id}", status_code=200, response_model=Category)
async def update_category(
    id: int,
    category: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
):
    return await service.update_category(id, category)


@router.delete("/{id}", status_code=200, response_model=Category)
async def delete_category(
    id: int, service: CategoryService = Depends(get_category_service)
):
    return await service.delete_category(id)


@router.delete("/", status_code=200)
async def delete_categories(service: CategoryService = Depends(get_category_service)):
    return await service.delete_categories()
