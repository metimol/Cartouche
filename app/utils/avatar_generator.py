"""
Avatar generator utility for the Cartouche Bot Service.
Handles generation of bot avatars.
"""

import uuid
from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()


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
        url = f"https://api.dicebear.com/9.x/{style}/png?seed={seed}"

        return url
