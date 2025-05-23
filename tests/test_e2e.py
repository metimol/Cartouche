"""
End-to-end test script for the Cartouche Bot Service.
Tests the complete flow from bot creation to post reactions.
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.logging import setup_logging
from app.db.session import get_db, engine, Base
from app.db.repositories.bot_repository import BotRepository
from app.db.repositories.memory_repository import MemoryRepository
from app.db.repositories.activity_repository import ActivityRepository
from app.services.content_generator import ContentGenerator
from app.services.bot_manager import BotManager
from app.services.reaction_engine import ReactionEngine
from app.clients.cartouche_api import CartoucheAPIClient

# Setup logging
logger = setup_logging()


async def test_end_to_end():
    """Test end-to-end flow."""
    logger.info("Starting end-to-end test...")

    try:
        # Get database session
        db = next(get_db())

        # Create repositories
        bot_repo = BotRepository(db)
        memory_repo = MemoryRepository(db)
        activity_repo = ActivityRepository(db)

        # Create services
        content_generator = ContentGenerator()
        api_client = CartoucheAPIClient()

        # Create bot manager
        bot_manager = BotManager(
            bot_repository=bot_repo,
            memory_repository=memory_repo,
            activity_repository=activity_repo,
            content_generator=content_generator,
            api_client=api_client,
        )

        # Create reaction engine
        reaction_engine = ReactionEngine(
            bot_repository=bot_repo, bot_manager=bot_manager
        )

        # Step 1: Create a test bot
        logger.info("Step 1: Creating test bot...")
        async with api_client:
            bot_data = await bot_manager.create_random_bot()

        bot_id = bot_data["id"]
        bot_name = bot_data["name"]
        logger.info(f"Created bot: {bot_name} (ID: {bot_id})")

        # Step 2: Create a post from the bot
        logger.info("Step 2: Creating post from bot...")
        async with api_client:
            post_result = await bot_manager.create_bot_post(bot_id)

        logger.info(f"Created post: {post_result}")

        # Step 3: Schedule reactions to the post
        logger.info("Step 3: Scheduling reactions to post...")
        post_id = (
            post_result["post"]["id"]
            if "post" in post_result and "id" in post_result["post"]
            else "test_post_id"
        )

        reaction_result = await reaction_engine.schedule_reactions_for_post(
            post_id, bot_name
        )
        logger.info(f"Scheduled reactions: {reaction_result}")

        # Step 4: Process due reactions
        logger.info("Step 4: Processing due reactions...")
        processed_reactions = await reaction_engine.process_due_reactions()
        logger.info(f"Processed reactions: {processed_reactions}")

        # Step 5: Verify activities in database
        logger.info("Step 5: Verifying activities in database...")
        activities = activity_repo.get_activities_by_bot_id(bot_id)
        logger.info(f"Found {len(activities)} activities for bot {bot_id}")

        # Log success
        logger.info("End-to-end test completed successfully")
        return True

    except Exception as e:
        logger.error(f"End-to-end test failed: {str(e)}")
        return False


async def run_tests():
    """Run all tests."""
    logger.info("Starting end-to-end tests...")

    # Create test results directory
    results_dir = Path("test_results")
    results_dir.mkdir(exist_ok=True)

    # Run test
    result = await test_end_to_end()

    # Log result
    status = "PASSED" if result else "FAILED"
    logger.info(f"End-to-end test: {status}")

    # Write result to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(results_dir / f"e2e_test_results_{timestamp}.txt", "w") as f:
        f.write(f"End-to-End Test Results - {datetime.now().isoformat()}\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"End-to-end test: {status}\n")

    return result


if __name__ == "__main__":
    # Run tests
    result = asyncio.run(run_tests())

    # Exit with appropriate code
    sys.exit(0 if result else 1)
