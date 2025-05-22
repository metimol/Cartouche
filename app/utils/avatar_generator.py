"""
Avatar generator utility for the Cartouche Bot Service.
Handles generation of bot avatars.
"""
import logging
import requests
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class AvatarGenerator:
    """Utility for generating bot avatars."""
    
    @staticmethod
    async def generate_dicebear_avatar(style: str, seed: str, output_path: Optional[str] = None) -> str:
        """
        Generate an avatar using DiceBear API.
        
        Args:
            style: Avatar style (e.g., 'avataaars', 'bottts', 'personas')
            seed: Seed string for deterministic generation
            output_path: Optional path to save the avatar
            
        Returns:
            URL or path to the generated avatar
        """
        try:
            # Construct DiceBear URL
            url = f"https://api.dicebear.com/7.x/{style}/svg?seed={seed}"
            
            # Make request
            response = requests.get(url)
            response.raise_for_status()
            
            # Save to file if output_path is provided
            if output_path:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(response.content)
                return output_path
            
            return url
        except Exception as e:
            logger.error(f"Failed to generate avatar: {str(e)}")
            # Return a default avatar URL
            return f"https://api.dicebear.com/7.x/identicon/svg?seed={seed}"
