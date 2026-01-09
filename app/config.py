import os

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class DatabaseConfig:
    """Database-related configuration."""

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")

    @classmethod
    def get_url(cls):
        if not all([cls.DB_USER, cls.DB_NAME]):
            raise ValueError("Database username or DB_NAME is not set in .env")

        if cls.DB_PASSWORD:
            auth_part = f"{cls.DB_USER}:{cls.DB_PASSWORD}"
        else:
            auth_part = cls.DB_USER

        return f"postgresql+asyncpg://{auth_part}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"


class JWTConfig:
    """JWT-related configuration."""

    SECRET_KEY = os.getenv("JWT_SECRET")
    ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_EXPIRE_MINUTES", 15))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_EXPIRE_DAYS", 7))


class RedisConfig:
    """Redis-related configuration."""

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB_TOKENS = int(os.getenv("REDIS_DB_REFRESH_TOKENS", 0))
    REDIS_DB_CACHE = int(os.getenv("REDIS_DB_LRU_CACHE", 1))

    @classmethod
    def get_tokens_url(cls) -> str:
        return f"redis://{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB_TOKENS}"

    @classmethod
    def get_cache_url(cls) -> str:
        return f"redis://{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB_CACHE}"


class ElasticsearchConfig:
    """Elasticsearch-related configuration."""

    HOST = os.getenv("ELASTIC_HOST", "es01")
    PORT = os.getenv("ES_PORT", os.getenv("ELASTIC_PORT", "9200"))
    SCHEME = os.getenv("ELASTIC_SCHEME", "https")
    USERNAME = os.getenv("ELASTIC_USERNAME", os.getenv("ELASTIC_USER", "elastic"))
    PASSWORD = os.getenv("ELASTIC_PASSWORD")
    VERIFY_CERTS = os.getenv("ELASTIC_VERIFY_CERTS", "true").lower() == "true"
    CA_CERT_PATH = os.getenv("ELASTIC_CA_CERT")
    PROPERTY_INDEX = os.getenv("ELASTIC_PROPERTY_INDEX", "properties")
    REQUEST_TIMEOUT = float(os.getenv("ELASTIC_TIMEOUT", 10))

    @classmethod
    def get_url(cls) -> str:
        return f"{cls.SCHEME}://{cls.HOST}:{cls.PORT}"
