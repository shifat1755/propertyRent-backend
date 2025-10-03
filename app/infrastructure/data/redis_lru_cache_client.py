import os

from redis.asyncio import Redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
# DB 1 → LRU cache
redis_lru_cache = Redis.from_url(f"{REDIS_URL}/1", decode_responses=True)
