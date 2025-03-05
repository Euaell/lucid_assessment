from typing import List, Dict
from fastapi import APIRouter, Depends, status

from app.core.security import get_current_user
from app.schemas.post import PostCreate, Post, PostDelete
from app.services.post_service import PostService
from app.models.user import User
from app.api.dependencies.request_validators import validate_request_size
from app.api.dependencies.services import get_post_service

router = APIRouter()


@router.post("/posts", response_model=Dict[str, int], status_code=status.HTTP_201_CREATED, tags=["posts"])
async def add_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
    _: None = Depends(validate_request_size)
):
    """
    Create a new post.
    
    This endpoint creates a new post with the provided text content,
    associating it with the authenticated user.
    
    Args:
        post_data (PostCreate): Post data including text content.
        current_user (User): Authenticated user from token dependency.
        db (AsyncSession): Database session dependency.
        _ (None): Request size validation dependency.
        
    Returns:
        Dict[str, int]: Dictionary with the post ID.
    """
    return await post_service.create_post(post_data.text, current_user)


@router.get("/posts", response_model=List[Post], tags=["posts"])
async def get_posts(
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
):
    """
    Get all posts for the authenticated user.
    
    This endpoint returns all posts associated with the authenticated user,
    with response caching for up to 5 minutes.
    
    Args:
        current_user (User): Authenticated user from token dependency.
        db (AsyncSession): Database session dependency.
        
    Returns:
        List[Post]: List of posts belonging to the user.
    """
    return await post_service.get_posts(current_user)


@router.delete("/posts", response_model=Dict[str, str], tags=["posts"])
async def delete_post(
    post_data: PostDelete,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
):
    """
    Delete a post.
    
    This endpoint deletes a post with the provided ID,
    after verifying that it belongs to the authenticated user.
    
    Args:
        post_data (PostDelete): Post deletion data including post ID.
        current_user (User): Authenticated user from token dependency.
        db (AsyncSession): Database session dependency.
        
    Returns:
        Dict[str, str]: Success message.
    """
    return await post_service.delete_post(post_data.post_id, current_user)
