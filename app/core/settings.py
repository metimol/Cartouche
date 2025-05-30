"""
Core settings module for the Cartouche Bot Service.
Loads configuration from environment variables.
"""

import os
from pathlib import Path
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
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "gemini")
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
REACTION_DELAY_MIN = float(os.getenv("REACTION_DELAY_MIN", "5"))
REACTION_DELAY_MAX = float(os.getenv("REACTION_DELAY_MAX", "30"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOG_FILE = os.getenv("LOG_FILE", "logs/cartouche.log")

# Bot categories and their base probabilities
BOT_CATEGORIES = {
    "fan": {
        "like_probability": 0.8,
        "comment_probability": 0.5,
        "follow_probability": 0.7,
        "unfollow_probability": 0.1,
        "post_probability": 0.4,
        "description": "Supportive, enthusiastic, positive",
    },
    "hater": {
        "like_probability": 0.1,
        "comment_probability": 0.4,
        "follow_probability": 0.2,
        "unfollow_probability": 0.6,
        "post_probability": 0.2,
        "description": "Critical, negative, provocative",
    },
    "silent": {
        "like_probability": 0.4,
        "comment_probability": 0.1,
        "follow_probability": 0.3,
        "unfollow_probability": 0.2,
        "post_probability": 0.1,
        "description": "Observant, rarely comments, occasional likes",
    },
    "random": {
        "like_probability": 0.5,
        "comment_probability": 0.3,
        "follow_probability": 0.4,
        "unfollow_probability": 0.4,
        "post_probability": 0.15,
        "description": "Unpredictable, varied behavior",
    },
    "neutral": {
        "like_probability": 0.5,
        "comment_probability": 0.3,
        "follow_probability": 0.5,
        "unfollow_probability": 0.3,
        "post_probability": 0.1,
        "description": "Balanced, rational, thoughtful",
    },
    "humorous": {
        "like_probability": 0.7,
        "comment_probability": 0.6,
        "follow_probability": 0.6,
        "unfollow_probability": 0.2,
        "post_probability": 0.4,
        "description": "Funny, sarcastic, meme-oriented",
    },
    "provocative": {
        "like_probability": 0.3,
        "comment_probability": 0.7,
        "follow_probability": 0.4,
        "unfollow_probability": 0.5,
        "post_probability": 0.2,
        "description": "Challenging, questioning, debate-oriented",
    },
    "role_player": {
        "like_probability": 0.6,
        "comment_probability": 0.5,
        "follow_probability": 0.5,
        "unfollow_probability": 0.3,
        "post_probability": 0.15,
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
    "fun-emoji",
    "pixel-art-neutral",
    "thumbs",
    "shapes",
]
