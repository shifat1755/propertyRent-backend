import uuid

from redis.asyncio import Redis

from app.config import JWTConfig, RedisConfig


class RedisTokenService:
    def __init__(self, redis_url: str | None = None):
        self.redis: Redis = Redis.from_url(
            redis_url or RedisConfig.get_tokens_url(), decode_responses=True
        )

    async def store(
        self,
        user_id: str,
        refresh_token: str,
        ttl: int = 60 * 60 * 24 * JWTConfig.REFRESH_TOKEN_EXPIRE_DAYS,
    ) -> str:
        session_id = str(uuid.uuid4())
        key = f"{user_id}:{session_id}"
        await self.redis.setex(key, ttl, refresh_token)
        return session_id

    async def get(self, user_id: str, session_id: str) -> str | None:
        key = f"{user_id}:{session_id}"
        return await self.redis.get(key)

    async def revoke(self, user_id: str, session_id: str) -> None:
        key = f"{user_id}:{session_id}"
        await self.redis.delete(key)
