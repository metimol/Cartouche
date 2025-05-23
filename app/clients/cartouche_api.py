"""
API client for the Cartouche C# REST API.
Handles communication with the main C# backend.
"""

import logging
import aiohttp
import json
from typing import Dict, List, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.settings import API_BASE_URL, API_TOKEN
from app.core.exceptions import APIError

logger = logging.getLogger(__name__)


class CartoucheAPIClient:
    """Client for interacting with the Cartouche C# REST API."""

    def __init__(self, base_url: str = API_BASE_URL, token: str = API_TOKEN):
        """
        Initialize the API client.

        Args:
            base_url: Base URL for the API
            token: API token for authentication
        """
        self.base_url = base_url
        self.token = token
        self.session = None

    async def __aenter__(self):
        """Create session when entering context."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close session when exiting context."""
        if self.session:
            await self.session.close()
            self.session = None

    def _get_auth_params(self) -> Dict[str, str]:
        """Get authentication parameters for requests."""
        return {"token": self.token}

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def get_posts(self, post_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get posts from the API.

        Args:
            post_id: Optional post ID to get a specific post

        Returns:
            List of post dictionaries
        """
        endpoint = "GetDocuments/Posts"
        if post_id:
            endpoint += f"{post_id}/"

        url = f"{self.base_url}/{endpoint}?token={self.token}"

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data if isinstance(data, list) else [data]
                else:
                    error_text = await response.text()
                    logger.error(
                        f"Error getting posts: {response.status} - {error_text}"
                    )
                    raise APIError(
                        f"Failed to get posts: {error_text}", response.status
                    )

        except aiohttp.ClientError as e:
            logger.error(f"Error in get_posts: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def get_users(self, is_bot: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get users from the API.

        Args:
            is_bot: Optional filter to get only bots or only real users

        Returns:
            List of user dictionaries
        """
        endpoint = "GetDocuments/Users"
        url = f"{self.base_url}/{endpoint}?token={self.token}"

        if is_bot is not None:
            url += f"&query={json.dumps({'IsBot': is_bot})}"

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    error_text = await response.text()
                    logger.error(
                        f"Error getting users: {response.status} - {error_text}"
                    )
                    raise APIError(
                        f"Failed to get users: {error_text}", response.status
                    )

        except aiohttp.ClientError as e:
            logger.error(f"Error in get_users: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def add_bot(self, bot_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new bot to the system.

        Args:
            bot_data: Bot data dictionary

        Returns:
            Response data
        """
        endpoint = "AddDocument/Users"
        url = f"{self.base_url}/{endpoint}?token={self.token}"

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            async with self.session.post(url, json=bot_data) as response:
                if response.status == 200:
                    try:
                        return await response.json()
                    except Exception as e:
                        text = await response.text()
                        logger.error(f"Failed to decode JSON, got: {text}")
                        raise APIError(f"Failed to decode JSON: {text}")
                else:
                    error_text = await response.text()
                    logger.error(f"Error adding bot: {response.status} - {error_text}")
                    raise APIError(f"Failed to add bot: {error_text}", response.status)

        except aiohttp.ClientError as e:
            logger.error(f"Error in add_bot: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def add_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new post to the system.

        Args:
            post_data: Post data dictionary

        Returns:
            Response data
        """
        endpoint = "AddDocument/Posts"
        url = f"{self.base_url}/{endpoint}?token={self.token}"

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            async with self.session.post(
                url, params=params, json=post_data
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    logger.error(f"Error adding post: {response.status} - {error_text}")
                    raise APIError(f"Failed to add post: {error_text}", response.status)

        except aiohttp.ClientError as e:
            logger.error(f"Error in add_post: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def like_post(self, post_id: int, bot_name: str) -> Dict[str, Any]:
        """
        Like a post.

        Args:
            post_id: Post ID
            bot_name: Bot name

        Returns:
            Response data
        """
        endpoint = f"UpdateDocument/Posts/{post_id}"
        url = f"{self.base_url}/{endpoint}?token={self.token}"
        data = {"Likes": ["Add", bot_name]}

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            async with self.session.post(url, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    logger.error(f"Error liking post: {response.status} - {error_text}")
                    raise APIError(
                        f"Failed to like post: {error_text}", response.status
                    )

        except aiohttp.ClientError as e:
            logger.error(f"Error in like_post: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def add_comment(
        self, post_id: int, comment_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add a comment to a post.

        Args:
            post_id: Post ID
            comment_data: Comment data dictionary with keys: Name, FullName, Avatar, Text, OnDate

        Returns:
            Response data
        """
        endpoint = f"UpdateDocument/Posts/{post_id}"
        url = f"{self.base_url}/{endpoint}?token={self.token}"

        # Format comment data as a string
        comment_str = str(comment_data).replace("'", "'")
        data = {"Comments": ["Add", comment_str]}

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            async with self.session.post(url, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    logger.error(
                        f"Error adding comment: {response.status} - {error_text}"
                    )
                    raise APIError(
                        f"Failed to add comment: {error_text}", response.status
                    )

        except aiohttp.ClientError as e:
            logger.error(f"Error in add_comment: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None
