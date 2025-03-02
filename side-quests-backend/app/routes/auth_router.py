from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.db.prisma_connection import get_prisma
from app.services.user import UserService
from app.utils.security import (
    verify_password,
    create_access_token,
)
from prisma import Prisma

router = APIRouter(tags=["Auth"])

async def get_user_service(db: Prisma = Depends(get_prisma)) -> UserService:
    return UserService(db)


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(
        data={"sub": str(user.id)},
    )
    return {"access_token": access_token, "token_type": "bearer"}
