from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.infrastructure.security.jwt import JWTHandler

# Create a reusable HTTPBearer security object
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Dependency to extract current user from Bearer token.
    Uses HTTPBearer to read the Authorization header.
    """
    token = credentials.credentials  # The actual JWT string

    jwt_handler = JWTHandler()
    payload = jwt_handler.decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization Needed",
        )

    return {
        "user_id": payload.get("sub"),
        "role": payload.get("roles", "user"),
        "user_type": payload.get("user_type", "tenant"),
    }
