from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED, tags=["auth"])
async def signup(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new user account.
    
    This endpoint creates a new user account with the provided email and password,
    and returns an access token for authentication.
    
    Args:
        user_data (UserCreate): User data including email and password.
        db (AsyncSession): Database session dependency.
        
    Returns:
        Token: JWT access token for the new user.
    """
    auth_service = AuthService(db)
    return await auth_service.signup_user(user_data.email, user_data.password)

@router.post("/login", response_model=Token, tags=["auth"])
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Login a user.
    
    This endpoint authenticates a user with email and password,
    and returns an access token for authentication.
    
    Args:
        user_data (UserLogin): User credentials including email and password.
        db (AsyncSession): Database session dependency.
        
    Returns:
        Token: JWT access token for the authenticated user.
    """
    auth_service = AuthService(db)
    return await auth_service.login_user(user_data.email, user_data.password) 