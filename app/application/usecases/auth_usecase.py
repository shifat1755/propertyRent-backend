from sqlalchemy.orm import Session

from app.domain.errors import (
    UserNotFoundError,
    WrongCredentials,
)
from app.infrastructure.data.redis_refresh_token_client import RedisTokenService
from app.infrastructure.repositories.user_repo import UserRepository
from app.infrastructure.security.bcrypt_hasher import verify_password
from app.infrastructure.security.jwt import JWTHandler
from app.presentation.schemas.user_schema import (
    Login_data,
    UserCredentials,
)


class AuthUsecase:
    def __init__(self, db: Session):
        self.userRepo = UserRepository(db)
        self.redis_token_service = RedisTokenService()
        self.jwt_handler = JWTHandler()

    async def login(self, user_cred=UserCredentials) -> Login_data:
        db_user = await self.userRepo.get_user_by_email(user_cred.email)
        if not db_user:
            raise UserNotFoundError
        if not verify_password(user_cred.password, db_user.hashed_password):
            raise WrongCredentials
        accesstoken = self.jwt_handler.generate_access_token(
            subject=str(db_user.id),
            extra_claims={
                "role": str(db_user.role),
                "user_type": str(db_user.user_type),
            },
        )
        refreshtoken = self.jwt_handler.generate_refresh_token(
            subject=str(db_user.id),
            extra_claims={
                "role": str(db_user.role),
                "user_type": str(db_user.user_type),
            },
        )

        session_id = await self.redis_token_service.store(
            user_id=str(db_user.id), refresh_token=refreshtoken
        )

        return Login_data(
            access_token=accesstoken,
            refresh_token=refreshtoken,
            session_id=session_id,
            user=db_user,
        )

    async def logout(self, user_id: str, session_id: str) -> None:
        await self.redis_token_service.revoke(user_id=user_id, session_id=session_id)
        return
