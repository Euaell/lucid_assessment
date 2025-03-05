from pydantic import BaseModel, Field
from typing import Optional

class Token(BaseModel):
    """
    Schema for token response.
    
    Attributes:
        access_token (str): JWT access token.
        token_type (str): Type of token, default is "bearer".
    """
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """
    Schema for token payload.
    
    Attributes:
        sub (str): Subject of the token (usually the user ID).
        exp (int): Expiration timestamp.
    """
    sub: Optional[str] = None
    exp: Optional[int] = None 