"""
Gemini LLM client for the Cartouche Bot Service.
Handles text generation using Google's Gemini API.
"""

import google.generativeai as genai
from app.clients.llm.base import BaseLLMClient
from app.core.exceptions import LLMError
from app.core.logging import setup_logging
from app.core.settings import GOOGLE_API_KEY, GOOGLE_MODEL

# Setup logging
logger = setup_logging()


class GeminiClient(BaseLLMClient):
    """Client for interacting with Google's Gemini API."""

    def __init__(self, api_key: str = GOOGLE_API_KEY, model: str = GOOGLE_MODEL):
        """
        Initialize the Gemini client.

        Args:
            api_key: API key for authentication
            model: Model name to use
        """
        self.api_key = api_key
        self.model = model

        # Configure the Gemini API
        genai.configure(api_key=api_key)

    async def generate_text(
        self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7
    ) -> str:
        """
        Generate text using Gemini.

        Args:
            prompt: Text prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for generation

        Returns:
            Generated text

        Raises:
            LLMError: If generation fails
        """
        try:
            # Create a generative model
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                "top_p": 0.95,
                "top_k": 40,
            }

            model = genai.GenerativeModel(
                model_name=self.model, generation_config=generation_config
            )

            # Generate content
            response = model.generate_content(prompt)

            # Extract and return text
            if response.text:
                return response.text.strip()
            else:
                raise LLMError("Gemini returned empty response")

        except Exception as e:
            logger.error(f"Gemini text generation error: {str(e)}")
            raise LLMError(f"Gemini text generation error: {str(e)}")
