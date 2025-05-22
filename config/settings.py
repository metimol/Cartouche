"""
Configuration settings for the Cartouche Bot Service.
"""
import os
import logging
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API settings
MAIN_APP_URL = os.getenv("MAIN_APP_URL", "http://localhost:8000")
MAIN_APP_API_KEY = os.getenv("MAIN_APP_API_KEY", "test_api_key")

# LLM settings
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-pro")
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "gemini-pro")  # Added for compatibility
LIGHT_LLM_MODEL = os.getenv("LIGHT_LLM_MODEL", "gemini-pro-vision")  # Added for compatibility
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))  # Added for compatibility
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))  # Added for compatibility
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "30"))

# Bot settings
MAX_DAILY_NEW_BOTS = int(os.getenv("MAX_DAILY_NEW_BOTS", "30"))
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")

# Database settings
DB_PATH = os.getenv("DB_PATH", "/tmp/cartouche_bots.db")  # Added for BotManager

# Language settings
SUPPORTED_LANGUAGES = ["en", "ru", "es", "fr", "de", "it", "pt", "ja", "zh", "ko"]

# Cache settings
CACHE_DIR = os.getenv("CACHE_DIR", "/tmp/cartouche_cache")

# Celery settings
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TIMEZONE = "UTC"
CELERY_ENABLE_UTC = True

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = os.getenv("LOG_FILE", "")

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    filename=LOG_FILE if LOG_FILE else None
)

# Server settings
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

# Bot personality types and their probabilities
BOT_PERSONALITY_TYPES = {
    "fan": 0.3,       # Fans are more common
    "hater": 0.1,     # Haters are less common
    "neutral": 0.4,   # Neutral users are most common
    "troll": 0.05,    # Trolls are rare
    "intellectual": 0.15  # Intellectuals are somewhat common
}

# Bot action probabilities by personality type
BOT_ACTION_PROBABILITIES = {
    "fan": {
        "like": 0.8,
        "comment": 0.6,
        "repost": 0.4,
        "follow": 0.7,
        "unfollow": 0.05,
        "post": 0.3
    },
    "hater": {
        "like": 0.1,
        "comment": 0.7,
        "repost": 0.2,
        "follow": 0.3,
        "unfollow": 0.4,
        "post": 0.4
    },
    "neutral": {
        "like": 0.5,
        "comment": 0.3,
        "repost": 0.2,
        "follow": 0.4,
        "unfollow": 0.2,
        "post": 0.2
    },
    "troll": {
        "like": 0.3,
        "comment": 0.8,
        "repost": 0.1,
        "follow": 0.2,
        "unfollow": 0.6,
        "post": 0.5
    },
    "intellectual": {
        "like": 0.6,
        "comment": 0.7,
        "repost": 0.3,
        "follow": 0.5,
        "unfollow": 0.1,
        "post": 0.6
    }
}
