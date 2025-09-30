import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.application.usecases.user_usecase import UserUsecase
from app.domain.errors import EmailAlreadyExistsError, UsernameAlreadyExistsError
from app.infrastructure.data.database import get_db
from app.presentation.schemas.user_schema import (
    UserCreate,
    UserList,
    UserRead,
    UserUpdate,
)

logger = logging.getLogger(__name__)
userRouter = APIRouter()


# Create user
@userRouter.post("/users/", response_model=UserRead)
async def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    usecase = UserUsecase(db)
    usecase = UserUsecase(db)
    try:
        user = await usecase.create_user(user_create)
    except EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Email already exists")
    except UsernameAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception:
        logger.exception("Error creating user")
        raise HTTPException(status_code=500, detail="Internal server error")
    return UserRead.model_validate(user)


# Get user by ID
@userRouter.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    usecase = UserUsecase(db)
    user = await usecase.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


# List users
@userRouter.get("/users/", response_model=UserList)
async def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip < 0 or limit <= 0:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters")
    usecase = UserUsecase(db)
    users = await usecase.list_users(skip, limit)
    return UserList(users=[UserRead.model_validate(u) for u in users], total=len(users))


# Update user
@userRouter.patch("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)
):
    usecase = UserUsecase(db)
    db_user = await usecase.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await usecase.update_user(db_user, user_update)
    return UserRead.model_validate(updated_user)


# Delete user
@userRouter.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    usecase = UserUsecase(db)
    db_user = await usecase.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    await usecase.delete_user(db_user)
    return
