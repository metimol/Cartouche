"""
LLM factory for the Cartouche Bot Service.
Creates and manages LLM clients based on configuration.
"""

from app.clients.llm.base import BaseLLMClient
from app.clients.llm.gemini import GeminiClient
from app.clients.llm.openai import OpenAIClient
from app.core.settings import DEFAULT_LLM_PROVIDER
from app.core.exceptions import LLMError

from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()


class LLMFactory:
    """Factory for creating LLM clients."""

    @staticmethod
    def create_client(
        provider: str = DEFAULT_LLM_PROVIDER,
    ) -> BaseLLMClient:
        """
        Create an LLM client based on provider.

        Args:
            provider: LLM provider name

        Returns:
            LLM client instance

        Raises:
            LLMError: If provider is not supported
        """
        if provider == "gemini":
            return GeminiClient()
        elif provider == "openai":
            return OpenAIClient()
        else:
            raise LLMError(f"Unsupported LLM provider: {provider}")
