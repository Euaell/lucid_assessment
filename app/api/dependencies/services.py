from app.services.post_service import PostService
from app.services.auth_service import AuthService
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_post_service(db: AsyncSession = Depends(get_db)) -> PostService:
    return PostService(db)


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)
