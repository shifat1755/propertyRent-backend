import datetime
from typing import Optional

import jwt

from app.config import JWTConfig


class JWTHandler:
    def __init__(
        self,
        secret_key: Optional[str] = None,
        algorithm: Optional[str] = None,
        access_token_expire_minutes: Optional[int] = None,
    ):
        self.secret_key = secret_key or JWTConfig.SECRET_KEY
        self.algorithm = algorithm or JWTConfig.ALGORITHM
        self.access_token_expire_minutes = (
            access_token_expire_minutes or JWTConfig.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    def generate_access_token(
        self, subject: str, extra_claims: Optional[dict] = None
    ) -> str:
        """
        Generate a signed JWT access token.

        :param subject: Identifier for the token owner (e.g., user_id).
        :param extra_claims: Optional custom claims to include.
        :return: Encoded JWT string.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        expire = now + datetime.timedelta(minutes=self.access_token_expire_minutes)

        payload = {
            "sub": subject,
            "iat": now,
            "exp": expire,
            "type": "access",
        }

        if extra_claims:
            payload.update(extra_claims)

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def generate_refresh_token(
        self, subject: str, extra_claims: Optional[dict] = None
    ) -> str:
        """
        Generate a signed JWT refresh token.

        :param subject: Identifier for the token owner (e.g., user_id).
        :param extra_claims: Optional custom claims to include.
        :return: Encoded JWT string.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        expire = now + datetime.timedelta(days=JWTConfig.REFRESH_TOKEN_EXPIRE_DAYS)

        payload = {
            "sub": subject,
            "iat": now,
            "exp": expire,
            "type": "refresh",
        }

        if extra_claims:
            payload.update(extra_claims)

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def decode_token(self, token: str) -> Optional[dict]:
        """
        Verify and decode a JWT access token.

        :param token: The JWT string to validate.
        :return: Decoded payload if valid, None if invalid/expired.
        """
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return decoded
        except jwt.ExpiredSignatureError:
            # Token has expired
            return None
        except jwt.InvalidTokenError:
            # Signature failed or token malformed
            return None
