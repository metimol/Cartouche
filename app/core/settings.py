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
API_TOKEN = os.getenv("API_TOKEN", None)

# LLM Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", None)
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "gemini")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))

# Database Configuration
DB_PATH = os.getenv("DB_PATH", "data/cartouche.db")

# Qdrant Configuration
QDRANT_HOST = os.getenv("QDRANT_HOST", None)
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))

# Bot Configuration
INITIAL_BOTS_COUNT = int(os.getenv("INITIAL_BOTS_COUNT", "20"))
DAILY_BOTS_GROWTH_MIN = int(os.getenv("DAILY_BOTS_GROWTH_MIN", "20"))
DAILY_BOTS_GROWTH_MAX = int(os.getenv("DAILY_BOTS_GROWTH_MAX", "50"))
MAX_BOTS_COUNT = int(os.getenv("MAX_BOTS_COUNT", "5000"))
MAX_COMMENTS_PER_POST = int(os.getenv("MAX_COMMENTS_PER_POST", "3"))

# Monitoring Configuration
MONITORING_INTERVAL = 60  # in seconds
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

def validate_settings():
    errors = []
    # API Configuration
    if not API_BASE_URL:
        errors.append("API_BASE_URL is required.")
    if not API_TOKEN:
        errors.append("API_TOKEN is required.")
    # LLM Configuration
    if not (GOOGLE_API_KEY or OPENAI_API_KEY):
        errors.append("At least one LLM API key (GOOGLE_API_KEY or OPENAI_API_KEY) is required.")
    if DEFAULT_LLM_PROVIDER not in ("gemini", "openai"):
        errors.append(f"DEFAULT_LLM_PROVIDER must be 'gemini' or 'openai', got '{DEFAULT_LLM_PROVIDER}'.")
    if not (0 <= TEMPERATURE <= 2):
        errors.append("TEMPERATURE must be between 0 and 2.")
    if MAX_TOKENS <= 0:
        errors.append("MAX_TOKENS must be positive.")
    # Database
    if not DB_PATH:
        errors.append("DB_PATH is required.")
    # Qdrant
    if not QDRANT_HOST:
        errors.append("QDRANT_HOST is required.")
    if not QDRANT_PORT or not (0 < QDRANT_PORT < 65536):
        errors.append("QDRANT_PORT must be a valid port number.")
    # Bots
    if not (0 < INITIAL_BOTS_COUNT <= MAX_BOTS_COUNT):
        errors.append("INITIAL_BOTS_COUNT must be > 0 and <= MAX_BOTS_COUNT.")
    if not (0 <= DAILY_BOTS_GROWTH_MIN <= DAILY_BOTS_GROWTH_MAX):
        errors.append("DAILY_BOTS_GROWTH_MIN must be <= DAILY_BOTS_GROWTH_MAX.")
    if MAX_BOTS_COUNT <= 0:
        errors.append("MAX_BOTS_COUNT must be positive.")
    # Monitoring
    if not isinstance(REACTION_DELAY_MIN, (int, float)) or not isinstance(REACTION_DELAY_MAX, (int, float)):
        errors.append("REACTION_DELAY_MIN and REACTION_DELAY_MAX must be numbers.")
    elif not (0 <= REACTION_DELAY_MIN <= REACTION_DELAY_MAX):
        errors.append("REACTION_DELAY_MIN must be <= REACTION_DELAY_MAX.")
    if not float(REACTION_DELAY_MIN).is_integer() or not float(REACTION_DELAY_MAX).is_integer():
        errors.append("REACTION_DELAY_MIN and REACTION_DELAY_MAX must be integers.")
    # Logging
    if not LOG_LEVEL:
        errors.append("LOG_LEVEL is required.")
    if not LOG_FILE:
        errors.append("LOG_FILE is required.")
    if errors:
        raise RuntimeError("\n".join(errors))

# Validate settings on import
validate_settings()
