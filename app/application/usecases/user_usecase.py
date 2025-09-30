from typing import List, Optional

from sqlalchemy.orm import Session

from app.infrastructure.data.models.user_model import User
from app.infrastructure.repositories.user_repo import UserRepository
from app.infrastructure.security.bcrypt_hasher import hash_password
from app.presentation.schemas.user_schema import UserCreate, UserUpdate


class UserUsecase:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    # Create
    async def create_user(self, user_create: UserCreate) -> User:
        hashed_password = hash_password(user_create.password)
        try:
            return await self.repo.create_user(user_create, hashed_password)
        except Exception as e:
            raise e

    # Get single user
    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.repo.get_user(user_id)

    # List users
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self.repo.list_users(skip, limit)

    # Update
    async def update_user(self, db_user: User, user_update: UserUpdate) -> User:
        if user_update.password:
            user_update.password = hash_password(user_update.password)
        return await self.repo.update_user(db_user, user_update)

    # Delete
    async def delete_user(self, db_user: User) -> None:
        await self.repo.delete_user(db_user)
