"""
Activity repository for the Cartouche Bot Service.
Handles database operations for bot activities.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.db.models import BotActivity
from app.core.exceptions import DatabaseError


class ActivityRepository:
    """Repository for bot activity operations."""

    def __init__(self, db: Session):
        """
        Initialize the repository.

        Args:
            db: Database session
        """
        self.db = db

    def get_activities_by_bot_id(
        self, bot_id: int, skip: int = 0, limit: int = 100
    ) -> List[BotActivity]:
        """
        Get activities for a specific bot.

        Args:
            bot_id: Bot ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of activities
        """
        return (
            self.db.query(BotActivity)
            .filter(BotActivity.bot_id == bot_id)
            .order_by(desc(BotActivity.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_activity_by_id(self, activity_id: int) -> Optional[BotActivity]:
        """
        Get an activity by ID.

        Args:
            activity_id: Activity ID

        Returns:
            Activity or None if not found
        """
        return self.db.query(BotActivity).filter(BotActivity.id == activity_id).first()

    def create_activity(self, activity_data: Dict[str, Any]) -> BotActivity:
        """
        Create a new activity.

        Args:
            activity_data: Activity data dictionary

        Returns:
            Created activity

        Raises:
            DatabaseError: If activity creation fails
        """
        try:
            activity = BotActivity(**activity_data)
            self.db.add(activity)
            self.db.commit()
            self.db.refresh(activity)
            return activity
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create activity: {str(e)}")

    def delete_activity(self, activity_id: int) -> bool:
        """
        Delete an activity.

        Args:
            activity_id: Activity ID

        Returns:
            True if successful

        Raises:
            DatabaseError: If activity deletion fails
        """
        try:
            activity = self.get_activity_by_id(activity_id)
            if not activity:
                raise DatabaseError(f"Activity with ID {activity_id} not found")

            self.db.delete(activity)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to delete activity: {str(e)}")

    def get_activities_by_type(
        self, bot_id: int, activity_type: str, skip: int = 0, limit: int = 100
    ) -> List[BotActivity]:
        """
        Get activities by type.

        Args:
            bot_id: Bot ID
            activity_type: Activity type (like, comment, follow, unfollow, post)
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of activities
        """
        return (
            self.db.query(BotActivity)
            .filter(
                BotActivity.bot_id == bot_id, BotActivity.activity_type == activity_type
            )
            .order_by(desc(BotActivity.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_activities_by_target(
        self, bot_id: int, target_id: str
    ) -> List[BotActivity]:
        """
        Get activities by target.

        Args:
            bot_id: Bot ID
            target_id: Target ID (post ID, user ID)

        Returns:
            List of activities
        """
        return (
            self.db.query(BotActivity)
            .filter(BotActivity.bot_id == bot_id, BotActivity.target_id == target_id)
            .order_by(desc(BotActivity.created_at))
            .all()
        )

    def check_activity_exists(
        self, bot_id: int, activity_type: str, target_id: str
    ) -> bool:
        """
        Check if an activity exists.

        Args:
            bot_id: Bot ID
            activity_type: Activity type
            target_id: Target ID

        Returns:
            True if activity exists
        """
        return (
            self.db.query(BotActivity)
            .filter(
                BotActivity.bot_id == bot_id,
                BotActivity.activity_type == activity_type,
                BotActivity.target_id == target_id,
            )
            .first()
            is not None
        )

    def count_activities_by_bot(self, bot_id: int) -> int:
        """
        Count activities for a specific bot.

        Args:
            bot_id: Bot ID

        Returns:
            Activity count
        """
        return (
            self.db.query(func.count(BotActivity.id))
            .filter(BotActivity.bot_id == bot_id)
            .scalar()
        )

    def count_activities_by_type(self, bot_id: int, activity_type: str) -> int:
        """
        Count activities by type for a specific bot.

        Args:
            bot_id: Bot ID
            activity_type: Activity type

        Returns:
            Activity count
        """
        return (
            self.db.query(func.count(BotActivity.id))
            .filter(
                BotActivity.bot_id == bot_id, BotActivity.activity_type == activity_type
            )
            .scalar()
        )

    def get_recent_activities(self, limit: int = 100) -> List[BotActivity]:
        """
        Get recent activities across all bots.

        Args:
            limit: Maximum number of records to return

        Returns:
            List of activities
        """
        return (
            self.db.query(BotActivity)
            .order_by(desc(BotActivity.created_at))
            .limit(limit)
            .all()
        )
