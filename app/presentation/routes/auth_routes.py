import logging

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.usecases.auth_usecase import AuthUsecase
from app.domain.errors import (
    UserNotFoundError,
    WrongCredentials,
)
from app.infrastructure.data.database import get_db
from app.presentation.routes.dependencies import get_current_user
from app.presentation.schemas.user_schema import (
    UserCredentials,
    loginresponse,
)

authRouter = APIRouter(prefix="/auth")

logger = logging.getLogger(__name__)


@authRouter.post("/login", response_model=loginresponse)
async def login_user(
    credential: UserCredentials, response: Response, db: AsyncSession = Depends(get_db)
):
    usecase = AuthUsecase(db=db)
    try:
        login_data = await usecase.login(user_cred=credential)

        # Set refresh token in HttpOnly cookie
        response.set_cookie(
            key="refresh_token",
            value=login_data.refresh_token,
            httponly=True,
            secure=True,
            samesite="Strict",
            path="/auth/refresh",
        )
        # Set session_id in HttpOnly cookie
        response.set_cookie(
            key="session_id",
            value=login_data.session_id,
            httponly=True,
            secure=True,
            samesite="Strict",
            path="/",
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


@authRouter.post("/logout")
async def logout_user(
    session_id: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
    sender=Depends(get_current_user),
):
    print("sender__", sender)
    if not session_id:
        raise HTTPException(status_code=401, detail="No session_id cookie found")

    usecase = AuthUsecase(db)
    try:
        await usecase.logout(sender["user_id"], session_id)
    except Exception:
        logger.exception("Error during logout")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {"detail": "Logged out successfully"}


# @authRouter.post("/refresh")
# async def refresh(response: Response, refresh_token: str | None = Cookie(default=None)):
#     if not refresh_token:
#         raise HTTPException(status_code=401, detail="No refresh token provided")

#     # verify and decode token
#     new_access, new_refresh = verify_and_refresh(refresh_token)

#     # set new refresh cookie
#     response.set_cookie(
#         key="refresh_token",
#         value=new_refresh,
#         httponly=True,
#         secure=True,
#         samesite="Strict",
#         path="/auth/refresh",
#     )

#     return {"access_token": new_access}
