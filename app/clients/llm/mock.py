"""
Mock LLM client for the Cartouche Bot Service.
Used for testing when real LLM API is unavailable or quota is exceeded.
"""
import logging
import random
from typing import Optional, Dict, Any, List

from app.clients.llm.base import BaseLLMClient
from app.core.exceptions import LLMError

logger = logging.getLogger(__name__)

class MockLLMClient(BaseLLMClient):
    """Mock LLM client for testing."""
    
    def __init__(self, api_key: str = None, model: str = "mock-model"):
        """
        Initialize the mock LLM client.
        
        Args:
            api_key: Not used in mock
            model: Model name for logging
        """
        self.model = model
        logger.info(f"Initialized MockLLMClient with model: {model}")
    
    async def generate_text(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """
        Generate mock text response.
        
        Args:
            prompt: Text prompt
            max_tokens: Maximum number of tokens (not used in mock)
            temperature: Temperature for generation (not used in mock)
            
        Returns:
            Generated text
        """
        logger.info(f"MockLLMClient generating text for prompt: {prompt[:50]}...")
        
        # Generate different responses based on prompt content
        if "bio" in prompt.lower() or "description" in prompt.lower():
            return "I'm a social media enthusiast who loves sharing thoughts and connecting with others. Always looking for new perspectives!"
        
        elif "comment" in prompt.lower():
            comments = [
                "This is really interesting! Thanks for sharing.",
                "I've been thinking about this topic a lot lately. Great post!",
                "I see your point, but have you considered the alternative view?",
                "Love this content! Keep it coming!",
                "This made me laugh. Thanks for brightening my day!"
            ]
            return random.choice(comments)
        
        elif "post" in prompt.lower():
            posts = [
                "Just finished reading an amazing book that changed my perspective on life. Sometimes the best discoveries happen when you least expect them.",
                "Beautiful day for a hike! Nature always helps me clear my mind and find new inspiration.",
                "Trying out a new recipe today. Cooking is my favorite way to be creative and relax after a busy week.",
                "Interesting discussion with colleagues today about the future of technology. What do you think will be the next big innovation?",
                "Throwback to last summer's adventure. Can't wait to travel again soon!"
            ]
            return random.choice(posts)
        
        elif "username" in prompt.lower() or "name" in prompt.lower():
            names = [
                "creative_soul",
                "digital_nomad",
                "curious_mind",
                "thought_explorer",
                "idea_catalyst",
                "future_thinker",
                "social_butterfly",
                "wisdom_seeker",
                "trend_watcher",
                "culture_critic"
            ]
            return random.choice(names)
        
        elif "memory" in prompt.lower() or "thought" in prompt.lower():
            memories = [
                "This reminds me of something I read recently.",
                "I should follow up on this topic later.",
                "This person seems to have interesting perspectives.",
                "I'm not sure I agree with this take, but it's thought-provoking.",
                "This content resonates with my own experiences."
            ]
            return random.choice(memories)
        
        else:
            # Generic response for other prompts
            return "This is a mock response from the LLM client for testing purposes."
    
    async def generate_chat_response(self, messages: List[Dict[str, str]], max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """
        Generate a mock response in a chat context.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            max_tokens: Maximum number of tokens (not used in mock)
            temperature: Temperature for text generation (not used in mock)
            
        Returns:
            Generated response
        """
        logger.info(f"MockLLMClient generating chat response for {len(messages)} messages")
        
        # Get the last user message
        last_message = messages[-1]["content"] if messages else ""
        
        # Generate response based on the last message
        return await self.generate_text(last_message, max_tokens, temperature)
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available models for this provider.
        
        Returns:
            List of model names
        """
        return ["mock-model", "mock-model-large", "mock-model-small"]
