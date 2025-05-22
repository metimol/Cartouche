"""
Ollama LLM client for the Cartouche Bot Service.
Implements the BaseLLMClient interface for Ollama's local API.
"""
import aiohttp
import json
from typing import Dict, List, Any, Optional

from app.clients.llm.base import BaseLLMClient
from app.core.settings import OLLAMA_BASE_URL
from app.core.exceptions import LLMError

class OllamaClient(BaseLLMClient):
    """Client for Ollama's local API."""
    
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = "llama2"):
        """
        Initialize the Ollama client.
        
        Args:
            base_url: Base URL for Ollama API
            model: Model to use
        """
        self.base_url = base_url
        self.model = model
    
    async def generate_text(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """
        Generate text from a prompt using Ollama.
        
        Args:
            prompt: The prompt to generate text from
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for text generation
            
        Returns:
            Generated text
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "max_tokens": max_tokens,
                        "temperature": temperature
                    }
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("response", "")
                    else:
                        error_text = await response.text()
                        raise LLMError(f"Ollama API error: {error_text}")
        except Exception as e:
            raise LLMError(f"Ollama text generation error: {str(e)}")
    
    async def generate_chat_response(self, 
                                   messages: List[Dict[str, str]], 
                                   max_tokens: int = 1024, 
                                   temperature: float = 0.7) -> str:
        """
        Generate a response in a chat context using Ollama.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for text generation
            
        Returns:
            Generated response
        """
        try:
            # Format messages for Ollama
            formatted_prompt = ""
            for message in messages:
                if message["role"] == "system":
                    formatted_prompt += f"System: {message['content']}\n\n"
                elif message["role"] == "user":
                    formatted_prompt += f"User: {message['content']}\n\n"
                elif message["role"] == "assistant":
                    formatted_prompt += f"Assistant: {message['content']}\n\n"
            
            formatted_prompt += "Assistant: "
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": formatted_prompt,
                        "max_tokens": max_tokens,
                        "temperature": temperature
                    }
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("response", "")
                    else:
                        error_text = await response.text()
                        raise LLMError(f"Ollama API error: {error_text}")
        except Exception as e:
            raise LLMError(f"Ollama chat generation error: {str(e)}")
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available models for Ollama.
        
        Returns:
            List of model names
        """
        return ["llama2", "mistral"]
