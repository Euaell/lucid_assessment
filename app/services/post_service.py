from typing import List, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.post_repository import PostRepository
from app.core.cache import get_cache, set_cache, clear_cache
from app.models.post import Post
from app.models.user import User
from app.schemas.post import Post as PostSchema

class PostService:
    """
    Post service handling business logic for post operations.
    
    This class handles post creation, retrieval, and deletion operations.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the service with a database session.
        
        Args:
            db (AsyncSession): SQLAlchemy async session for database operations.
        """
        self.db = db
        self.repository = PostRepository(db)
    
    async def create_post(self, text: str, current_user: User) -> Dict[str, int]:
        """
        Create a new post.
        
        Args:
            text (str): Post content.
            current_user (User): The user creating the post.
            
        Returns:
            Dict[str, int]: Dictionary with the post ID.
        """
        post = await self.repository.create(text, current_user.id)
        
        # Clear cache for this user's posts
        clear_cache(f"user_posts_{current_user.id}")
        
        return {"post_id": post.id}
    
    async def get_posts(self, current_user: User) -> List[PostSchema]:
        """
        Get all posts for a user, with caching.
        
        Args:
            current_user (User): The user whose posts to retrieve.
            
        Returns:
            List[PostSchema]: List of posts belonging to the user.
        """
        # Check cache first
        cache_key = f"user_posts_{current_user.id}"
        cached_posts = get_cache(cache_key)
        
        if cached_posts is not None:
            return cached_posts
        
        # If not in cache, retrieve from database
        posts = await self.repository.get_by_user_id(current_user.id)
        
        # Convert to schema and cache
        post_schemas = [PostSchema.from_orm(post) for post in posts]
        set_cache(cache_key, post_schemas)
        
        return post_schemas
    
    async def delete_post(self, post_id: int, current_user: User) -> Dict[str, str]:
        """
        Delete a post.
        
        Args:
            post_id (int): ID of the post to delete.
            current_user (User): The user deleting the post.
            
        Returns:
            Dict[str, str]: Success message.
            
        Raises:
            HTTPException: If the post doesn't exist or doesn't belong to the user.
        """
        # First check if the post exists and belongs to the user
        post = await self.repository.get_by_id(post_id)
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
            
        if post.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this post"
            )
        
        # Delete the post
        deleted = await self.repository.delete(post_id, current_user.id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete post"
            )
        
        # Clear cache for this user's posts
        clear_cache(f"user_posts_{current_user.id}")
        
        return {"message": "Post deleted successfully"} 