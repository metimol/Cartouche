"""
HTTP client utility for the Cartouche Bot Service.
Provides a wrapper around requests/aiohttp for making HTTP requests.
"""
import logging
import json
from typing import Dict, Any, Optional, Union, List
import aiohttp
import requests
from config import settings

logger = logging.getLogger(__name__)

class HttpClient:
    """HTTP client for making requests to external services."""
    
    def __init__(self, base_url: Optional[str] = None, headers: Optional[Dict[str, str]] = None):
        """
        Initialize the HTTP client.
        
        Args:
            base_url: Base URL for all requests
            headers: Default headers for all requests
        """
        self.base_url = base_url or settings.MAIN_APP_URL
        self.headers = headers or {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.MAIN_APP_API_KEY}"
        }
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Request headers
            
        Returns:
            Response data
        """
        try:
            url = self._build_url(endpoint)
            merged_headers = {**self.headers, **(headers or {})}
            
            response = requests.get(url, params=params, headers=merged_headers)
            response.raise_for_status()
            
            return response.json()
        
        except Exception as e:
            logger.error(f"Error making GET request to {endpoint}: {str(e)}")
            return {"error": str(e)}
    
    def post(self, endpoint: str, data: Dict[str, Any], 
             headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a POST request.
        
        Args:
            endpoint: API endpoint
            data: Request data
            headers: Request headers
            
        Returns:
            Response data
        """
        try:
            url = self._build_url(endpoint)
            merged_headers = {**self.headers, **(headers or {})}
            
            response = requests.post(url, json=data, headers=merged_headers)
            response.raise_for_status()
            
            return response.json()
        
        except Exception as e:
            logger.error(f"Error making POST request to {endpoint}: {str(e)}")
            return {"error": str(e)}
    
    def put(self, endpoint: str, data: Dict[str, Any], 
            headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a PUT request.
        
        Args:
            endpoint: API endpoint
            data: Request data
            headers: Request headers
            
        Returns:
            Response data
        """
        try:
            url = self._build_url(endpoint)
            merged_headers = {**self.headers, **(headers or {})}
            
            response = requests.put(url, json=data, headers=merged_headers)
            response.raise_for_status()
            
            return response.json()
        
        except Exception as e:
            logger.error(f"Error making PUT request to {endpoint}: {str(e)}")
            return {"error": str(e)}
    
    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a DELETE request.
        
        Args:
            endpoint: API endpoint
            headers: Request headers
            
        Returns:
            Response data
        """
        try:
            url = self._build_url(endpoint)
            merged_headers = {**self.headers, **(headers or {})}
            
            response = requests.delete(url, headers=merged_headers)
            response.raise_for_status()
            
            return response.json()
        
        except Exception as e:
            logger.error(f"Error making DELETE request to {endpoint}: {str(e)}")
            return {"error": str(e)}
    
    async def async_get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
                        headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make an asynchronous GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Request headers
            
        Returns:
            Response data
        """
        try:
            url = self._build_url(endpoint)
            merged_headers = {**self.headers, **(headers or {})}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=merged_headers) as response:
                    response.raise_for_status()
                    return await response.json()
        
        except Exception as e:
            logger.error(f"Error making async GET request to {endpoint}: {str(e)}")
            return {"error": str(e)}
    
    async def async_post(self, endpoint: str, data: Dict[str, Any], 
                         headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make an asynchronous POST request.
        
        Args:
            endpoint: API endpoint
            data: Request data
            headers: Request headers
            
        Returns:
            Response data
        """
        try:
            url = self._build_url(endpoint)
            merged_headers = {**self.headers, **(headers or {})}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, headers=merged_headers) as response:
                    response.raise_for_status()
                    return await response.json()
        
        except Exception as e:
            logger.error(f"Error making async POST request to {endpoint}: {str(e)}")
            return {"error": str(e)}
    
    def _build_url(self, endpoint: str) -> str:
        """
        Build a full URL from the endpoint.
        
        Args:
            endpoint: API endpoint
            
        Returns:
            Full URL
        """
        if endpoint.startswith(('http://', 'https://')):
            return endpoint
        
        # Remove leading slash if present
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        
        # Remove trailing slash from base URL if present
        base_url = self.base_url
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        
        return f"{base_url}/{endpoint}"
