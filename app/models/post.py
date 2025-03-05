from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base

class Post(Base):
    """
    SQLAlchemy Post model representing the posts table.
    
    Attributes:
        id (int): Primary key for the post.
        text (str): Content of the post.
        user_id (int): Foreign key to the user who created the post.
        created_at (DateTime): Timestamp when the post was created.
        user (relationship): Relationship to the user who created the post.
    """
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship with user
    user = relationship("User", back_populates="posts") 