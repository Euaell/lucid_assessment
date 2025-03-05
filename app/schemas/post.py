from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    """
    Base schema for post data.
    
    Attributes:
        text (str): Content of the post.
    """
    text: str = Field(..., min_length=1, max_length=1000000, description="Post content")
    
    @validator('text')
    def text_must_not_be_empty(cls, v):
        """Validate that text is not empty."""
        if not v.strip():
            raise ValueError('Post text cannot be empty')
        return v

class PostCreate(PostBase):
    """
    Schema for post creation.
    
    Attributes:
        text (str): Content of the post.
    """
    pass

class PostInDBBase(PostBase):
    """
    Base schema for post stored in database.
    
    Attributes:
        id (int): Post ID.
        user_id (int): ID of the user who created the post.
        created_at (datetime): Creation timestamp.
    """
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Post(PostInDBBase):
    """
    Schema for post response.
    
    This is the schema returned to clients.
    """
    pass

class PostDelete(BaseModel):
    """
    Schema for post deletion.
    
    Attributes:
        post_id (int): ID of the post to delete.
    """
    post_id: int = Field(..., description="ID of the post to delete") 