"""
Scheduler service for the Cartouche Bot Service.
Handles scheduling and execution of background tasks.
"""

from typing import Dict, List, Any, Optional, Callable
import asyncio
from datetime import datetime, timedelta

from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()


class Scheduler:
    """Service for scheduling and executing background tasks."""

    def __init__(self):
        """Initialize the scheduler."""
        self.tasks = {}
        self.running = False
        self.main_task = None

    async def start(self):
        """Start the scheduler."""
        if self.running:
            return

        self.running = True
        self.main_task = asyncio.create_task(self._run_scheduler())
        logger.info("Scheduler started")

    async def stop(self):
        """Stop the scheduler."""
        if not self.running:
            return

        self.running = False
        if self.main_task:
            self.main_task.cancel()
            try:
                await self.main_task
            except asyncio.CancelledError:
                pass
            self.main_task = None

        logger.info("Scheduler stopped")

    async def _run_scheduler(self):
        """Run the scheduler loop."""
        while self.running:
            try:
                now = datetime.utcnow()

                # Find and execute due tasks
                for task_id, task in list(self.tasks.items()):
                    if task["next_run"] <= now:
                        # Schedule next run
                        if task["interval"]:
                            task["next_run"] = now + timedelta(seconds=task["interval"])
                        else:
                            # One-time task
                            del self.tasks[task_id]

                        # Execute task
                        asyncio.create_task(self._execute_task(task_id, task))

                # Sleep for a short time
                await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"Error in scheduler loop: {str(e)}")
                await asyncio.sleep(5)  # Sleep longer on error

    async def _execute_task(self, task_id: str, task: Dict[str, Any]):
        """
        Execute a scheduled task.

        Args:
            task_id: Task ID
            task: Task data
        """
        try:
            logger.debug(f"Executing task {task_id}")
            await task["callback"](*task["args"], **task["kwargs"])
            logger.debug(f"Task {task_id} completed")
        except Exception as e:
            logger.error(f"Error executing task {task_id}: {str(e)}")

    def schedule_task(
        self,
        callback: Callable,
        delay: int = 0,
        interval: Optional[int] = None,
        task_id: Optional[str] = None,
        *args,
        **kwargs,
    ) -> str:
        """
        Schedule a task.

        Args:
            callback: Async function to call
            delay: Delay in seconds before first execution
            interval: Interval in seconds between executions (None for one-time task)
            task_id: Optional task ID (generated if not provided)
            *args: Arguments to pass to the callback
            **kwargs: Keyword arguments to pass to the callback

        Returns:
            Task ID
        """
        if task_id is None:
            task_id = f"task_{len(self.tasks)}_{datetime.utcnow().timestamp()}"

        self.tasks[task_id] = {
            "callback": callback,
            "next_run": datetime.utcnow() + timedelta(seconds=delay),
            "interval": interval,
            "args": args,
            "kwargs": kwargs,
        }

        logger.info(
            f"Scheduled task {task_id} with delay {delay}s and interval {interval}s"
        )

        return task_id

    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a scheduled task.

        Args:
            task_id: Task ID

        Returns:
            True if task was cancelled, False if not found
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            logger.info(f"Cancelled task {task_id}")
            return True

        return False

    def get_scheduled_tasks(self) -> List[Dict[str, Any]]:
        """
        Get all scheduled tasks.

        Returns:
            List of scheduled tasks
        """
        return [
            {
                "task_id": task_id,
                "next_run": task["next_run"].isoformat(),
                "interval": task["interval"],
            }
            for task_id, task in self.tasks.items()
        ]
