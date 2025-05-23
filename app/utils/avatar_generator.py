"""
Avatar generator utility for the Cartouche Bot Service.
Handles generation of bot avatars.
"""

import logging
import uuid

logger = logging.getLogger(__name__)


class AvatarGenerator:
    """Utility for generating bot avatars."""

    @staticmethod
    async def generate_dicebear_avatar(style: str) -> str:
        """
        Generate an avatar using DiceBear API.

        Args:
            style: Avatar style (e.g., 'avataaars', 'bottts', 'personas')

        Returns:
            URL to the generated avatar
        """

        # Generate random seed
        seed = uuid.uuid4()

        # Generate url for avatar
        url = f"https://api.dicebear.com/7.x/{style}/svg?seed={seed}"

        return url
