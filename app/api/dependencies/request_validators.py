from fastapi import Request, HTTPException, status
from app.core.config import settings

async def validate_request_size(request: Request):
    """
    Validate that the request payload doesn't exceed the maximum allowed size.
    
    This dependency checks the Content-Length header against the configured maximum size.
    
    Args:
        request (Request): FastAPI request object.
        
    Raises:
        HTTPException: If the request size exceeds the maximum allowed size.
    """
    content_length = request.headers.get("content-length")
    
    if content_length:
        size = int(content_length)
        if size > settings.MAX_REQUEST_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Request size too large. Maximum allowed size is {settings.MAX_REQUEST_SIZE_BYTES} bytes"
            ) 