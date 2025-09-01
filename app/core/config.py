from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database configuration
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str
    APP_PORT: int
    
    # Auth configuration
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # Pagination
    DEFAULT_PAGE: int
    DEFAULT_PAGE_SIZE: int
    MAX_PAGE_SIZE: int

    class Config:
        env_file = ".env"   # tells Pydantic to load from .env

# cache so it’s not re-created every time
@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
