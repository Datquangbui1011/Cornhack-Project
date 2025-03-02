import logging
from typing import Any, List
from fastapi import HTTPException
from pydantic import ValidationError
from prisma.errors import PrismaError
from prisma import Prisma
from app.models.user import User, UserCreate, UserLogin, UserUpdate
from app.utils.decorators import handle_service_exceptions
from app.utils.security import hash_password

logger = logging.getLogger(__name__)


class UserService:
    """
    Service class for managing user operations.
    """

    def __init__(self, prisma_client: Prisma):
        self.prisma = prisma_client

    @handle_service_exceptions
    async def get_users(self) -> List[User]:
        users = await self.prisma.user.find_many()
        if not users:
            return []
        return [User.model_validate(user.model_dump(mode="python")) for user in users]

    @handle_service_exceptions
    async def get_user_by_email(self, email: str) -> UserLogin:
        user = await self.prisma.user.find_unique(where={"email": email})
        if not user:
            return None
        return UserLogin.model_validate(user.model_dump(mode="python"))

    @handle_service_exceptions
    async def get_user_by_id(self, id: int) -> User:
        user = await self.prisma.user.find_unique(where={"id": id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return User.model_validate(user.model_dump(mode="python"))

    @handle_service_exceptions
    async def create_user(self, user: UserCreate) -> User:
        user_exist = await self.get_user_by_email(user.email)

        if user_exist:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed = hash_password(user.password)
        data = user.model_dump(mode="python", exclude={"password"})
        data["hashed_password"] = hashed
        created = await self.prisma.user.create(data=data)
        return User.model_validate(created.model_dump(mode="python"))

    @handle_service_exceptions
    async def update_user(self, id: int, user: UserUpdate) -> User:
        update_data = user.model_dump(exclude_unset=True)
        # If a new password is provided, hash it and update the hashed_password field.
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = hash_password(update_data["password"])
            update_data.pop("password")
        updated = await self.prisma.user.update(where={"id": id}, data=update_data)
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")
        return User.model_validate(updated.model_dump(mode="python"))

    @handle_service_exceptions
    async def delete_user(self, id: int) -> User:
        user = await self.prisma.user.delete(where={"id": id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return User.model_validate(user.model_dump(mode="python"))
