"""
JSON to string converter for Cartouche C# API.
Handles special formatting requirements for API requests.
"""

import json
from typing import Dict, Any
from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()


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
            # Convert to JSON string first
            json_str = json.dumps(data, ensure_ascii=False, separators=(",", ": "))

            # Replace quoted "Add" with unquoted Add for special operations
            # This handles operations like Add, Remove, Update, Delete etc.
            special_operations = ["Add", "Remove", "Update", "Delete"]

            for operation in special_operations:
                # Replace "Add" with Add (remove quotes around operation names)
                json_str = json_str.replace(f'"{operation}"', operation)

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
            # Insert the comment_data dict directly, not as a string
            data = {"Comments": ["Add", comment_data]}

            result = JSONToStringConverter.convert_to_api_string(data)

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
            data = {"Likes": ["Add", bot_name]}
            result = JSONToStringConverter.convert_to_api_string(data)

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
            result = json.dumps(post_data, ensure_ascii=False, separators=(",", ": "))

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
            result = json.dumps(bot_data, ensure_ascii=False, separators=(",", ": "))

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
            result = JSONToStringConverter.convert_to_api_string(update_data)

            return result

        except Exception as e:
            logger.error(f"Failed to format update data: {str(e)}")
            raise ValueError(f"Failed to format update data: {str(e)}")

    @staticmethod
    def format_follow_data(bot_name: str) -> str:
        """
        Format follow (subscribe) data for API consumption.

        Args:
            bot_name: Name of the bot who follows

        Returns:
            Formatted string for API
        """
        try:
            data = {"Following": ["Add", bot_name]}
            result = JSONToStringConverter.convert_to_api_string(data)
            return result
        except Exception as e:
            logger.error(f"Failed to format follow data: {str(e)}")
            raise ValueError(f"Failed to format follow data: {str(e)}")
