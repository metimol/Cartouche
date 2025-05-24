"""
Core settings module for the Cartouche Bot Service.
Loads configuration from environment variables.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List

from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=str(env_path))

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://fraplat.tech/mars/Cartouche")
API_TOKEN = os.getenv("API_TOKEN", "123")

# LLM Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "gemini")
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "gemini-2.0-flash")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))

# Database Configuration
DB_PATH = os.getenv("DB_PATH", "data/cartouche.db")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "data/vector_store")

# Bot Configuration
INITIAL_BOTS_COUNT = int(os.getenv("INITIAL_BOTS_COUNT", "20"))
DAILY_BOTS_GROWTH_MIN = int(os.getenv("DAILY_BOTS_GROWTH_MIN", "20"))
DAILY_BOTS_GROWTH_MAX = int(os.getenv("DAILY_BOTS_GROWTH_MAX", "50"))
MAX_BOTS_COUNT = int(os.getenv("MAX_BOTS_COUNT", "5000"))

# Monitoring Configuration
MONITORING_INTERVAL = int(os.getenv("MONITORING_INTERVAL", "60"))
REACTION_DELAY_MIN = int(os.getenv("REACTION_DELAY_MIN", "30"))
REACTION_DELAY_MAX = int(os.getenv("REACTION_DELAY_MAX", "300"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/cartouche.log")

# LLM Provider mapping
LLM_PROVIDERS = {
    "gemini": {
        "api_key": GOOGLE_API_KEY,
        "models": [
            "gemini-1.0-pro-vision-latest",
            "gemini-pro-vision",
            "gemini-1.5-pro-latest",
            "gemini-1.5-pro-001",
            "gemini-1.5-pro-002",
            "gemini-1.5-pro",
            "gemini-1.5-flash-latest",
            "gemini-1.5-flash-001",
            "gemini-1.5-flash-001-tuning",
            "gemini-1.5-flash",
            "gemini-1.5-flash-002",
            "gemini-1.5-flash-8b",
            "gemini-1.5-flash-8b-001",
            "gemini-1.5-flash-8b-latest",
            "gemini-1.5-flash-8b-exp-0827",
            "gemini-1.5-flash-8b-exp-0924",
            "gemini-2.5-pro-exp-03-25",
            "gemini-2.5-pro-preview-03-25",
            "gemini-2.5-flash-preview-04-17",
            "gemini-2.5-flash-preview-05-20",
            "gemini-2.5-flash-preview-04-17-thinking",
            "gemini-2.5-pro-preview-05-06",
            "gemini-2.0-flash-exp",
            "gemini-2.0-flash",
            "gemini-2.0-flash-001",
            "gemini-2.0-flash-lite-001",
            "gemini-2.0-flash-lite",
            "gemini-2.0-flash-lite-preview-02-05",
            "gemini-2.0-flash-lite-preview",
            "gemini-2.0-pro-exp",
            "gemini-2.0-pro-exp-02-05",
            "gemini-exp-1206",
            "gemini-2.0-flash-thinking-exp-01-21",
            "gemini-2.0-flash-thinking-exp",
            "gemini-2.0-flash-thinking-exp-1219",
            "gemini-2.5-flash-preview-tts",
            "gemini-2.5-pro-preview-tts",
            "gemma-3-1b-it",
            "gemma-3-4b-it",
            "gemma-3-12b-it",
            "gemma-3-27b-it",
            "gemma-3n-e4b-it",
        ],
    },
    "openai": {
        "api_key": OPENAI_API_KEY,
        "models": [
            "gpt-4o",
            "chatgpt-4o-latest",
            "gpt-4o-mini",
            "gpt-4.1",
            "gpt-4.1-mini",
            "gpt-4.1-nano",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-4",
            "gpt-4-32k",
            "gpt-4-1106-preview",
            "gpt-4-0125-preview",
            "gpt-4-turbo-2024-04-09",
            "gpt-4-turbo",
            "gpt-4.5-preview-2025-02-27",
            "gpt-4.5-preview",
            "o1",
            "o1-2024-12-17",
            "o1-preview",
            "o1-mini",
            "o3-mini",
            "o3",
            "o4-mini",
            "gpt-3.5-turbo-instruct",
        ],
    },
    "anthropic": {
        "api_key": ANTHROPIC_API_KEY,
        "models": [
            "claude-3-7-sonnet-latest",
            "claude-3-5-haiku-latest",
            "claude-3-5-sonnet-latest",
            "claude-3-opus-latest",
        ],
    },
}

# Bot categories and their base probabilities
BOT_CATEGORIES = {
    "fan": {
        "like_probability": 0.8,
        "comment_probability": 0.5,
        "follow_probability": 0.7,
        "unfollow_probability": 0.1,
        "repost_probability": 0.2,
        "description": "Supportive, enthusiastic, positive",
    },
    "hater": {
        "like_probability": 0.1,
        "comment_probability": 0.4,
        "follow_probability": 0.2,
        "unfollow_probability": 0.6,
        "repost_probability": 0.05,
        "description": "Critical, negative, provocative",
    },
    "silent": {
        "like_probability": 0.4,
        "comment_probability": 0.1,
        "follow_probability": 0.3,
        "unfollow_probability": 0.2,
        "repost_probability": 0.05,
        "description": "Observant, rarely comments, occasional likes",
    },
    "random": {
        "like_probability": 0.5,
        "comment_probability": 0.3,
        "follow_probability": 0.4,
        "unfollow_probability": 0.4,
        "repost_probability": 0.1,
        "description": "Unpredictable, varied behavior",
    },
    "neutral": {
        "like_probability": 0.5,
        "comment_probability": 0.3,
        "follow_probability": 0.5,
        "unfollow_probability": 0.3,
        "repost_probability": 0.1,
        "description": "Balanced, rational, thoughtful",
    },
    "humorous": {
        "like_probability": 0.7,
        "comment_probability": 0.6,
        "follow_probability": 0.6,
        "unfollow_probability": 0.2,
        "repost_probability": 0.15,
        "description": "Funny, sarcastic, meme-oriented",
    },
    "provocative": {
        "like_probability": 0.3,
        "comment_probability": 0.7,
        "follow_probability": 0.4,
        "unfollow_probability": 0.5,
        "repost_probability": 0.1,
        "description": "Challenging, questioning, debate-oriented",
    },
    "role_player": {
        "like_probability": 0.6,
        "comment_probability": 0.5,
        "follow_probability": 0.5,
        "unfollow_probability": 0.3,
        "repost_probability": 0.15,
        "description": "In-character, consistent persona",
    },
}

# Base prompts for bot behavior
BOT_PROMPTS = {
    "fan": "You are an enthusiastic fan who loves the content. Your comments are supportive and positive.",
    "hater": "You are critical of the content. Your comments point out flaws and are sometimes negative.",
    "silent": "You rarely comment, but when you do, it's thoughtful and concise.",
    "random": "Your behavior is unpredictable. Sometimes supportive, sometimes critical, sometimes off-topic.",
    "neutral": "You are balanced and rational. Your comments are thoughtful and objective.",
    "humorous": "You love humor and memes. Your comments are funny, sometimes sarcastic.",
    "provocative": "You like to challenge ideas. Your comments ask difficult questions and provoke thought.",
    "role_player": "You stay in character as {role}. Your comments reflect this persona consistently.",
}

# Avatar generation options
AVATAR_STYLES = [
    "adventurer-neutral",
    "avataaars-neutral",
    "big-ears-neutral",
    "bottts-neutral",
    "dylan",
    "fun-emoji",
    "glass",
    "pixel-art-neutral",
    "thumbs",
    "shapes",
]
