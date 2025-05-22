"""
API interface for the Cartouche Bot Service.
Handles API key verification and other API-related utilities.
"""
import logging
from fastapi import HTTPException, Depends, Header
from typing import Optional

from config import settings

logger = logging.getLogger(__name__)

def verify_api_key(authorization: Optional[str] = Header(None)) -> str:
    """
    Verify the API key from the Authorization header.
    
    Args:
        authorization: Authorization header value
        
    Returns:
        API key if valid
        
    Raises:
        HTTPException: If API key is invalid
    """
    if not authorization:
        logger.warning("Missing Authorization header")
        raise HTTPException(status_code=401, detail="Missing API key")
    
    # Extract API key from Authorization header
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.warning("Invalid Authorization header format")
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    
    api_key = parts[1]
    
    # In a real implementation, this would validate against a database or secure storage
    # For now, we'll just check against the configured API key
    if api_key != settings.MAIN_APP_API_KEY and settings.MAIN_APP_API_KEY:
        logger.warning("Invalid API key")
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return api_key
