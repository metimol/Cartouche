"""
Configuration settings for the Cartouche Bot Service.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
API_PREFIX = "/api/v1"

# LLM settings
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "gemini-1.5-pro")
LIGHT_LLM_MODEL = os.getenv("LIGHT_LLM_MODEL", "gemini-1.5-flash")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Database settings
DB_PATH = os.getenv("DB_PATH", "bot_memory.db")

# Redis settings
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))

# Bot settings
INITIAL_BOTS_COUNT = int(os.getenv("INITIAL_BOTS_COUNT", "20"))
MAX_BOTS_COUNT = int(os.getenv("MAX_BOTS_COUNT", "500"))
BOT_GROWTH_RATE = float(os.getenv("BOT_GROWTH_RATE", "0.05"))
MAX_NEW_BOTS_PER_DAY = int(os.getenv("MAX_NEW_BOTS_PER_DAY", "30"))
BOT_GROWTH_INTERVAL = int(os.getenv("BOT_GROWTH_INTERVAL", "86400"))  # 24 hours in seconds

# Main app integration
MAIN_APP_URL = os.getenv("MAIN_APP_URL", "http://localhost:8080")
MAIN_APP_API_KEY = os.getenv("MAIN_APP_API_KEY", "")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "bot_service.log")

# Celery settings
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

# Language settings
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
SUPPORTED_LANGUAGES = ["en", "ru", "es", "fr", "de"]

# DiceBear API
DICEBEAR_API_URL = os.getenv("DICEBEAR_API_URL", "https://api.dicebear.com/7.x")
DICEBEAR_STYLE = os.getenv("DICEBEAR_STYLE", "avataaars")
