"""
Test script for the Cartouche Bot Service.
Tests database connections, API integrations, and core functionality.
"""
import os
import sys
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import dotenv at the very beginning to ensure environment variables are loaded
from dotenv import load_dotenv
# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=str(env_path))
else:
    print(f"Warning: .env file not found at {env_path}")

from app.core.logging import setup_logging
from app.db.session import get_db, engine, Base
from app.db.models import Bot, BotMemory, BotActivity
from app.db.repositories.bot_repository import BotRepository
from app.db.repositories.memory_repository import MemoryRepository
from app.db.repositories.activity_repository import ActivityRepository
from app.services.content_generator import ContentGenerator
from app.services.bot_manager import BotManager
from app.services.reaction_engine import ReactionEngine
from app.clients.cartouche_api import CartoucheAPIClient
from app.clients.llm import LLMFactory
from app.core.settings import GOOGLE_API_KEY, DEFAULT_LLM_PROVIDER
from app.tests.mock_api import MockCartoucheAPIClient

# Setup logging
logger = setup_logging()

# Print environment variables for debugging
logger.info(f"Environment variables: DEFAULT_LLM_PROVIDER={DEFAULT_LLM_PROVIDER}, GOOGLE_API_KEY={GOOGLE_API_KEY[:5]}...")

async def test_database_connection():
    """Test database connection and models."""
    logger.info("Testing database connection...")
    
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Get database session
        db = next(get_db())
        
        # Test repositories
        bot_repo = BotRepository(db)
        memory_repo = MemoryRepository(db)
        activity_repo = ActivityRepository(db)
        
        # Count bots
        bot_count = bot_repo.count_bots()
        logger.info(f"Current bot count: {bot_count}")
        
        return True
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        return False

async def test_llm_integration():
    """Test LLM integration."""
    logger.info("Testing LLM integration...")
    
    try:
        # Create LLM client with explicit provider and key
        provider = DEFAULT_LLM_PROVIDER
        api_key = GOOGLE_API_KEY
        
        logger.info(f"Creating LLM client with provider: {provider}")
        llm_client = LLMFactory.create_client(provider=provider, api_key=api_key)
        
        # Test text generation
        prompt = "Write a short greeting message."
        response = await llm_client.generate_text(prompt, max_tokens=50)
        
        logger.info(f"LLM response: {response}")
        
        if response and len(response) > 0:
            logger.info("LLM integration test passed")
            return True
        else:
            logger.error("LLM returned empty response")
            return False
    except Exception as e:
        logger.error(f"LLM integration test failed: {str(e)}")
        return False

async def test_content_generator():
    """Test content generator service."""
    logger.info("Testing content generator...")
    
    try:
        # Create content generator with explicit provider and key
        content_generator = ContentGenerator(llm_provider=DEFAULT_LLM_PROVIDER, api_key=GOOGLE_API_KEY)
        
        # Test bot description generation
        description = await content_generator.generate_bot_description("fan", 25, "Male")
        logger.info(f"Generated bot description: {description}")
        
        # Test comment generation
        comment = await content_generator.generate_comment("fan", "I just got a new car!")
        logger.info(f"Generated comment: {comment}")
        
        # Test post generation
        post = await content_generator.generate_post("fan")
        logger.info(f"Generated post: {post}")
        
        if description and comment and post:
            logger.info("Content generator test passed")
            return True
        else:
            logger.error("Content generator returned empty content")
            return False
    except Exception as e:
        logger.error(f"Content generator test failed: {str(e)}")
        return False

async def test_api_client():
    """Test C# API client."""
    logger.info("Testing API client...")
    
    try:
        # Use mock API client for testing
        api_client = MockCartoucheAPIClient()
        
        # Test getting posts
        async with api_client:
            posts = await api_client.get_posts()
            
        logger.info(f"Retrieved {len(posts)} posts from API")
        
        if posts is not None:
            logger.info("API client test passed")
            return True
        else:
            logger.error("API client returned None")
            return False
    except Exception as e:
        logger.error(f"API client test failed: {str(e)}")
        return False

async def test_bot_manager():
    """Test bot manager service."""
    logger.info("Testing bot manager...")
    
    try:
        # Get database session
        db = next(get_db())
        
        # Create repositories
        bot_repo = BotRepository(db)
        memory_repo = MemoryRepository(db)
        activity_repo = ActivityRepository(db)
        
        # Create services with explicit provider and key
        content_generator = ContentGenerator(llm_provider=DEFAULT_LLM_PROVIDER, api_key=GOOGLE_API_KEY)
        api_client = MockCartoucheAPIClient()
        
        # Create bot manager
        bot_manager = BotManager(
            bot_repository=bot_repo,
            memory_repository=memory_repo,
            activity_repository=activity_repo,
            content_generator=content_generator,
            api_client=api_client
        )
        
        # Test bot creation
        async with api_client:
            bot_data = await bot_manager.create_random_bot()
        
        logger.info(f"Created bot: {bot_data['name']}")
        
        if bot_data:
            logger.info("Bot manager test passed")
            return True
        else:
            logger.error("Bot manager returned None")
            return False
    except Exception as e:
        logger.error(f"Bot manager test failed: {str(e)}")
        return False

async def run_tests():
    """Run all tests."""
    logger.info("Starting tests...")
    
    # Create test results directory
    results_dir = Path("test_results")
    results_dir.mkdir(exist_ok=True)
    
    # Run tests
    test_results = {
        "database": await test_database_connection(),
        "llm": await test_llm_integration(),
        "content_generator": await test_content_generator(),
        "api_client": await test_api_client(),
        "bot_manager": await test_bot_manager()
    }
    
    # Log results
    logger.info("Test results:")
    for test_name, result in test_results.items():
        status = "PASSED" if result else "FAILED"
        logger.info(f"  {test_name}: {status}")
    
    # Write results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(results_dir / f"test_results_{timestamp}.txt", "w") as f:
        f.write(f"Test Results - {datetime.now().isoformat()}\n")
        f.write("=" * 50 + "\n\n")
        
        for test_name, result in test_results.items():
            status = "PASSED" if result else "FAILED"
            f.write(f"{test_name}: {status}\n")
    
    # Return overall result
    return all(test_results.values())

if __name__ == "__main__":
    # Run tests
    result = asyncio.run(run_tests())
    
    # Exit with appropriate code
    sys.exit(0 if result else 1)
