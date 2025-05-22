"""
Gemini LLM client for the Cartouche Bot Service.
Handles text generation using Google's Gemini API.
"""
import logging
import google.generativeai as genai
from typing import Optional, Dict, Any, List

from app.clients.llm.base import BaseLLMClient
from app.core.exceptions import LLMError

logger = logging.getLogger(__name__)

class GeminiClient(BaseLLMClient):
    """Client for interacting with Google's Gemini API."""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
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
        
        # Log available models for debugging
        try:
            models = genai.list_models()
            model_names = [model.name for model in models]
            logger.info(f"Available Gemini models: {model_names}")
        except Exception as e:
            logger.warning(f"Failed to list Gemini models: {str(e)}")
    
    async def generate_text(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
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
                "top_k": 40
            }
            
            model = genai.GenerativeModel(
                model_name=self.model,
                generation_config=generation_config
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
    
    async def generate_chat_response(self, messages: List[Dict[str, str]], max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """
        Generate a response in a chat context.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for text generation
            
        Returns:
            Generated response
            
        Raises:
            LLMError: If generation fails
        """
        try:
            # Create a generative model
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                "top_p": 0.95,
                "top_k": 40
            }
            
            model = genai.GenerativeModel(
                model_name=self.model,
                generation_config=generation_config
            )
            
            # Convert messages to Gemini format
            gemini_messages = []
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                # Map roles to Gemini format
                if role == "system":
                    # Add system message as user message with [SYSTEM] prefix
                    gemini_messages.append({"role": "user", "parts": [f"[SYSTEM] {content}"]})
                elif role == "assistant":
                    gemini_messages.append({"role": "model", "parts": [content]})
                else:  # user or any other role
                    gemini_messages.append({"role": "user", "parts": [content]})
            
            # Generate content in chat mode
            chat = model.start_chat(history=gemini_messages)
            response = chat.send_message(gemini_messages[-1]["parts"][0] if gemini_messages else "")
            
            # Extract and return text
            if response.text:
                return response.text.strip()
            else:
                raise LLMError("Gemini returned empty chat response")
        
        except Exception as e:
            logger.error(f"Gemini chat response generation error: {str(e)}")
            raise LLMError(f"Gemini chat response generation error: {str(e)}")
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available models for this provider.
        
        Returns:
            List of model names
        """
        try:
            models = genai.list_models()
            return [model.name for model in models]
        except Exception as e:
            logger.error(f"Failed to get available Gemini models: {str(e)}")
            return [self.model]  # Return default model if listing fails
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using Gemini.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
            
        Raises:
            LLMError: If embedding generation fails
        """
        try:
            # Use embedding model
            embedding_model = "embedding-001"
            result = genai.embed_content(
                model=embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            
            # Extract and return embedding
            if result and hasattr(result, "embedding"):
                return result.embedding
            else:
                raise LLMError("Gemini returned invalid embedding")
        
        except Exception as e:
            logger.error(f"Gemini embedding generation error: {str(e)}")
            raise LLMError(f"Gemini embedding generation error: {str(e)}")
