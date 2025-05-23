"""
Test helper for the Cartouche Bot Service.
Mocks API responses for testing.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from unittest.mock import AsyncMock, MagicMock

logger = logging.getLogger(__name__)


class MockCartoucheAPIClient:
    """Mock client for testing the Cartouche API integration."""

    def __init__(self):
        """Initialize the mock client."""
        self.posts = [
            {
                "id": "1",
                "name": "test_user",
                "fullName": "Test User",
                "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=test_user",
                "text": "This is a test post",
                "likes": [],
                "comments": [],
                "onDate": "2025-05-22T12:00:00Z",
            },
            {
                "id": "2",
                "name": "bot_user",
                "fullName": "Bot User",
                "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=bot_user",
                "text": "This is a bot post",
                "likes": [],
                "comments": [],
                "onDate": "2025-05-22T12:30:00Z",
            },
        ]

        self.users = [
            {
                "name": "test_user",
                "fullName": "Test User",
                "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=test_user",
                "isBot": False,
                "description": "Real user for testing",
            },
            {
                "name": "bot_user",
                "fullName": "Bot User",
                "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=bot_user",
                "isBot": True,
                "description": "Bot user for testing",
            },
        ]

    async def __aenter__(self):
        """Enter context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        pass

    async def get_posts(self, post_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Mock getting posts from the API.

        Args:
            post_id: Optional post ID to get a specific post

        Returns:
            List of post dictionaries
        """
        logger.info(f"Mock API: Getting posts (post_id={post_id})")

        if post_id:
            for post in self.posts:
                if post["id"] == str(post_id):
                    return [post]
            return []

        return self.posts

    async def get_users(self, is_bot: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Mock getting users from the API.

        Args:
            is_bot: Optional filter to get only bots or only real users

        Returns:
            List of user dictionaries
        """
        logger.info(f"Mock API: Getting users (is_bot={is_bot})")

        if is_bot is not None:
            return [user for user in self.users if user["isBot"] == is_bot]

        return self.users

    async def add_bot(self, bot_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mock adding a new bot to the system.

        Args:
            bot_data: Bot data dictionary

        Returns:
            Response data
        """
        logger.info(f"Mock API: Adding bot {bot_data.get('name', 'unknown')}")

        # Add bot to users list
        bot_data["isBot"] = True
        self.users.append(bot_data)

        return {
            "success": True,
            "id": str(len(self.users)),
            "name": bot_data.get("name", "unknown"),
        }

    async def add_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mock adding a new post to the system.

        Args:
            post_data: Post data dictionary

        Returns:
            Response data
        """
        logger.info(f"Mock API: Adding post from {post_data.get('name', 'unknown')}")

        # Add post to posts list
        post_id = str(len(self.posts) + 1)
        post_data["id"] = post_id
        post_data["likes"] = []
        post_data["comments"] = []
        self.posts.append(post_data)

        return {"success": True, "id": post_id, "post": post_data}

    async def like_post(self, post_id: int, bot_name: str) -> Dict[str, Any]:
        """
        Mock liking a post.

        Args:
            post_id: Post ID
            bot_name: Bot name

        Returns:
            Response data
        """
        logger.info(f"Mock API: Bot {bot_name} liking post {post_id}")

        for post in self.posts:
            if post["id"] == str(post_id):
                if bot_name not in post["likes"]:
                    post["likes"].append(bot_name)
                return {"success": True, "id": post_id, "likes": post["likes"]}

        return {"success": False, "error": "Post not found"}

    async def add_comment(
        self, post_id: int, comment_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Mock adding a comment to a post.

        Args:
            post_id: Post ID
            comment_data: Comment data dictionary

        Returns:
            Response data
        """
        logger.info(f"Mock API: Adding comment to post {post_id}")

        for post in self.posts:
            if post["id"] == str(post_id):
                post["comments"].append(comment_data)
                return {"success": True, "id": post_id, "comments": post["comments"]}

        return {"success": False, "error": "Post not found"}
