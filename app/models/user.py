from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base

class User(Base):
    """
    SQLAlchemy User model representing the users table.
    
    Attributes:
        id (int): Primary key for the user.
        email (str): User's email address, must be unique.
        hashed_password (str): Hashed password for the user.
        created_at (DateTime): Timestamp when the user was created.
        posts (relationship): Relationship to the user's posts.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship with posts
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan") 