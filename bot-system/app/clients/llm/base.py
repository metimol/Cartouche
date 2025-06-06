"""
Base LLM client for the Cartouche Bot Service.
Defines the interface for all LLM providers.
"""

from abc import ABC, abstractmethod


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
