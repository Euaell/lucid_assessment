
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """
    Repository for User model database operations.
    
    This class handles all database interactions for the User model,
    following the repository pattern to separate business logic from data access.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with a database session.
        
        Args:
            db (AsyncSession): SQLAlchemy async session for database operations.
        """
        self.db = db
    
    async def create(self, email: str, password: str) -> User:
        """
        Create a new user in the database.
        
        Args:
            email (str): User's email address.
            password (str): User's password (will be hashed).
            
        Returns:
            User: The created user.
        """
        # Import here to avoid circular imports
        from app.core.security import get_password_hash
        
        hashed_password = get_password_hash(password)
        db_user = User(email=email, hashed_password=hashed_password)
        
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        
        return db_user
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            email (str): User's email address.
            
        Returns:
            Optional[User]: The user if found, None otherwise.
        """
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get a user by ID.
        
        Args:
            user_id (int): User's ID.
            
        Returns:
            Optional[User]: The user if found, None otherwise.
        """
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
