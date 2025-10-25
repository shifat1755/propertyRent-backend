from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.errors import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
    UserNotFoundError,
)
from app.infrastructure.data.models.user_model import User
from app.infrastructure.repositories.user_repo import UserRepository
from app.infrastructure.security.bcrypt_hasher import hash_password
from app.infrastructure.security.jwt import JWTHandler
from app.presentation.schemas.user_schema import (
    UserCreate,
    UserUpdate,
)


class UserUsecase:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        self.jwt_handler = JWTHandler()

    # Create
    async def create_user(self, user_create: UserCreate) -> User:
        if await self.repo.get_user_by_email(user_create.email):
            raise EmailAlreadyExistsError

        if await self.repo.get_user_by_username(user_create.username):
            raise UsernameAlreadyExistsError

        hashed_password = hash_password(user_create.password)
        try:
            return await self.repo.create_user(user_create, hashed_password)
        except Exception as e:
            raise e

    # Get single user
    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.repo.get_user_by_id(user_id)

    # List users
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self.repo.list_users(skip, limit)

    # Update
    async def update_user_by_id(self, id: int, user_update: UserUpdate) -> User:
        db_user = await self.get_user(id)
        if not db_user:
            raise UserNotFoundError

        if user_update.email and user_update.email != db_user.email:
            if await self.repo.get_user_by_email(user_update.email):
                raise EmailAlreadyExistsError

        if user_update.username and user_update.username != db_user.username:
            if await self.repo.get_user_by_username(user_update.username):
                raise UsernameAlreadyExistsError

        if user_update.password:
            user_update.password = hash_password(user_update.password)

        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)

        await self.repo.db.commit()
        await self.repo.db.refresh(db_user)
        return db_user

    # Delete
    async def delete_user(self, user_id: int) -> None:
        db_user = await self.repo.get_user_by_id(user_id)
        if not db_user:
            raise UserNotFoundError
        await self.repo.delete_user(db_user)
        await self.repo.db.commit()
        return
