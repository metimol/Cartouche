"""
OpenAI LLM client for the Cartouche Bot Service.
Implements the BaseLLMClient interface for OpenAI's API.
"""

import openai

from app.clients.llm.base import BaseLLMClient
from app.core.settings import OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_MODEL
from app.core.exceptions import LLMError


class OpenAIClient(BaseLLMClient):
    """Client for OpenAI's API."""

    def __init__(
        self,
        api_key: str = OPENAI_API_KEY,
        api_base: str = OPENAI_API_BASE,
        model: str = OPENAI_MODEL,
    ):
        """
        Initialize the OpenAI client.

        Args:
            api_key: API key for OpenAI
            api_base: API base URL for OpenAI
            model: Model to use
        """
        self.api_key = api_key
        self.api_base = api_base
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.api_base)

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
