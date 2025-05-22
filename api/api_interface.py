"""
API interface for the Cartouche Bot Service.
Handles API key verification and other API-related utilities.
"""
import logging
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from config import settings

logger = logging.getLogger(__name__)

security_scheme = HTTPBearer()

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> str:
    """
    Verify the API key from the Authorization header using FastAPI's HTTPBearer.
    
    Args:
        credentials: HTTPAuthorizationCredentials object
        
    Returns:
        API key if valid
        
    Raises:
        HTTPException: If API key is invalid
    """
    if not credentials or not credentials.credentials:
        logger.warning("Missing Authorization header")
        raise HTTPException(status_code=401, detail="Missing API key")

    api_key = credentials.credentials

    if api_key != settings.MAIN_APP_API_KEY and settings.MAIN_APP_API_KEY:
        logger.warning("Invalid API key")
        raise HTTPException(status_code=401, detail="Invalid API key")

    return api_key
