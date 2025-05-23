"""
OpenAI LLM client for the Cartouche Bot Service.
Implements the BaseLLMClient interface for OpenAI's API.
"""

import openai
from typing import Dict, List, Any, Optional

from app.clients.llm.base import BaseLLMClient
from app.core.settings import OPENAI_API_KEY
from app.core.exceptions import LLMError


class OpenAIClient(BaseLLMClient):
    """Client for OpenAI's API."""

    def __init__(self, api_key: str = OPENAI_API_KEY, model: str = "gpt-3.5-turbo"):
        """
        Initialize the OpenAI client.

        Args:
            api_key: API key for OpenAI
            model: Model to use
        """
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)

    async def generate_text(
        self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7
    ) -> str:
        """
        Generate text from a prompt using OpenAI.

        Args:
            prompt: The prompt to generate text from
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for text generation

        Returns:
            Generated text
        """
        try:
            response = self.client.completions.create(
                model=self.model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            raise LLMError(f"OpenAI text generation error: {str(e)}")

    async def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate a response in a chat context using OpenAI.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for text generation

        Returns:
            Generated response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise LLMError(f"OpenAI chat generation error: {str(e)}")

    def get_available_models(self) -> List[str]:
        """
        Get list of available models for OpenAI.

        Returns:
            List of model names
        """
        return ["gpt-3.5-turbo", "gpt-4"]
