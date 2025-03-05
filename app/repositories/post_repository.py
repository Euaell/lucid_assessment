from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post

class PostRepository:
    """
    Repository for Post model database operations.
    
    This class handles all database interactions for the Post model,
    following the repository pattern to separate business logic from data access.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with a database session.
        
        Args:
            db (AsyncSession): SQLAlchemy async session for database operations.
        """
        self.db = db
    
    async def create(self, text: str, user_id: int) -> Post:
        """
        Create a new post in the database.
        
        Args:
            text (str): Post content.
            user_id (int): ID of the user creating the post.
            
        Returns:
            Post: The created post.
        """
        db_post = Post(text=text, user_id=user_id)
        
        self.db.add(db_post)
        await self.db.commit()
        await self.db.refresh(db_post)
        
        return db_post
    
    async def get_by_id(self, post_id: int) -> Optional[Post]:
        """
        Get a post by ID.
        
        Args:
            post_id (int): Post ID.
            
        Returns:
            Optional[Post]: The post if found, None otherwise.
        """
        query = select(Post).where(Post.id == post_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: int) -> List[Post]:
        """
        Get all posts for a user.
        
        Args:
            user_id (int): User ID.
            
        Returns:
            List[Post]: List of posts belonging to the user.
        """
        query = select(Post).where(Post.user_id == user_id).order_by(Post.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def delete(self, post_id: int, user_id: int) -> bool:
        """
        Delete a post.
        
        Args:
            post_id (int): ID of the post to delete.
            user_id (int): ID of the user who owns the post.
            
        Returns:
            bool: True if the post was deleted, False otherwise.
        """
        stmt = delete(Post).where(Post.id == post_id, Post.user_id == user_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.rowcount > 0 