"""
LLM factory for the Cartouche Bot Service.
Creates and manages LLM clients based on configuration.
"""

from typing import Dict, Optional, List, Any
import os
import logging

from app.clients.llm.base import BaseLLMClient
from app.clients.llm.gemini import GeminiClient
from app.clients.llm.openai import OpenAIClient
from app.clients.llm.anthropic import AnthropicClient
from app.core.settings import DEFAULT_LLM_PROVIDER, LLM_PROVIDERS
from app.core.exceptions import LLMError

logger = logging.getLogger(__name__)

# Check if we're in test mode
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"


class LLMFactory:
    """Factory for creating LLM clients."""

    @staticmethod
    def create_client(
        provider: str = DEFAULT_LLM_PROVIDER,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ) -> BaseLLMClient:
        """
        Create an LLM client based on provider.

        Args:
            provider: LLM provider name
            api_key: Optional API key
            base_url: Optional base URL
            model: Optional model name

        Returns:
            LLM client instance

        Raises:
            LLMError: If provider is not supported
        """
        if provider == "gemini":
            return GeminiClient(api_key=api_key, model=model or "gemini-2.0-flash")
        elif provider == "openai":
            return OpenAIClient(api_key=api_key, model=model or "gpt-3.5-turbo")
        elif provider == "anthropic":
            return AnthropicClient(
                api_key=api_key, model=model or "claude-3-sonnet"
            )
        else:
            raise LLMError(f"Unsupported LLM provider: {provider}")

    @staticmethod
    def get_available_providers() -> List[str]:
        """
        Get list of available LLM providers.

        Returns:
            List of provider names
        """
        providers = list(LLM_PROVIDERS.keys())
        return providers

    @staticmethod
    def get_provider_models(provider: str) -> List[str]:
        """
        Get list of available models for a provider.

        Args:
            provider: LLM provider name

        Returns:
            List of model names

        Raises:
            LLMError: If provider is not supported
        """
        if provider in LLM_PROVIDERS:
            return LLM_PROVIDERS[provider]["models"]
        else:
            raise LLMError(f"Unsupported LLM provider: {provider}")
