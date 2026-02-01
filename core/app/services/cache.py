"""
Caching service with Redis and in-memory fallback.
"""
import json
import time
from typing import Any, Optional
from functools import wraps

from flask import current_app


class CacheService:
    """Caching service with Redis primary and in-memory fallback."""
    
    _instance = None
    _redis_client = None
    _memory_cache = {}
    _memory_expiry = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def _get_redis(self):
        """Get Redis client, initializing if needed."""
        if self._redis_client is None:
            redis_url = current_app.config.get('REDIS_URL')
            if redis_url:
                try:
                    import redis
                    self._redis_client = redis.from_url(redis_url)
                    # Test connection
                    self._redis_client.ping()
                    current_app.logger.info("✓ Connected to Redis")
                except Exception as e:
                    current_app.logger.warning(f"Redis unavailable, using memory cache: {e}")
                    self._redis_client = False  # Mark as unavailable
        return self._redis_client if self._redis_client else None
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        redis_client = self._get_redis()
        
        if redis_client:
            try:
                value = redis_client.get(key)
                if value:
                    return json.loads(value)
            except Exception as e:
                current_app.logger.error(f"Redis get error: {e}")
        
        # Fallback to memory cache
        if key in self._memory_cache:
            if self._memory_expiry.get(key, 0) > time.time():
                return self._memory_cache[key]
            else:
                # Expired
                del self._memory_cache[key]
                del self._memory_expiry[key]
        
        return None
    
    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Set a value in cache with TTL (seconds)."""
        redis_client = self._get_redis()
        
        if redis_client:
            try:
                redis_client.setex(key, ttl, json.dumps(value))
                return True
            except Exception as e:
                current_app.logger.error(f"Redis set error: {e}")
        
        # Fallback to memory cache
        self._memory_cache[key] = value
        self._memory_expiry[key] = time.time() + ttl
        
        # Simple memory cleanup (remove expired entries if cache is large)
        if len(self._memory_cache) > 1000:
            self._cleanup_memory_cache()
        
        return True
    
    def delete(self, key: str) -> bool:
        """Delete a key from cache."""
        redis_client = self._get_redis()
        
        if redis_client:
            try:
                redis_client.delete(key)
            except Exception:
                pass
        
        # Also remove from memory cache
        self._memory_cache.pop(key, None)
        self._memory_expiry.pop(key, None)
        
        return True
    
    def _cleanup_memory_cache(self):
        """Remove expired entries from memory cache."""
        now = time.time()
        expired_keys = [k for k, exp in self._memory_expiry.items() if exp < now]
        for key in expired_keys:
            self._memory_cache.pop(key, None)
            self._memory_expiry.pop(key, None)


# Singleton instance
cache = CacheService()


def cached(ttl: int = 300, key_prefix: str = ''):
    """Decorator to cache function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Build cache key from function name and arguments
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator
