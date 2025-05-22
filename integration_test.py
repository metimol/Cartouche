"""
Integration test module for the Cartouche Autonomous Service.
Tests integration with the main C# service.
"""
import os
import asyncio
import logging
import json
from datetime import datetime

from api_client import APIClient
from database import Database
from bot_manager import BotManager
from content_generator import ContentGenerator
from reaction_engine import ReactionEngine
from monitor import Monitor
from memory import Memory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('integration_test.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def test_api_connection():
    """Test connection to the C# API."""
    logger.info("Testing API connection...")
    
    try:
        async with APIClient() as client:
            # Test getting posts
            posts = await client.get_posts()
            logger.info(f"Successfully retrieved {len(posts)} posts")
            
            # Test getting users
            users = await client.get_users()
            logger.info(f"Successfully retrieved {len(users)} users")
            
            return True
    
    except Exception as e:
        logger.error(f"API connection test failed: {str(e)}")
        return False

async def test_bot_creation():
    """Test bot creation."""
    logger.info("Testing bot creation...")
    
    try:
        database = Database()
        api_client = APIClient()
        bot_manager = BotManager(database, api_client)
        
        # Create a test bot
        bot_id = await bot_manager.create_bot()
        
        if bot_id > 0:
            logger.info(f"Successfully created bot with ID {bot_id}")
            
            # Get bot from database
            bot = await database.get_bot(bot_id)
            logger.info(f"Bot details: {bot.get('name')}, {bot.get('full_name')}")
            
            return True
        else:
            logger.error("Failed to create bot")
            return False
    
    except Exception as e:
        logger.error(f"Bot creation test failed: {str(e)}")
        return False

async def test_content_generation():
    """Test content generation."""
    logger.info("Testing content generation...")
    
    try:
        content_generator = ContentGenerator()
        
        # Test bot profile
        bot_profile = {
            "name": "testbot123",
            "full_name": "Test Bot",
            "age": 30,
            "gender": "Other",
            "categories": ["neutral", "humorous"],
            "description": "A test bot for integration testing"
        }
        
        # Test post content
        post_content = "This is a test post for integration testing. What do you think about autonomous AI systems?"
        
        # Generate comment
        comment = await content_generator.generate_comment(bot_profile, post_content)
        logger.info(f"Generated comment: {comment}")
        
        # Generate post
        post = await content_generator.generate_post(bot_profile, ["technology", "AI"])
        logger.info(f"Generated post: {post}")
        
        return True
    
    except Exception as e:
        logger.error(f"Content generation test failed: {str(e)}")
        return False

async def test_post_reaction():
    """Test post reaction."""
    logger.info("Testing post reaction...")
    
    try:
        database = Database()
        api_client = APIClient()
        content_generator = ContentGenerator()
        reaction_engine = ReactionEngine(database, api_client, content_generator)
        
        # Get a post from the API
        async with api_client as client:
            posts = await client.get_posts()
            
            if not posts:
                logger.error("No posts available for testing")
                return False
            
            # Process the first post
            post = posts[0]
            result = await reaction_engine.process_post(post)
            
            logger.info(f"Post reaction result: {result}")
            
            return True
    
    except Exception as e:
        logger.error(f"Post reaction test failed: {str(e)}")
        return False

async def test_memory_storage():
    """Test memory storage and retrieval."""
    logger.info("Testing memory storage and retrieval...")
    
    try:
        memory = Memory()
        
        # Test memory storage
        test_bot_id = 999
        test_memory = "This is a test memory for integration testing."
        test_metadata = {"type": "test", "timestamp": datetime.now().isoformat()}
        
        success = await memory.store_memory(test_bot_id, test_memory, test_metadata)
        
        if not success:
            logger.error("Failed to store memory")
            return False
        
        # Test memory retrieval
        memories = await memory.retrieve_memories(test_bot_id, "test memory")
        
        if memories:
            logger.info(f"Retrieved {len(memories)} memories")
            logger.info(f"First memory: {memories[0]['content']}")
            return True
        else:
            logger.error("Failed to retrieve memories")
            return False
    
    except Exception as e:
        logger.error(f"Memory storage test failed: {str(e)}")
        return False

async def test_monitor():
    """Test monitor functionality."""
    logger.info("Testing monitor functionality...")
    
    try:
        database = Database()
        api_client = APIClient()
        content_generator = ContentGenerator()
        reaction_engine = ReactionEngine(database, api_client, content_generator)
        monitor = Monitor(database, api_client, reaction_engine)
        
        # Start monitor
        await monitor.start()
        
        # Wait for a short time to allow monitor to process posts
        logger.info("Monitor started, waiting for 10 seconds...")
        await asyncio.sleep(10)
        
        # Stop monitor
        await monitor.stop()
        
        logger.info("Monitor test completed")
        return True
    
    except Exception as e:
        logger.error(f"Monitor test failed: {str(e)}")
        return False

async def run_integration_tests():
    """Run all integration tests."""
    logger.info("Starting integration tests...")
    
    tests = [
        ("API Connection", test_api_connection),
        ("Bot Creation", test_bot_creation),
        ("Content Generation", test_content_generation),
        ("Post Reaction", test_post_reaction),
        ("Memory Storage", test_memory_storage),
        ("Monitor Functionality", test_monitor)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"Running test: {test_name}")
        try:
            result = await test_func()
            results[test_name] = "PASS" if result else "FAIL"
        except Exception as e:
            logger.error(f"Test {test_name} raised an exception: {str(e)}")
            results[test_name] = "ERROR"
    
    # Log results
    logger.info("Integration test results:")
    for test_name, result in results.items():
        logger.info(f"{test_name}: {result}")
    
    # Save results to file
    with open('integration_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Return overall success
    return all(result == "PASS" for result in results.values())

if __name__ == "__main__":
    asyncio.run(run_integration_tests())
