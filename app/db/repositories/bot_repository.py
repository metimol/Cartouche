"""
Bot repository for the Cartouche Bot Service.
Handles database operations for bots.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.exceptions import DatabaseError
from app.db.models import Bot


class BotRepository:
    """Repository for bot operations."""

    def __init__(self, db: Session):
        """
        Initialize the repository.

        Args:
            db: Database session
        """
        self.db = db

    def get_all_bots(self, skip: int = 0, limit: int = 100) -> List[Bot]:
        """
        Get all bots with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of bots
        """
        return self.db.query(Bot).offset(skip).limit(limit).all()

    def get_bot_by_id(self, bot_id: int) -> Optional[Bot]:
        """
        Get a bot by ID.

        Args:
            bot_id: Bot ID

        Returns:
            Bot or None if not found
        """
        return self.db.query(Bot).filter(Bot.id == bot_id).first()

    def get_bot_by_name(self, name: str) -> Optional[Bot]:
        """
        Get a bot by name.

        Args:
            name: Bot name

        Returns:
            Bot or None if not found
        """
        return self.db.query(Bot).filter(Bot.name == name).first()

    def create_bot(self, bot_data: Dict[str, Any]) -> Bot:
        """
        Create a new bot.

        Args:
            bot_data: Bot data dictionary

        Returns:
            Created bot

        Raises:
            DatabaseError: If bot creation fails
        """
        try:
            bot = Bot(**bot_data)
            self.db.add(bot)
            self.db.commit()
            self.db.refresh(bot)
            return bot
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create bot: {str(e)}")

    def update_bot(self, bot_id: int, bot_data: Dict[str, Any]) -> Bot:
        """
        Update a bot.

        Args:
            bot_id: Bot ID
            bot_data: Bot data dictionary

        Returns:
            Updated bot

        Raises:
            DatabaseError: If bot update fails
        """
        try:
            bot = self.get_bot_by_id(bot_id)
            if not bot:
                raise DatabaseError(f"Bot with ID {bot_id} not found")

            for key, value in bot_data.items():
                setattr(bot, key, value)

            self.db.commit()
            self.db.refresh(bot)
            return bot
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to update bot: {str(e)}")

    def delete_bot(self, bot_id: int) -> bool:
        """
        Delete a bot.

        Args:
            bot_id: Bot ID

        Returns:
            True if successful

        Raises:
            DatabaseError: If bot deletion fails
        """
        try:
            bot = self.get_bot_by_id(bot_id)
            if not bot:
                raise DatabaseError(f"Bot with ID {bot_id} not found")

            self.db.delete(bot)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to delete bot: {str(e)}")

    def update_last_active(self, bot_id: int) -> Bot:
        """
        Update the last active timestamp of a bot.

        Args:
            bot_id: Bot ID

        Returns:
            Updated bot

        Raises:
            DatabaseError: If update fails
        """
        try:
            bot = self.get_bot_by_id(bot_id)
            if not bot:
                raise DatabaseError(f"Bot with ID {bot_id} not found")

            bot.last_active = datetime.utcnow()
            self.db.commit()
            self.db.refresh(bot)
            return bot
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to update bot last active: {str(e)}")

    def get_bots_by_category(
        self, category: str, skip: int = 0, limit: int = 100
    ) -> List[Bot]:
        """
        Get bots by category.

        Args:
            category: Bot category
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of bots
        """
        return (
            self.db.query(Bot)
            .filter(Bot.category == category)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_bots(
        self, hours: int = 24, skip: int = 0, limit: int = 100
    ) -> List[Bot]:
        """
        Get bots active within the last N hours.

        Args:
            hours: Number of hours
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of bots
        """
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        return (
            self.db.query(Bot)
            .filter(Bot.last_active >= cutoff)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_bots(self) -> int:
        """
        Count total number of bots.

        Returns:
            Bot count
        """
        return self.db.query(func.count(Bot.id)).scalar()

    def count_bots_by_category(self) -> Dict[str, int]:
        """
        Count bots by category.

        Returns:
            Dictionary with category counts
        """
        result = (
            self.db.query(Bot.category, func.count(Bot.id)).group_by(Bot.category).all()
        )
        return {category: count for category, count in result}
