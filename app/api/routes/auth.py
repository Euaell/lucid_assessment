from fastapi import APIRouter, Depends, status

from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token
from app.services.auth_service import AuthService
from app.api.dependencies.services import get_auth_service

router = APIRouter()


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Create a new user account.
    
    This endpoint creates a new user account with the provided email and password,
    and returns an access token for authentication.
    
    Args:
        user_data (UserCreate): User data including email and password.
        auth_service (AuthService): Authentication service dependency.
        
    Returns:
        Token: Access token for authentication.
    """
    return await auth_service.signup_user(user_data.email, user_data.password)


@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Log in to an existing user account.
    
    This endpoint authenticates a user with the provided email and password,
    and returns an access token for authentication.
    
    Args:
        user_data (UserLogin): User data including email and password.
        auth_service (AuthService): Authentication service dependency.
        
    Returns:
        Token: Access token for authentication.
    """
    return await auth_service.login_user(user_data.email, user_data.password)
