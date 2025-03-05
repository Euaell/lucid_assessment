import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    
    Attributes:
        DATABASE_URL: Connection string for the MySQL database
        SECRET_KEY: Secret key for JWT token generation
        ALGORITHM: Algorithm used for JWT token encoding/decoding
        ACCESS_TOKEN_EXPIRE_MINUTES: Expiration time for access tokens in minutes
    """
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+aiomysql://user:password@localhost:3306/fastapi_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Cache settings
    CACHE_EXPIRATION_SECONDS: int = 300  # 5 minutes
    
    # Request size limits (1MB = 1048576 bytes)
    MAX_REQUEST_SIZE_BYTES: int = 1048576

settings = Settings() 