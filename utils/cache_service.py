"""
Cache service for the Cartouche Bot Service.
Handles caching of frequently used data.
"""
import logging
import json
import os
import time
from typing import Dict, Any, Optional, Union, List
from datetime import datetime, timedelta

from config import settings

logger = logging.getLogger(__name__)

class CacheService:
    """Service for caching frequently used data."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize the cache service.
        
        Args:
            cache_dir: Directory for cache files. If not provided, uses the one from settings.
        """
        self.cache_dir = cache_dir or settings.CACHE_DIR
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """Ensure the cache directory exists."""
        try:
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir)
                logger.info(f"Created cache directory: {self.cache_dir}")
        except Exception as e:
            logger.error(f"Error creating cache directory: {str(e)}")
    
    def get(self, key: str, default: Any = None, max_age: Optional[int] = None) -> Any:
        """
        Get a value from the cache.
        
        Args:
            key: Cache key
            default: Default value if key not found
            max_age: Maximum age in seconds
            
        Returns:
            Cached value or default
        """
        try:
            cache_file = os.path.join(self.cache_dir, f"{key}.json")
            
            if not os.path.exists(cache_file):
                return default
            
            # Check if cache is expired
            if max_age is not None:
                file_mtime = os.path.getmtime(cache_file)
                if time.time() - file_mtime > max_age:
                    logger.debug(f"Cache expired for key: {key}")
                    return default
            
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        except Exception as e:
            logger.error(f"Error getting cache for key {key}: {str(e)}")
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            
        Returns:
            Boolean indicating success
        """
        try:
            cache_file = os.path.join(self.cache_dir, f"{key}.json")
            
            with open(cache_file, 'w') as f:
                json.dump(value, f)
            
            logger.debug(f"Cache set for key: {key}")
            return True
        
        except Exception as e:
            logger.error(f"Error setting cache for key {key}: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Boolean indicating success
        """
        try:
            cache_file = os.path.join(self.cache_dir, f"{key}.json")
            
            if os.path.exists(cache_file):
                os.remove(cache_file)
                logger.debug(f"Cache deleted for key: {key}")
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"Error deleting cache for key {key}: {str(e)}")
            return False
    
    def clear(self) -> bool:
        """
        Clear all cache.
        
        Returns:
            Boolean indicating success
        """
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    os.remove(os.path.join(self.cache_dir, filename))
            
            logger.info("Cache cleared")
            return True
        
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            return False
    
    def clear_expired(self, max_age: int) -> int:
        """
        Clear expired cache entries.
        
        Args:
            max_age: Maximum age in seconds
            
        Returns:
            Number of entries cleared
        """
        try:
            count = 0
            current_time = time.time()
            
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.cache_dir, filename)
                    file_mtime = os.path.getmtime(file_path)
                    
                    if current_time - file_mtime > max_age:
                        os.remove(file_path)
                        count += 1
            
            logger.info(f"Cleared {count} expired cache entries")
            return count
        
        except Exception as e:
            logger.error(f"Error clearing expired cache: {str(e)}")
            return 0
