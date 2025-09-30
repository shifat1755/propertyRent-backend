from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.errors import EmailAlreadyExistsError, UsernameAlreadyExistsError
from app.infrastructure.data.models.user_model import User
from app.presentation.schemas.user_schema import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # Create user
    async def create_user(self, user: UserCreate, hashed_password: str) -> User:
        stmt = select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
        result = await self.db.execute(stmt)
        existingUser = result.scalars().first()
        if existingUser:
            if existingUser.email == user.email:
                raise EmailAlreadyExistsError
            elif existingUser.username == user.username:
                raise UsernameAlreadyExistsError

        else:
            db_user = User(
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                phone=user.phone,
                bio=user.bio,
                avatar_url=user.avatar_url,
                user_type=user.user_type,
                role=user.role,
                hashed_password=hashed_password,
            )

            try:
                self.db.add(db_user)
                await self.db.commit()
                await self.db.refresh(db_user)
                return db_user
            except Exception as e:
                self.db.rollback()
                raise e

    # Get by ID
    async def get_user(self, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        res = await self.db.execute(stmt)
        return res.scalars().first()

    # List users with optional limit/offset
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        stmt = select(User).offset(skip).limit(limit)
        res = await self.db.execute(stmt)
        return res.scalars().all()

    # Update user
    async def update_user(
        self,
        db_user: User,
        user_update: UserUpdate,
    ) -> User:
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    # Delete user
    async def delete_user(self, db_user: User) -> None:
        await self.db.delete(db_user)
        await self.db.commit()
