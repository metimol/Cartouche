"""
API client for the Cartouche C# REST API.
Handles communication with the main C# backend.
"""

import logging
import aiohttp
import json
from typing import Dict, List, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.settings import SOCIAL_NETWORK_URL, API_KEY
from app.core.exceptions import APIError
from app.utils.json_to_string import JSONToStringConverter

from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()


class CartoucheAPIClient:
    """Client for interacting with the Cartouche C# REST API."""

    def __init__(self, base_url: str = SOCIAL_NETWORK_URL, token: str = API_KEY):
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
    async def get_posts(self, post_id: Optional[int] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get posts from the API.

        Args:
            post_id: Optional post ID to get a specific post
            limit: Limit for number of posts when getting all posts (default: 50)

        Returns:
            List of post dictionaries
        """
        if post_id:
            # Get specific post
            endpoint = f"/api/posts/{post_id}"
            url = f"{self.base_url}/{endpoint}"
        else:
            # Get all posts with caching and limit
            endpoint = "/api/posts"
            url = f"{self.base_url}/{endpoint}?limit={limit}"

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            headers = {"X-API-KEY": self.token}
            async with self.session.get(url, headers=headers) as response:
                response_text = await response.text()
                if response.status == 200:
                    try:
                        data = json.loads(response_text)
                        return data if isinstance(data, list) else [data]
                    except Exception as e:
                        logger.error(
                            f"[API][GET_POSTS] JSON decode error: {e}, Raw: {response_text}"
                        )
                        raise APIError(f"Failed to decode JSON: {response_text}")
                else:
                    logger.error(
                        f"[API][GET_POSTS] Error: {response.status} - {response_text}"
                    )
                    raise APIError(
                        f"Failed to get posts: {response_text}", response.status
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Error in get_posts: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

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

        # Convert bot data to API format
        formatted_data = JSONToStringConverter.format_bot_data(bot_data)

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            headers = {"Content-Type": "text/plain; charset=utf-8"}
            async with self.session.post(
                url, data=formatted_data, headers=headers
            ) as response:
                response_text = await response.text()
                if response.status == 200:
                    return {"status": "success"}
                else:
                    logger.error(
                        f"[API][ADD_BOT] Error: {response.status} - {response_text}"
                    )
                    raise APIError(
                        f"Failed to add bot: {response_text}", response.status
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Error in add_bot: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

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

        # Convert post data to API format
        formatted_data = JSONToStringConverter.format_post_data(post_data)

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            headers = {"Content-Type": "text/plain; charset=utf-8"}
            async with self.session.post(
                url, data=formatted_data, headers=headers
            ) as response:
                response_text = await response.text()
                if response.status == 200:
                    try:
                        return json.loads(response_text)
                    except Exception as e:
                        logger.error(
                            f"[API][ADD_POST] JSON decode error: {e}, Raw: {response_text}"
                        )
                        raise APIError(f"Failed to decode JSON: {response_text}")
                else:
                    logger.error(
                        f"[API][ADD_POST] Error: {response.status} - {response_text}"
                    )
                    raise APIError(
                        f"Failed to add post: {response_text}", response.status
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Error in add_post: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

    async def like_post(self, post_id: int, bot_name: str) -> Dict[str, Any]:
        """
        Like a post.

        Args:
            post_id: Post ID
            bot_name: Bot name

        Returns:
            Response status
        """
        endpoint = f"UpdateDocument/Posts/{post_id}"
        url = f"{self.base_url}/{endpoint}?token={self.token}"

        # Convert like data to API format
        formatted_data = JSONToStringConverter.format_like_data(bot_name)

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            headers = {"Content-Type": "text/plain; charset=utf-8"}
            async with self.session.post(
                url, data=formatted_data, headers=headers
            ) as response:
                response_text = await response.text()
                if response.status == 200:
                    return {"status": "success"}
                else:
                    logger.error(
                        f"[API][LIKE_POST] Error: {response.status} - {response_text}"
                    )
                    raise APIError(
                        f"Failed to like post: {response_text}", response.status
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Error in like_post: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

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

        # Convert comment data to API format
        formatted_data = JSONToStringConverter.format_comment_data(comment_data)

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            headers = {"Content-Type": "text/plain; charset=utf-8"}
            async with self.session.post(
                url, data=formatted_data, headers=headers
            ) as response:
                response_text = await response.text()
                if response.status == 200:
                    return {"status": "success"}
                else:
                    logger.error(
                        f"[API][ADD_COMMENT] Error: {response.status} - {response_text}"
                    )
                    raise APIError(
                        f"Failed to add comment: {response_text}", response.status
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Error in add_comment: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None

    async def follow_user(self, user_name: str, bot_name: str) -> Dict[str, Any]:
        """
        Subscribe (follow) a user as a bot.

        Args:
            user_name: Name of the user to follow
            bot_name: Name of the bot who follows

        Returns:
            Response data
        """
        # Build the endpoint and query
        endpoint = "UpdateDocument/Users"
        query = json.dumps({"Name": user_name})
        url = f"{self.base_url}/{endpoint}/?query={query}&token={self.token}"

        # Prepare request body
        formatted_data = JSONToStringConverter.format_follow_data(bot_name)

        if not self.session:
            self.session = aiohttp.ClientSession()
            need_to_close = True
        else:
            need_to_close = False

        try:
            headers = {"Content-Type": "text/plain; charset=utf-8"}
            async with self.session.post(
                url, data=formatted_data, headers=headers
            ) as response:
                response_text = await response.text()
                if response.status == 200:
                    return {"status": "success"}
                else:
                    logger.error(
                        f"[API][FOLLOW_USER] Error: {response.status} - {response_text}"
                    )
                    raise APIError(
                        f"Failed to follow user: {response_text}", response.status
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Error in follow_user: {str(e)}")
            raise APIError(f"API client error: {str(e)}")

        finally:
            if need_to_close and self.session:
                await self.session.close()
                self.session = None