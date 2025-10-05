import enum
from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.infrastructure.data.database import Base


class UserType(enum.Enum):
    TENANT = "tenant"
    LANDLORD = "landlord"
    AGENT = "agent"
    ADMIN = "admin"


class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    username: Mapped[str | None] = mapped_column(
        String, unique=True, index=True, nullable=True
    )
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    # User type and role
    user_type: Mapped[UserType] = mapped_column(
        SqlEnum(
            UserType, name="usertype", values_callable=lambda x: [m.value for m in x]
        ),
        nullable=False,
    )
    role: Mapped[UserRole | None] = mapped_column(
        SqlEnum(
            UserRole, name="userrole", values_callable=lambda x: [m.value for m in x]
        ),
        nullable=True,
    )

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # Personal info
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str | None] = mapped_column(String, nullable=True)

    # Profile
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationship to properties
    properties: Mapped[List["PropertyModel"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan"
    )
