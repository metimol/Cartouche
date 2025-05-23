"""
Content generator service for the Cartouche Bot Service.
Handles generation of bot content using LLM.
"""

from typing import List
import random
import logging

from app.clients.llm import LLMFactory
from app.core.settings import (
    BOT_PROMPTS,
    BOT_CATEGORIES,
    TEMPERATURE,
    MAX_TOKENS,
    DEFAULT_LLM_PROVIDER,
    GOOGLE_API_KEY,
)
from app.core.exceptions import LLMError

logger = logging.getLogger(__name__)


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
        key = api_key or GOOGLE_API_KEY

        logger.info(f"Initializing ContentGenerator with provider: {provider}")
        self.llm_client = LLMFactory.create_client(provider=provider, api_key=key)

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
You are a bot that writes social media bios. Write ONLY the bio. Do not write anything else. Do not write explanations, greetings, or extra words. 

Write a short social media bio for a {age}-year-old {gender} who is {category_desc}.
The bio must be 1 to 3 sentences. The style is casual. The bio must reflect the personality. Do NOT use hashtags. Do NOT use emojis. Do NOT add any extra text. Only output the bio itself.
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

            # Include memories if available
            memory_context = ""
            if bot_memories and len(bot_memories) > 0:
                memory_context = (
                    "Here are some of your past interactions and thoughts:\n"
                )
                for memory in bot_memories[:3]:  # Limit to 3 memories
                    memory_context += f"- {memory}\n"

            prompt = f"""
{base_prompt}

{memory_context}

Someone posted this on social media:
"{post_text}"

Write ONLY a short, realistic comment as a response. Do not write anything else. Do not write explanations, greetings, or extra words. The comment must be 1 or 2 sentences. Be authentic and match the tone of your character. Only output the comment itself.
"""

            return await self.llm_client.generate_text(
                prompt=prompt, max_tokens=150, temperature=TEMPERATURE
            )
        except Exception as e:
            logger.error(f"Failed to generate comment: {str(e)}")
            raise LLMError(f"Failed to generate comment: {str(e)}")

    async def generate_post(
        self, bot_category: str, bot_interests: List[str] = None
    ) -> str:
        """
        Generate a post for a bot.

        Args:
            bot_category: Bot category
            bot_interests: List of bot interests

        Returns:
            Generated post

        Raises:
            LLMError: If generation fails
        """
        try:
            base_prompt = BOT_PROMPTS.get(bot_category, BOT_PROMPTS["neutral"])

            # Include interests if available
            interest_context = ""
            if bot_interests and len(bot_interests) > 0:
                interest = random.choice(bot_interests)
                interest_context = f"You're interested in {interest}."

            prompt = f"""
{base_prompt}

{interest_context}

Write ONLY a short, realistic social media post. Do not write anything else. Do not write explanations, greetings, or extra words. The post must be 1 to 3 sentences. Be authentic and match the tone of your character. Only output the post itself.
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

You just saw this {context_type}:
"{content}"

Write ONLY a short memory (1 sentence) about how you feel about this {context_type}. This is your internal thought, not something you would say publicly. Do not write anything else. Do not write explanations, greetings, or extra words. Only output the memory itself.
"""

            return await self.llm_client.generate_text(
                prompt=prompt, max_tokens=100, temperature=TEMPERATURE
            )
        except Exception as e:
            logger.error(f"Failed to generate memory: {str(e)}")
            raise LLMError(f"Failed to generate memory: {str(e)}")

    async def generate_bot_username(self, category: str) -> str:
        """
        Generate a username for a bot.

        Args:
            category: Bot category

        Returns:
            Generated username

        Raises:
            LLMError: If generation fails
        """
        try:
            category_desc = BOT_CATEGORIES.get(category, {}).get("description", "")
            prompt = f"""
You are a bot that creates usernames. Write ONLY the username. Do not write anything else. Do not write explanations, greetings, or extra words.

Create a unique social media username for someone who is {category_desc}.
The username must be a single word or words connected with underscores. No spaces, no special characters, no numbers. The username must be short (max 20 characters) and memorable. Only output the username itself.
Examples:
funny_friend
musiclover
happycat
"""

            username = await self.llm_client.generate_text(
                prompt=prompt, max_tokens=50, temperature=0.8
            )

            # Clean up the username
            username = username.strip().replace(" ", "_").replace("@", "")
            if len(username) > 15:
                username = username[:15]

            return username
        except Exception as e:
            logger.error(f"Failed to generate bot name: {str(e)}")
            raise LLMError(f"Failed to generate bot name: {str(e)}")

    async def generate_unique_bot_username(self, category: str, bot_repository) -> str:
        """
        Generate a unique username for a bot, ensuring it does not exist in the database.
        Args:
            category: Bot category
            bot_repository: BotRepository instance
        Returns:
            Unique username
        Raises:
            LLMError: If generation fails
        """
        max_attempts = 10
        for _ in range(max_attempts):
            username = await self.generate_bot_username(category)
            if not bot_repository.get_bot_by_name(username):
                return username
        # Fallback: add random suffix if all attempts failed
        import uuid

        for _ in range(10):
            username = f"{username[:12]}_{str(uuid.uuid4())[:2]}"
            if not bot_repository.get_bot_by_name(username):
                return username
        raise LLMError(
            "Failed to generate unique bot username after multiple attempts."
        )

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
You are a bot that creates realistic full names for people. Write ONLY the full name (first and last name). Do not write anything else. Do not write explanations, greetings, or extra words.

Create a realistic full name for a {age}-year-old {gender}.
The name should be common, natural, and appropriate for the gender and age. Only output the full name itself.
Examples:
Emily Carter
James Lee
Ava Johnson
"""
            full_name = await self.llm_client.generate_text(
                prompt=prompt, max_tokens=20, temperature=0.8
            )
            return full_name.strip()
        except Exception as e:
            logger.error(f"Failed to generate full name: {str(e)}")
            raise LLMError(f"Failed to generate full name: {str(e)}")
