from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime


class UserBase(BaseModel):
    """
    Base schema for user data.
    
    Attributes:
        email (EmailStr): User's email address.
    """
    email: EmailStr = Field(..., description="User email address")
    
    @validator('email')
    def email_must_be_valid(cls, v):
        """Validate email format."""
        # The EmailStr type already validates the email format
        return v


class UserCreate(UserBase):
    """
    Schema for user creation.
    
    Attributes:
        email (EmailStr): User's email address.
        password (str): User's password.
    """
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")
    
    @validator('password')
    def password_must_be_strong(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserLogin(UserBase):
    """
    Schema for user login.
    
    Attributes:
        email (EmailStr): User's email address.
        password (str): User's password.
    """
    password: str = Field(..., description="User password")


class UserInDBBase(UserBase):
    """
    Base schema for user stored in database.
    
    Attributes:
        id (int): User ID.
        created_at (datetime): Creation timestamp.
    """
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class User(UserInDBBase):
    """
    Schema for user response.
    
    This is the schema returned to clients, excluding sensitive data.
    """
    pass
 