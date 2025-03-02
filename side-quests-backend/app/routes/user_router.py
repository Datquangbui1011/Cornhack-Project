from fastapi import APIRouter, Depends, HTTPException
from typing import List
from prisma import Prisma
from app.services.user import UserService
from app.models.user import User, UserCreate, UserUpdate
from app.db.prisma_connection import get_prisma

router = APIRouter(prefix="/users", tags=["Users"])

def get_user_service(prisma: Prisma = Depends(get_prisma)) -> UserService:
    return UserService(prisma)

@router.get("/", response_model=List[User])
async def read_users(service: UserService = Depends(get_user_service)):
    return await service.get_users()

@router.get("/{id}", response_model=User)
async def read_user(id: int, service: UserService = Depends(get_user_service)):
    return await service.get_user_by_id(id)

@router.post("/", response_model=User)
async def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.create_user(user)

@router.patch("/{id}", response_model=User)
async def update_user(id: int, user: UserUpdate, service: UserService = Depends(get_user_service)):
    return await service.update_user(id, user)

@router.delete("/{id}", response_model=User)
async def delete_user(id: int, service: UserService = Depends(get_user_service)):
    return await service.delete_user(id)
