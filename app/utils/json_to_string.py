"""
JSON to string converter for Cartouche C# API.
Handles special formatting requirements for API requests.
"""

import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class JSONToStringConverter:
    """Converter for JSON to special string format required by Cartouche C# API."""

    @staticmethod
    def convert_to_api_string(data: Dict[str, Any]) -> str:
        """
        Convert dictionary to API-compatible string format.

        Args:
            data: Dictionary to convert

        Returns:
            String formatted for API consumption

        Examples:
            Input: {"Comments": ["Add", {"Name": "Bot", "Text": "Hello"}]}
            Output: {"Comments": [Add, {"Name": "Bot", "Text": "Hello"}]}
        """
        try:
            logger.info(f"[JSON_TO_STRING][convert_to_api_string] Input: {data}")

            # Convert to JSON string first
            json_str = json.dumps(data, ensure_ascii=False, separators=(",", ": "))

            # Replace quoted "Add" with unquoted Add for special operations
            # This handles operations like Add, Remove, Update, Delete etc.
            special_operations = ["Add", "Remove", "Update", "Delete"]

            for operation in special_operations:
                # Replace "Add" with Add (remove quotes around operation names)
                json_str = json_str.replace(f'"{operation}"', operation)

            logger.info(f"[JSON_TO_STRING][convert_to_api_string] Output: {json_str}")

            return json_str

        except Exception as e:
            logger.error(f"Failed to convert data to API string: {str(e)}")
            raise ValueError(f"Failed to convert data to API string: {str(e)}")

    @staticmethod
    def format_comment_data(comment_data: Dict[str, Any]) -> str:
        """
        Format comment data for API consumption.

        Args:
            comment_data: Comment data dictionary

        Returns:
            Formatted string for API
        """
        try:
            logger.info(f"[JSON_TO_STRING][format_comment_data] Input: {comment_data}")

            # Insert the comment_data dict directly, not as a string
            data = {"Comments": ["Add", comment_data]}

            result = JSONToStringConverter.convert_to_api_string(data)

            logger.info(f"[JSON_TO_STRING][format_comment_data] Output: {result}")

            return result

        except Exception as e:
            logger.error(f"Failed to format comment data: {str(e)}")
            raise ValueError(f"Failed to format comment data: {str(e)}")

    @staticmethod
    def format_like_data(bot_name: str) -> str:
        """
        Format like data for API consumption.

        Args:
            bot_name: Name of the bot performing the like

        Returns:
            Formatted string for API
        """
        try:
            logger.info(f"[JSON_TO_STRING][format_like_data] Input: {bot_name}")

            data = {"Likes": ["Add", bot_name]}
            result = JSONToStringConverter.convert_to_api_string(data)

            logger.info(f"[JSON_TO_STRING][format_like_data] Output: {result}")

            return result

        except Exception as e:
            logger.error(f"Failed to format like data: {str(e)}")
            raise ValueError(f"Failed to format like data: {str(e)}")

    @staticmethod
    def format_post_data(post_data: Dict[str, Any]) -> str:
        """
        Format post data for API consumption.

        Args:
            post_data: Post data dictionary

        Returns:
            Formatted string for API
        """
        try:
            logger.info(f"[JSON_TO_STRING][format_post_data] Input: {post_data}")

            result = json.dumps(post_data, ensure_ascii=False, separators=(",", ": "))

            logger.info(f"[JSON_TO_STRING][format_post_data] Output: {result}")

            return result

        except Exception as e:
            logger.error(f"Failed to format post data: {str(e)}")
            raise ValueError(f"Failed to format post data: {str(e)}")

    @staticmethod
    def format_bot_data(bot_data: Dict[str, Any]) -> str:
        """
        Format bot data for API consumption.

        Args:
            bot_data: Bot data dictionary

        Returns:
            Formatted string for API
        """
        try:
            logger.info(f"[JSON_TO_STRING][format_bot_data] Input: {bot_data}")

            result = json.dumps(bot_data, ensure_ascii=False, separators=(",", ": "))

            logger.info(f"[JSON_TO_STRING][format_bot_data] Output: {result}")

            return result

        except Exception as e:
            logger.error(f"Failed to format bot data: {str(e)}")
            raise ValueError(f"Failed to format bot data: {str(e)}")

    @staticmethod
    def format_update_data(update_data: Dict[str, Any]) -> str:
        """
        Format update data for API consumption.
        Handles special operations like Add, Remove, Update.

        Args:
            update_data: Update data dictionary

        Returns:
            Formatted string for API
        """
        try:
            logger.info(f"[JSON_TO_STRING][format_update_data] Input: {update_data}")

            result = JSONToStringConverter.convert_to_api_string(update_data)

            logger.info(f"[JSON_TO_STRING][format_update_data] Output: {result}")

            return result

        except Exception as e:
            logger.error(f"Failed to format update data: {str(e)}")
            raise ValueError(f"Failed to format update data: {str(e)}")
