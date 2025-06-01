"""
Content generator service for the Cartouche Bot Service.
Handles generation of bot content using LLM.
"""

from typing import List

from app.clients.llm import LLMFactory
from app.core.settings import (
    BOT_PROMPTS,
    BOT_CATEGORIES,
    TEMPERATURE,
    DEFAULT_LLM_PROVIDER,
)
from app.core.exceptions import LLMError

from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()


class ContentGenerator:
    """Service for generating bot content."""

    def __init__(self, llm_provider: str = None, api_key: str = None):
        """
        Initialize the content generator.

        Args:
            llm_provider: LLM provider name
            api_key: API key for the provider
        """
        # Use environment variables as defaults if not provided
        provider = llm_provider or DEFAULT_LLM_PROVIDER

        self.llm_client = LLMFactory.create_client(provider=provider)

    async def generate_bot_description(
        self, category: str, age: int, gender: str
    ) -> str:
        """
        Generate a description for a bot.

        Args:
            category: Bot category
            age: Bot age
            gender: Bot gender

        Returns:
            Generated description

        Raises:
            LLMError: If generation fails
        """
        try:
            category_desc = BOT_CATEGORIES.get(category, {}).get("description", "")
            prompt = f"""
You are a social media user. Your profile: {age} years old, {gender}, {category_desc}.

You are about to write your social media bio.

Write ONLY a short, authentic bio (1-3 sentences) that reflects your personality. Do not write anything else. Do not use hashtags, emojis, or extra words. Only output the bio itself.
"""
            return await self.llm_client.generate_text(
                prompt=prompt, max_tokens=100, temperature=0.7
            )
        except Exception as e:
            logger.error(f"Failed to generate bot description: {str(e)}")
            raise LLMError(f"Failed to generate bot description: {str(e)}")

    async def generate_comment(
        self, bot_category: str, post_text: str, bot_memories: List[str] = None
    ) -> str:
        """
        Generate a comment for a post.

        Args:
            bot_category: Bot category
            post_text: Post text
            bot_memories: List of bot memories related to this post or user

        Returns:
            Generated comment

        Raises:
            LLMError: If generation fails
        """
        try:
            base_prompt = BOT_PROMPTS.get(bot_category, BOT_PROMPTS["neutral"])
            memory_context = ""
            if bot_memories and len(bot_memories) > 0:
                memory_context = "Here are some of your past thoughts and experiences related to this topic:\n"
                for memory in bot_memories[:3]:
                    memory_context += f"- {memory}\n"
            prompt = f"""
{base_prompt}

You are about to comment on a social media post.

{memory_context}
This is the post you see:
"{post_text}"

Based on your memories and your personality, write ONLY a short, authentic comment (1-2 sentences) as your reaction. Do not write anything else. Do not include explanations, greetings, or extra words. Your comment should reflect your character and your past experiences. Only output the comment itself.
"""
            return await self.llm_client.generate_text(
                prompt=prompt, max_tokens=150, temperature=TEMPERATURE
            )
        except Exception as e:
            logger.error(f"Failed to generate comment: {str(e)}")
            raise LLMError(f"Failed to generate comment: {str(e)}")

    async def generate_post(self, bot_category: str) -> str:
        """
        Generate a post for a bot.

        Args:
            bot_category: Bot category
            bot_interests: (ignored, for backward compatibility)

        Returns:
            Generated post

        Raises:
            LLMError: If generation fails
        """
        try:
            base_prompt = BOT_PROMPTS.get(bot_category, BOT_PROMPTS["neutral"])
            prompt = f"""
{base_prompt}

You are about to write a new post on your social media page. Think about your mood, your day, or anything you want to share with your followers. Your post should reflect your unique personality and current feelings.

Write ONLY a short, authentic social media post (1-3 sentences). Do not write anything else. Do not include explanations, greetings, or extra words. Only output the post itself.
"""
            return await self.llm_client.generate_text(
                prompt=prompt, max_tokens=200, temperature=TEMPERATURE
            )
        except Exception as e:
            logger.error(f"Failed to generate post: {str(e)}")
            raise LLMError(f"Failed to generate post: {str(e)}")

    async def generate_memory(
        self, bot_category: str, content: str, context_type: str
    ) -> str:
        """
        Generate a memory entry for a bot.

        Args:
            bot_category: Bot category
            content: Content to remember (post, comment, etc.)
            context_type: Type of context (post, comment, user)

        Returns:
            Generated memory

        Raises:
            LLMError: If generation fails
        """
        try:
            base_prompt = BOT_PROMPTS.get(bot_category, BOT_PROMPTS["neutral"])
            prompt = f"""
{base_prompt}

You are a social media user. You just saw this {context_type}:
"{content}"

Write ONLY a short, private memory (1-3 sentences) about how you feel about this {context_type}. This is your internal thought, not something you would say publicly. Do not write anything else. Do not include explanations, greetings, or extra words. Only output the memory itself.
"""
            return await self.llm_client.generate_text(
                prompt=prompt, max_tokens=100, temperature=TEMPERATURE
            )
        except Exception as e:
            logger.error(f"Failed to generate memory: {str(e)}")
            raise LLMError(f"Failed to generate memory: {str(e)}")

    async def generate_full_name(self, gender: str, age: int) -> str:
        """
        Generate a realistic full name for a bot based on gender and age.

        Args:
            gender: Gender of the person (e.g., 'male', 'female', 'non-binary')
            age: Age of the person

        Returns:
            Generated full name (first and last name)

        Raises:
            LLMError: If generation fails
        """
        try:
            prompt = f"""
You are a social media user. Your profile: {age} years old, {gender}.

You need a realistic full name (first and last) for your profile. The name should be natural and common for your gender and age. Only output the name.
Examples:
Emily Carter
James Lee
Ava Johnson
"""
            full_name = await self.llm_client.generate_text(
                prompt=prompt, max_tokens=20, temperature=0.8
            )
            return full_name
        except Exception as e:
            logger.error(f"Failed to generate full name: {str(e)}")
            raise LLMError(f"Failed to generate full name: {str(e)}")
