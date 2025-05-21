"""
Bot manager for the Cartouche Bot Service.
Handles bot creation, management, and retrieval.
"""
import logging
import sqlite3
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

from models import Bot
from config import settings

logger = logging.getLogger(__name__)

class BotManager:
    """Manager for bot operations."""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the bot manager.
        
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
            
            # Create bots table if not exists
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS bots (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                full_name TEXT NOT NULL,
                avatar TEXT,
                age INTEGER,
                gender TEXT,
                category TEXT,
                description TEXT,
                created_at TEXT,
                last_active TEXT,
                following TEXT,
                followers_count INTEGER DEFAULT 0,
                posts_count INTEGER DEFAULT 0,
                likes_given INTEGER DEFAULT 0,
                comments_given INTEGER DEFAULT 0,
                reposts_given INTEGER DEFAULT 0,
                like_probability REAL DEFAULT 0.5,
                comment_probability REAL DEFAULT 0.2,
                post_probability REAL DEFAULT 0.1,
                follow_probability REAL DEFAULT 0.3,
                unfollow_probability REAL DEFAULT 0.1,
                repost_probability REAL DEFAULT 0.05
            )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Database initialized successfully")
        
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
    
    def get_all_bots(self) -> List[Dict[str, Any]]:
        """
        Get all bots from the database.
        
        Returns:
            List of bot dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM bots")
            rows = cursor.fetchall()
            
            bots = []
            for row in rows:
                bot_dict = dict(row)
                
                # Convert JSON strings to Python objects
                if bot_dict.get('category'):
                    bot_dict['category'] = json.loads(bot_dict['category'])
                if bot_dict.get('following'):
                    bot_dict['following'] = json.loads(bot_dict['following'])
                
                bots.append(bot_dict)
            
            conn.close()
            return bots
        
        except Exception as e:
            logger.error(f"Error getting all bots: {str(e)}")
            return []
    
    def get_bot(self, bot_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific bot by ID.
        
        Args:
            bot_id: Bot ID
            
        Returns:
            Bot dictionary or None if not found
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM bots WHERE id = ?", (bot_id,))
            row = cursor.fetchone()
            
            if row:
                bot_dict = dict(row)
                
                # Convert JSON strings to Python objects
                if bot_dict.get('category'):
                    bot_dict['category'] = json.loads(bot_dict['category'])
                if bot_dict.get('following'):
                    bot_dict['following'] = json.loads(bot_dict['following'])
                
                conn.close()
                return bot_dict
            
            conn.close()
            return None
        
        except Exception as e:
            logger.error(f"Error getting bot {bot_id}: {str(e)}")
            return None
    
    def add_bot(self, bot: Bot) -> bool:
        """
        Add a new bot to the database.
        
        Args:
            bot: Bot object
            
        Returns:
            Boolean indicating success
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convert Python objects to JSON strings
            category_json = json.dumps(bot.category)
            following_json = json.dumps(bot.following)
            
            cursor.execute('''
            INSERT INTO bots (
                id, name, full_name, avatar, age, gender, category, description,
                created_at, last_active, following, followers_count, posts_count,
                likes_given, comments_given, reposts_given,
                like_probability, comment_probability, post_probability,
                follow_probability, unfollow_probability, repost_probability
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                bot.id, bot.name, bot.full_name, bot.avatar, bot.age, bot.gender,
                category_json, bot.description, bot.created_at.isoformat(),
                bot.last_active.isoformat(), following_json, bot.followers_count,
                bot.posts_count, bot.likes_given, bot.comments_given, bot.reposts_given,
                bot.like_probability, bot.comment_probability, bot.post_probability,
                bot.follow_probability, bot.unfollow_probability, bot.repost_probability
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Added new bot: {bot.name} (ID: {bot.id})")
            return True
        
        except Exception as e:
            logger.error(f"Error adding bot: {str(e)}")
            return False
    
    def update_bot(self, bot_id: int, updates: Dict[str, Any]) -> bool:
        """
        Update a bot in the database.
        
        Args:
            bot_id: Bot ID
            updates: Dictionary of fields to update
            
        Returns:
            Boolean indicating success
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Prepare SET clause and parameters
            set_clause = []
            params = []
            
            for key, value in updates.items():
                # Convert Python objects to JSON strings
                if key == 'category' and isinstance(value, list):
                    value = json.dumps(value)
                elif key == 'following' and isinstance(value, list):
                    value = json.dumps(value)
                elif key in ('created_at', 'last_active') and isinstance(value, datetime):
                    value = value.isoformat()
                
                set_clause.append(f"{key} = ?")
                params.append(value)
            
            # Add bot_id to parameters
            params.append(bot_id)
            
            # Execute update
            cursor.execute(f'''
            UPDATE bots SET {', '.join(set_clause)} WHERE id = ?
            ''', params)
            
            conn.commit()
            conn.close()
            
            logger.info(f"Updated bot {bot_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error updating bot {bot_id}: {str(e)}")
            return False
    
    def delete_bot(self, bot_id: int) -> bool:
        """
        Delete a bot from the database.
        
        Args:
            bot_id: Bot ID
            
        Returns:
            Boolean indicating success
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM bots WHERE id = ?", (bot_id,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Deleted bot {bot_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting bot {bot_id}: {str(e)}")
            return False
    
    def get_next_bot_id(self) -> int:
        """
        Get the next available bot ID.
        
        Returns:
            Next available bot ID
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT MAX(id) FROM bots")
            result = cursor.fetchone()
            
            conn.close()
            
            if result[0] is None:
                return 1
            else:
                return result[0] + 1
        
        except Exception as e:
            logger.error(f"Error getting next bot ID: {str(e)}")
            return 1
    
    def get_bots_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get bots by category.
        
        Args:
            category: Bot category
            
        Returns:
            List of bot dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Use JSON substring matching to find bots with the specified category
            cursor.execute("SELECT * FROM bots WHERE category LIKE ?", (f'%"{category}"%',))
            rows = cursor.fetchall()
            
            bots = []
            for row in rows:
                bot_dict = dict(row)
                
                # Convert JSON strings to Python objects
                if bot_dict.get('category'):
                    bot_dict['category'] = json.loads(bot_dict['category'])
                if bot_dict.get('following'):
                    bot_dict['following'] = json.loads(bot_dict['following'])
                
                bots.append(bot_dict)
            
            conn.close()
            return bots
        
        except Exception as e:
            logger.error(f"Error getting bots by category {category}: {str(e)}")
            return []
    
    def count_bots(self) -> int:
        """
        Count the total number of bots.
        
        Returns:
            Total number of bots
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM bots")
            result = cursor.fetchone()
            
            conn.close()
            
            return result[0] if result else 0
        
        except Exception as e:
            logger.error(f"Error counting bots: {str(e)}")
            return 0
