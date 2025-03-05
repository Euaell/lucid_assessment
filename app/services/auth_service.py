from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.token import Token

class AuthService:
    """
    Authentication service handling business logic for auth operations.
    
    This class handles user authentication, token generation, and related operations.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the service with a database session.
        
        Args:
            db (AsyncSession): SQLAlchemy async session for database operations.
        """
        self.db = db
        self.user_repository = UserRepository(db)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.
        
        Args:
            email (str): User's email.
            password (str): User's password.
            
        Returns:
            Optional[User]: Authenticated user if successful, None otherwise.
        """
        user = await self.user_repository.get_by_email(email)
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
            
        return user
    
    async def signup_user(self, email: str, password: str) -> Token:
        """
        Register a new user and generate an access token.
        
        Args:
            email (str): User's email.
            password (str): User's password.
            
        Returns:
            Token: Access token for the new user.
            
        Raises:
            HTTPException: If a user with the email already exists.
        """
        existing_user = await self.user_repository.get_by_email(email)
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
            
        user = await self.user_repository.create(email, password)
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=str(user.id), 
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token)
    
    async def login_user(self, email: str, password: str) -> Token:
        """
        Authenticate a user and generate an access token.
        
        Args:
            email (str): User's email.
            password (str): User's password.
            
        Returns:
            Token: Access token for the authenticated user.
            
        Raises:
            HTTPException: If authentication fails.
        """
        user = await self.authenticate_user(email, password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=str(user.id), 
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token) 