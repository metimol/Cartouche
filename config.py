"""
Configuration module for the Cartouche Autonomous Service.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
LOG_DIR = BASE_DIR / 'logs'

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# API Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'https://fraplat.tech/mars/Cartouche')
API_TOKEN = os.getenv('API_TOKEN', '123')  # Default token from the API documentation

# Database Configuration
DB_PATH = os.getenv('DB_PATH', str(DATA_DIR / 'cartouche.db'))
VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', str(DATA_DIR / 'vector_store'))

# LLM Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
DEFAULT_LLM_MODEL = os.getenv('DEFAULT_LLM_MODEL', 'gemini-pro')
LIGHT_LLM_MODEL = os.getenv('LIGHT_LLM_MODEL', 'gemini-pro')
MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1024'))
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))

# Bot Configuration
INITIAL_BOTS_COUNT = int(os.getenv('INITIAL_BOTS_COUNT', '20'))
DAILY_BOTS_GROWTH_MIN = int(os.getenv('DAILY_BOTS_GROWTH_MIN', '20'))
DAILY_BOTS_GROWTH_MAX = int(os.getenv('DAILY_BOTS_GROWTH_MAX', '50'))
MAX_BOTS_COUNT = int(os.getenv('MAX_BOTS_COUNT', '10000'))

# Bot Categories
BOT_CATEGORIES = [
    'fan',
    'hater',
    'silent',
    'random',
    'neutral',
    'humorous',
    'provocative',
    'roleplay'
]

# Monitoring Configuration
MONITORING_INTERVAL = int(os.getenv('MONITORING_INTERVAL', '60'))  # seconds
REACTION_DELAY_MIN = int(os.getenv('REACTION_DELAY_MIN', '30'))  # seconds
REACTION_DELAY_MAX = int(os.getenv('REACTION_DELAY_MAX', '300'))  # seconds

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', str(LOG_DIR / 'cartouche.log'))
LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Cache Configuration
CACHE_TTL = int(os.getenv('CACHE_TTL', '3600'))  # seconds

# Scheduler Configuration
SCHEDULER_TIMEZONE = os.getenv('SCHEDULER_TIMEZONE', 'UTC')
