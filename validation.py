"""
Validation module for the Cartouche Autonomous Service.
Tests long-term autonomy and performance.
"""
import os
import asyncio
import logging
import json
import time
from datetime import datetime, timedelta

from api_client import APIClient
from database import Database
from bot_manager import BotManager
from content_generator import ContentGenerator
from reaction_engine import ReactionEngine
from monitor import Monitor
from memory import Memory
from config import INITIAL_BOTS_COUNT, DAILY_BOTS_GROWTH_MIN

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('validation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ValidationMetrics:
    """Class to track validation metrics."""
    
    def __init__(self):
        """Initialize metrics."""
        self.start_time = datetime.now()
        self.end_time = None
        self.duration = None
        self.bot_count_start = 0
        self.bot_count_end = 0
        self.posts_processed = 0
        self.likes_given = 0
        self.comments_given = 0
        self.reposts_given = 0
        self.errors = []
        self.api_calls = 0
        self.api_errors = 0
        self.memory_operations = 0
    
    def to_dict(self):
        """Convert metrics to dictionary."""
        return {
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration.total_seconds() if self.duration else None,
            "bot_count_start": self.bot_count_start,
            "bot_count_end": self.bot_count_end,
            "bot_growth": self.bot_count_end - self.bot_count_start,
            "posts_processed": self.posts_processed,
            "likes_given": self.likes_given,
            "comments_given": self.comments_given,
            "reposts_given": self.reposts_given,
            "errors": self.errors,
            "api_calls": self.api_calls,
            "api_errors": self.api_errors,
            "memory_operations": self.memory_operations
        }

async def validate_autonomy(duration_minutes=30):
    """
    Validate system autonomy by running it for a specified duration.
    
    Args:
        duration_minutes: Duration in minutes to run the validation
    
    Returns:
        ValidationMetrics object
    """
    logger.info(f"Starting autonomy validation for {duration_minutes} minutes...")
    
    metrics = ValidationMetrics()
    
    try:
        # Initialize components
        database = Database()
        api_client = APIClient()
        content_generator = ContentGenerator()
        memory = Memory()
        bot_manager = BotManager(database, api_client)
        reaction_engine = ReactionEngine(database, api_client, content_generator)
        monitor = Monitor(database, api_client, reaction_engine)
        
        # Count initial bots
        metrics.bot_count_start = await database.count_bots()
        
        # If no bots exist, initialize them
        if metrics.bot_count_start == 0:
            logger.info("No bots found, initializing...")
            await bot_manager.initialize_bots()
            metrics.bot_count_start = await database.count_bots()
        
        logger.info(f"Starting with {metrics.bot_count_start} bots")
        
        # Start monitor
        await monitor.start()
        
        # Define a custom API client to track API calls
        class TrackingAPIClient(APIClient):
            async def get_posts(self, *args, **kwargs):
                metrics.api_calls += 1
                try:
                    result = await super().get_posts(*args, **kwargs)
                    return result
                except Exception as e:
                    metrics.api_errors += 1
                    raise
        
        tracking_api_client = TrackingAPIClient()
        
        # Run for specified duration
        end_time = datetime.now() + timedelta(minutes=duration_minutes)
        
        while datetime.now() < end_time:
            try:
                # Simulate bot growth (accelerated for validation)
                if datetime.now().minute % 5 == 0:  # Every 5 minutes
                    new_bots = await bot_manager.grow_bot_population()
                    logger.info(f"Added {new_bots} new bots")
                
                # Simulate subscription processing
                if datetime.now().minute % 3 == 0:  # Every 3 minutes
                    actions = await bot_manager.process_subscriptions()
                    logger.info(f"Processed {actions} subscription actions")
                
                # Get some posts to process manually (in addition to monitor)
                async with tracking_api_client as client:
                    posts = await client.get_posts()
                
                if posts:
                    # Process a random post
                    import random
                    post = random.choice(posts)
                    result = await reaction_engine.process_post(post)
                    
                    # Update metrics
                    metrics.posts_processed += 1
                    metrics.likes_given += result.get('likes', 0)
                    metrics.comments_given += result.get('comments', 0)
                    metrics.reposts_given += result.get('reposts', 0)
                    
                    logger.info(f"Manually processed post {post.get('id')}: {result}")
                
                # Simulate memory operations
                if datetime.now().minute % 2 == 0:  # Every 2 minutes
                    # Get a random bot
                    bots = await database.get_bots()
                    if bots:
                        bot = random.choice(bots)
                        
                        # Store a memory
                        memory_text = f"Validation test memory at {datetime.now().isoformat()}"
                        await memory.store_memory(bot['id'], memory_text)
                        
                        # Retrieve memories
                        memories = await memory.retrieve_memories(bot['id'], "test")
                        
                        metrics.memory_operations += 2  # One store, one retrieve
                
                # Wait before next iteration
                await asyncio.sleep(30)
            
            except Exception as e:
                error_msg = f"Error during validation: {str(e)}"
                logger.error(error_msg)
                metrics.errors.append(error_msg)
                await asyncio.sleep(60)  # Wait longer on error
        
        # Stop monitor
        await monitor.stop()
        
        # Count final bots
        metrics.bot_count_end = await database.count_bots()
        
        # Calculate duration
        metrics.end_time = datetime.now()
        metrics.duration = metrics.end_time - metrics.start_time
        
        logger.info(f"Validation completed. Duration: {metrics.duration}")
        logger.info(f"Bot growth: {metrics.bot_count_start} -> {metrics.bot_count_end}")
        logger.info(f"Posts processed: {metrics.posts_processed}")
        logger.info(f"Reactions: {metrics.likes_given} likes, {metrics.comments_given} comments, {metrics.reposts_given} reposts")
        
        # Save metrics to file
        with open('validation_metrics.json', 'w') as f:
            json.dump(metrics.to_dict(), f, indent=2)
        
        return metrics
    
    except Exception as e:
        error_msg = f"Validation failed: {str(e)}"
        logger.error(error_msg)
        metrics.errors.append(error_msg)
        
        # Calculate duration even on failure
        metrics.end_time = datetime.now()
        metrics.duration = metrics.end_time - metrics.start_time
        
        # Save metrics to file
        with open('validation_metrics.json', 'w') as f:
            json.dump(metrics.to_dict(), f, indent=2)
        
        return metrics

async def validate_performance():
    """
    Validate system performance by measuring response times.
    
    Returns:
        Dictionary with performance metrics
    """
    logger.info("Starting performance validation...")
    
    performance = {
        "api_response_times": [],
        "content_generation_times": [],
        "database_operation_times": [],
        "memory_operation_times": []
    }
    
    try:
        # Initialize components
        database = Database()
        api_client = APIClient()
        content_generator = ContentGenerator()
        memory = Memory()
        
        # Test API response times
        for _ in range(5):
            start_time = time.time()
            async with api_client as client:
                await client.get_posts()
            end_time = time.time()
            performance["api_response_times"].append(end_time - start_time)
        
        # Test content generation times
        bot_profile = {
            "name": "perftest",
            "full_name": "Performance Test",
            "age": 30,
            "gender": "Other",
            "categories": ["neutral"],
            "description": "A test bot for performance testing"
        }
        
        for _ in range(5):
            start_time = time.time()
            await content_generator.generate_comment(bot_profile, "Test post content")
            end_time = time.time()
            performance["content_generation_times"].append(end_time - start_time)
        
        # Test database operation times
        for _ in range(5):
            start_time = time.time()
            await database.get_bots()
            end_time = time.time()
            performance["database_operation_times"].append(end_time - start_time)
        
        # Test memory operation times
        test_bot_id = 9999
        for i in range(5):
            start_time = time.time()
            await memory.store_memory(test_bot_id, f"Performance test memory {i}")
            await memory.retrieve_memories(test_bot_id, "test")
            end_time = time.time()
            performance["memory_operation_times"].append(end_time - start_time)
        
        # Calculate averages
        for key in performance:
            if performance[key]:
                performance[f"{key}_avg"] = sum(performance[key]) / len(performance[key])
        
        logger.info("Performance validation completed")
        logger.info(f"Average API response time: {performance.get('api_response_times_avg', 0):.4f} seconds")
        logger.info(f"Average content generation time: {performance.get('content_generation_times_avg', 0):.4f} seconds")
        logger.info(f"Average database operation time: {performance.get('database_operation_times_avg', 0):.4f} seconds")
        logger.info(f"Average memory operation time: {performance.get('memory_operation_times_avg', 0):.4f} seconds")
        
        # Save performance metrics to file
        with open('performance_metrics.json', 'w') as f:
            json.dump(performance, f, indent=2)
        
        return performance
    
    except Exception as e:
        error_msg = f"Performance validation failed: {str(e)}"
        logger.error(error_msg)
        performance["error"] = error_msg
        
        # Save performance metrics to file
        with open('performance_metrics.json', 'w') as f:
            json.dump(performance, f, indent=2)
        
        return performance

async def run_validation():
    """Run all validation tests."""
    logger.info("Starting validation...")
    
    # Run autonomy validation
    autonomy_metrics = await validate_autonomy(duration_minutes=10)
    
    # Run performance validation
    performance_metrics = await validate_performance()
    
    # Combine results
    validation_results = {
        "autonomy": autonomy_metrics.to_dict(),
        "performance": performance_metrics,
        "timestamp": datetime.now().isoformat(),
        "success": len(autonomy_metrics.errors) == 0 and "error" not in performance_metrics
    }
    
    # Save combined results
    with open('validation_results.json', 'w') as f:
        json.dump(validation_results, f, indent=2)
    
    logger.info(f"Validation completed. Success: {validation_results['success']}")
    return validation_results

if __name__ == "__main__":
    asyncio.run(run_validation())
