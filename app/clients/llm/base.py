"""
Base LLM client for the Cartouche Bot Service.
Defines the interface for all LLM providers.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    async def generate_text(
        self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7
    ) -> str:
        """
        Generate text from a prompt.

        Args:
            prompt: The prompt to generate text from
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for text generation (higher = more random)

        Returns:
            Generated text
        """
        pass

    @abstractmethod
    async def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate a response in a chat context.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for text generation (higher = more random)

        Returns:
            Generated response
        """
        pass

    @abstractmethod
    def get_available_models(self) -> List[str]:
        """
        Get list of available models for this provider.

        Returns:
            List of model names
        """
        pass
