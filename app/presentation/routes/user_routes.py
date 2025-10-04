import json
import logging

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.application.usecases.user_usecase import UserUsecase
from app.domain.errors import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
    UserNotFoundError,
    WrongCredentials,
)
from app.infrastructure.data.database import get_db
from app.presentation.routes.dependencies import get_current_user
from app.presentation.schemas.user_schema import (
    UserCreate,
    UserCredentials,
    UserList,
    UserRead,
    UserUpdate,
    loginresponse,
)

logger = logging.getLogger(__name__)
userRouter = APIRouter()


@userRouter.post("/users/login", response_model=loginresponse)
async def login_user(
    credential: UserCredentials, response: Response, db: Session = Depends(get_db)
):
    usecase = UserUsecase(db=db)
    try:
        login_data = await usecase.login(user_cred=credential)

        # Set refresh token in HttpOnly cookie
        cookie_value = json.dumps(
            {
                "refresh_token": login_data.refresh_token,
                "session_id": login_data.session_id,
            }
        )
        response.set_cookie(
            key="refresh_token",
            value=cookie_value,
            httponly=True,
            secure=True,
            samesite="Strict",
            path="/auth/refresh",
        )
        # Return access token, session_id, user info in JSON
        return {
            "access_token": login_data.access_token,
            "user": login_data.user,
        }
    except WrongCredentials:
        raise HTTPException(status_code=401, detail="Credentials mismatch")
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception:
        logger.exception("Error during login")
        raise HTTPException(status_code=500, detail="Internal server error")


# Create user
@userRouter.post("/users/signup", response_model=UserRead)
async def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
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
async def get_user(
    user_id: int, db: Session = Depends(get_db), sender=Depends(get_current_user)
):
    usecase = UserUsecase(db)
    user = await usecase.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


# List users
@userRouter.get("/users/", response_model=UserList)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # sender=Depends(get_current_user),
):
    if skip < 0 or limit <= 0:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters")
    usecase = UserUsecase(db)
    users = await usecase.list_users(skip, limit)
    return UserList(users=[UserRead.model_validate(u) for u in users], total=len(users))


# Update user
@userRouter.patch("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    sender=Depends(get_current_user),
):
    usecase = UserUsecase(db)
    try:
        user = await usecase.update_user_by_id(user_id, user_update)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Email already exists")
    except UsernameAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception:
        logger.exception("Error updating user")
        raise HTTPException(status_code=500, detail="Internal server error")
    return UserRead.model_validate(user)


# Delete user
@userRouter.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: int, db: Session = Depends(get_db), sender=Depends(get_current_user)
):
    usecase = UserUsecase(db)
    try:
        await usecase.delete_user(user_id)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception:
        logger.exception("Error deleting user")
        raise HTTPException(status_code=500, detail="Internal server error")
    return
