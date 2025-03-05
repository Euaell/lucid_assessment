import time
from typing import Dict, Any, Tuple, Optional
from app.core.config import settings

# Simple in-memory cache implementation
# Structure: {key: (data, expiry_timestamp)}
cache: Dict[str, Tuple[Any, float]] = {}

def get_cache(key: str) -> Optional[Any]:
    """
    Retrieve data from cache if it exists and hasn't expired.
    
    Args:
        key (str): The cache key to retrieve.
        
    Returns:
        Optional[Any]: The cached data if found and valid, None otherwise.
    """
    if key in cache:
        data, expiry = cache[key]
        if time.time() < expiry:
            return data
        else:
            # Remove expired cache entry
            del cache[key]
    return None

def set_cache(key: str, data: Any, expiry_seconds: int = None) -> None:
    """
    Store data in the cache with an expiration time.
    
    Args:
        key (str): The cache key to store data under.
        data (Any): The data to cache.
        expiry_seconds (int, optional): Time in seconds until the cache expires.
                                       Defaults to the application setting.
    """
    if expiry_seconds is None:
        expiry_seconds = settings.CACHE_EXPIRATION_SECONDS
        
    expiry = time.time() + expiry_seconds
    cache[key] = (data, expiry)

def clear_cache(key: str = None) -> None:
    """
    Clear cache entries.
    
    Args:
        key (str, optional): Specific key to clear. If None, clears all cache.
    """
    if key:
        if key in cache:
            del cache[key]
    else:
        cache.clear() 