"""
Anthropic LLM client for the Cartouche Bot Service.
Implements the BaseLLMClient interface for Anthropic's Claude API.
"""
import anthropic
from typing import Dict, List, Any, Optional

from app.clients.llm.base import BaseLLMClient
from app.core.settings import ANTHROPIC_API_KEY
from app.core.exceptions import LLMError

class AnthropicClient(BaseLLMClient):
    """Client for Anthropic's Claude API."""
    
    def __init__(self, api_key: str = ANTHROPIC_API_KEY, model: str = "claude-3-sonnet"):
        """
        Initialize the Anthropic client.
        
        Args:
            api_key: API key for Anthropic
            model: Model to use
        """
        self.api_key = api_key
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    async def generate_text(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """
        Generate text from a prompt using Claude.
        
        Args:
            prompt: The prompt to generate text from
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for text generation
            
        Returns:
            Generated text
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise LLMError(f"Anthropic text generation error: {str(e)}")
    
    async def generate_chat_response(self, 
                                   messages: List[Dict[str, str]], 
                                   max_tokens: int = 1024, 
                                   temperature: float = 0.7) -> str:
        """
        Generate a response in a chat context using Claude.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for text generation
            
        Returns:
            Generated response
        """
        try:
            # Convert messages to Anthropic format
            anthropic_messages = []
            for message in messages:
                role = "user" if message["role"] == "user" else "assistant"
                anthropic_messages.append({"role": role, "content": message["content"]})
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=anthropic_messages
            )
            return response.content[0].text
        except Exception as e:
            raise LLMError(f"Anthropic chat generation error: {str(e)}")
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available models for Anthropic.
        
        Returns:
            List of model names
        """
        return ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]
