"""
Memory service for the Cartouche Bot Service.
Handles storage and retrieval of bot interaction history.
"""
import logging
import sqlite3
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

from config import settings

logger = logging.getLogger(__name__)

class MemoryService:
    """Service for bot memory operations."""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the memory service.
        
        Args:
            db_path: Path to the SQLite database file. If not provided, uses the one from settings.
        """
        self.db_path = db_path or settings.DB_PATH
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize the database with required tables."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create interactions table if not exists
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_id INTEGER NOT NULL,
                target_id TEXT NOT NULL,
                interaction_type TEXT NOT NULL,
                content TEXT,
                timestamp TEXT NOT NULL
            )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Memory database initialized successfully")
        
        except Exception as e:
            logger.error(f"Error initializing memory database: {str(e)}")
    
    def add_interaction(self, bot_id: int, target_id: str, interaction_type: str, content: Optional[str] = None) -> bool:
        """
        Add a new interaction to the memory.
        
        Args:
            bot_id: Bot ID
            target_id: Target ID (user or bot)
            interaction_type: Type of interaction (like, comment, follow, etc.)
            content: Optional content of the interaction
            
        Returns:
            Boolean indicating success
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO interactions (bot_id, target_id, interaction_type, content, timestamp)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                bot_id,
                target_id,
                interaction_type,
                content,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Added interaction: Bot {bot_id} -> {interaction_type} -> {target_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error adding interaction: {str(e)}")
            return False
    
    def get_interaction_history(self, bot_id: int, target_id: str, limit: int = 10) -> str:
        """
        Get interaction history between a bot and a target.
        
        Args:
            bot_id: Bot ID
            target_id: Target ID (user or bot)
            limit: Maximum number of interactions to retrieve
            
        Returns:
            String representation of interaction history
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT interaction_type, content, timestamp
            FROM interactions
            WHERE bot_id = ? AND target_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
            ''', (bot_id, target_id, limit))
            
            rows = cursor.fetchall()
            
            conn.close()
            
            # Format history as string
            history = []
            for interaction_type, content, timestamp in rows:
                dt = datetime.fromisoformat(timestamp)
                formatted_time = dt.strftime("%Y-%m-%d %H:%M")
                
                if content:
                    history.append(f"{interaction_type.upper()} ({formatted_time}): {content}")
                else:
                    history.append(f"{interaction_type.upper()} ({formatted_time})")
            
            return "\n".join(history)
        
        except Exception as e:
            logger.error(f"Error getting interaction history: {str(e)}")
            return ""
    
    def get_all_interactions(self, bot_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get all interactions for a bot.
        
        Args:
            bot_id: Bot ID
            limit: Maximum number of interactions to retrieve
            
        Returns:
            List of interaction dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, target_id, interaction_type, content, timestamp
            FROM interactions
            WHERE bot_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
            ''', (bot_id, limit))
            
            rows = cursor.fetchall()
            
            interactions = []
            for row in rows:
                interactions.append(dict(row))
            
            conn.close()
            return interactions
        
        except Exception as e:
            logger.error(f"Error getting all interactions: {str(e)}")
            return []
    
    def get_interactions_by_type(self, bot_id: int, interaction_type: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get interactions of a specific type for a bot.
        
        Args:
            bot_id: Bot ID
            interaction_type: Type of interaction (like, comment, follow, etc.)
            limit: Maximum number of interactions to retrieve
            
        Returns:
            List of interaction dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, target_id, content, timestamp
            FROM interactions
            WHERE bot_id = ? AND interaction_type = ?
            ORDER BY timestamp DESC
            LIMIT ?
            ''', (bot_id, interaction_type, limit))
            
            rows = cursor.fetchall()
            
            interactions = []
            for row in rows:
                interactions.append(dict(row))
            
            conn.close()
            return interactions
        
        except Exception as e:
            logger.error(f"Error getting interactions by type: {str(e)}")
            return []
    
    def clear_old_interactions(self, days: int = 30) -> bool:
        """
        Clear interactions older than a specified number of days.
        
        Args:
            days: Number of days to keep
            
        Returns:
            Boolean indicating success
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calculate cutoff date
            cutoff_date = (datetime.now() - datetime.timedelta(days=days)).isoformat()
            
            cursor.execute('''
            DELETE FROM interactions
            WHERE timestamp < ?
            ''', (cutoff_date,))
            
            deleted_count = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            logger.info(f"Cleared {deleted_count} old interactions")
            return True
        
        except Exception as e:
            logger.error(f"Error clearing old interactions: {str(e)}")
            return False
