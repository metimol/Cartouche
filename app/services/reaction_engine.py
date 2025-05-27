"""
Reaction engine service for the Cartouche Bot Service.
Handles scheduling and processing of bot reactions to posts.
"""

from typing import Dict, List, Any
import random
from datetime import datetime, timedelta

from app.db.repositories.bot_repository import BotRepository
from app.services.bot_manager import BotManager
from app.core.settings import REACTION_DELAY_MIN, REACTION_DELAY_MAX

from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()


class ReactionEngine:
    """Service for scheduling and processing bot reactions."""

    def __init__(self, bot_repository: BotRepository, bot_manager: BotManager):
        """
        Initialize the reaction engine.

        Args:
            bot_repository: Bot repository
            bot_manager: Bot manager
        """
        self.bot_repository = bot_repository
        self.bot_manager = bot_manager
        self.scheduled_tasks = {}

    async def schedule_reactions_for_post(
        self, post_id: str, post_author: str
    ) -> Dict[str, Any]:
        """
        Schedule reactions for a new post.

        Args:
            post_id: Post ID
            post_author: Post author name

        Returns:
            Scheduling result
        """
        # Get all bots
        bots = self.bot_repository.get_all_bots()

        # Filter out the author if it's a bot
        bots = [bot for bot in bots if bot.name != post_author]

        # Determine which bots will see the post (random subset)
        visibility_ratio = random.uniform(0.3, 0.8)  # 30-80% of bots will see the post
        visible_bots = random.sample(bots, int(len(bots) * visibility_ratio))

        scheduled_count = 0
        for bot in visible_bots:
            # Determine if bot will react
            will_react = random.random() < max(
                bot.like_probability, bot.comment_probability
            )

            if will_react:
                # Schedule reaction with random delay
                delay = random.randint(REACTION_DELAY_MIN, REACTION_DELAY_MAX)

                # Create task ID
                task_id = f"{bot.id}_{post_id}_{datetime.utcnow().timestamp()}"

                # Schedule task
                self.scheduled_tasks[task_id] = {
                    "bot_id": bot.id,
                    "post_id": post_id,
                    "scheduled_time": datetime.utcnow() + timedelta(seconds=delay),
                }

                scheduled_count += 1
                logger.info(
                    f"Scheduled reaction for bot {bot.name} to post {post_id} in {delay} seconds"
                )

        return {
            "post_id": post_id,
            "total_bots": len(bots),
            "visible_bots": len(visible_bots),
            "scheduled_reactions": scheduled_count,
        }

    async def process_due_reactions(self) -> List[Dict[str, Any]]:
        """
        Process all due reactions.

        Returns:
            List of processed reactions
        """
        now = datetime.utcnow()
        due_tasks = []

        # Find due tasks
        for task_id, task in list(self.scheduled_tasks.items()):
            if task["scheduled_time"] <= now:
                due_tasks.append((task_id, task))
                del self.scheduled_tasks[task_id]

        results = []
        for task_id, task in due_tasks:
            try:
                # Process bot activity
                result = await self.bot_manager.process_bot_activity(task["bot_id"])
                results.append(
                    {"task_id": task_id, "result": result, "status": "success"}
                )
            except Exception as e:
                logger.error(f"Failed to process reaction task {task_id}: {str(e)}")
                results.append({"task_id": task_id, "error": str(e), "status": "error"})

        return results

    def get_pending_reactions_count(self) -> int:
        """
        Get count of pending reactions.

        Returns:
            Number of pending reactions
        """
        return len(self.scheduled_tasks)

    def get_scheduled_reactions(self) -> List[Dict[str, Any]]:
        """
        Get all scheduled reactions.

        Returns:
            List of scheduled reactions
        """
        return [
            {
                "task_id": task_id,
                "bot_id": task["bot_id"],
                "post_id": task["post_id"],
                "scheduled_time": task["scheduled_time"].isoformat(),
            }
            for task_id, task in self.scheduled_tasks.items()
        ]
