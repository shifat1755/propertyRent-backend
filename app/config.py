import os
from dotenv import load_dotenv

load_dotenv()  # load .env from root


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
