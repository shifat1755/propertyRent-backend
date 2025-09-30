from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.infrastructure.data.models.user_model import UserRole, UserType


# --------------------------
# Base schemas
# --------------------------
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., max_length=50)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone: Optional[str] = Field(None, max_length=15)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None
    user_type: UserType
    role: UserRole = UserRole.USER

    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "email": "example@example.com",
                "username": "example_user",
                "first_name": "Rohim",
                "last_name": "Uddin",
                "phone": "1234567890",
                "bio": "This is an example bio.",
                "avatar_url": "https://example.com/avatar.png",
                "user_type": "tenant",
                "role": "user",
            }
        },
    )


# --------------------------
# Password mixin with validator
# --------------------------
class PasswordMixin(BaseModel):
    password: Optional[str] = Field(None, min_length=8, max_length=72)

    @field_validator("password")
    def strong_password(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v.encode("utf-8")) > 72:
            raise ValueError(
                "Password must be at most 72 bytes (avoid emojis or special Unicode)"
            )
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        if not any(not c.isalnum() for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


# --------------------------
# Input schemas
# --------------------------
class UserCreate(UserBase, PasswordMixin):
    password: str = Field(..., min_length=8, max_length=72)

    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "email": "example@example.com",
                "username": "example_user",
                "password": "StrongPass1!",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "1234567890",
                "bio": "This is an example bio.",
                "avatar_url": "https://example.com/avatar.png",
                "user_type": "tenant",
                "role": "user",
            }
        },
    )


class UserUpdate(PasswordMixin):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, max_length=50)
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    phone: Optional[str] = Field(None, max_length=15)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None
    user_type: Optional[UserType] = None
    role: Optional[UserRole] = None
    password: Optional[str] = None

    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "username": "new_username",
                "password": "NewStrongPass1!",
                "first_name": "Jane",
                "last_name": "Doe",
                "phone": "0987654321",
                "bio": "Updated bio",
                "avatar_url": "https://example.com/new_avatar.png",
                "user_type": "landlord",
                "role": "admin",
            }
        },
    )


# --------------------------
# Output / Response schemas
# --------------------------
class UserRead(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    last_login: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "example@example.com",
                "username": "example_user",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "1234567890",
                "bio": "This is an example bio.",
                "avatar_url": "https://example.com/avatar.png",
                "user_type": "tenant",
                "role": "user",
                "is_active": True,
                "is_verified": False,
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-02T12:00:00Z",
                "last_login": "2025-01-03T12:00:00Z",
            }
        },
    )


class UserList(BaseModel):
    users: List[UserRead]
    total: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "users": [
                    {
                        "id": 1,
                        "email": "example@example.com",
                        "username": "example_user",
                        "first_name": "John",
                        "last_name": "Doe",
                        "phone": "1234567890",
                        "bio": "This is an example bio.",
                        "avatar_url": "https://example.com/avatar.png",
                        "user_type": "tenant",
                        "role": "user",
                        "is_active": True,
                        "is_verified": False,
                        "created_at": "2025-01-01T12:00:00Z",
                        "updated_at": "2025-01-02T12:00:00Z",
                        "last_login": "2025-01-03T12:00:00Z",
                    }
                ],
                "total": 1,
            }
        }
    )
