from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.data.models.user_model import User
from app.presentation.schemas.user_schema import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # Create user
    async def create_user(self, user: UserCreate, hashed_password: str) -> User:
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
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        res = await self.db.execute(stmt)
        return res.scalars().first()

    # List users with optional limit/offset
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        stmt = select(User).offset(skip).limit(limit)
        res = await self.db.execute(stmt)
        return res.scalars().all()

    # Delete user
    async def delete_user(self, db_user: User) -> None:
        await self.db.delete(db_user)

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        return result.scalars().first()
