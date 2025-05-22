"""
Database module for the Cartouche Autonomous Service.
Handles database operations and provides an interface for storing and retrieving data.
"""
import logging
import sqlite3
import json
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import aiosqlite

from config import DB_PATH

logger = logging.getLogger(__name__)

class Database:
    """Database manager for the Cartouche Autonomous Service."""
    
    def __init__(self, db_path: str = DB_PATH):
        """
        Initialize the database manager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize the database with required tables."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create bots table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS bots (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                full_name TEXT NOT NULL,
                avatar TEXT,
                age INTEGER,
                gender TEXT,
                categories TEXT,
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
                repost_probability REAL DEFAULT 0.05,
                api_data TEXT
            )
            ''')
            
            # Create posts table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                post_id INTEGER,
                user_name TEXT,
                full_name TEXT,
                avatar TEXT,
                text TEXT,
                on_date TEXT,
                processed BOOLEAN DEFAULT FALSE,
                api_data TEXT
            )
            ''')
            
            # Create reactions table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS reactions (
                id INTEGER PRIMARY KEY,
                bot_id INTEGER,
                post_id INTEGER,
                reaction_type TEXT,
                content TEXT,
                timestamp TEXT,
                FOREIGN KEY (bot_id) REFERENCES bots (id),
                FOREIGN KEY (post_id) REFERENCES posts (id)
            )
            ''')
            
            # Create interactions table for bot memory
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY,
                bot_id INTEGER,
                user_name TEXT,
                interaction_type TEXT,
                content TEXT,
                timestamp TEXT,
                FOREIGN KEY (bot_id) REFERENCES bots (id)
            )
            ''')
            
            # Create system_state table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_state (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Database initialized successfully")
        
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
    
    async def get_bots(self) -> List[Dict[str, Any]]:
        """
        Get all bots from the database.
        
        Returns:
            List of bot dictionaries
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute("SELECT * FROM bots") as cursor:
                    rows = await cursor.fetchall()
                    
                    bots = []
                    for row in rows:
                        bot_dict = dict(row)
                        
                        # Convert JSON strings to Python objects
                        if bot_dict.get('categories'):
                            bot_dict['categories'] = json.loads(bot_dict['categories'])
                        if bot_dict.get('following'):
                            bot_dict['following'] = json.loads(bot_dict['following'])
                        if bot_dict.get('api_data'):
                            bot_dict['api_data'] = json.loads(bot_dict['api_data'])
                        
                        bots.append(bot_dict)
                    
                    return bots
        
        except Exception as e:
            logger.error(f"Error getting bots: {str(e)}")
            return []
    
    async def get_bot(self, bot_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific bot by ID.
        
        Args:
            bot_id: Bot ID
            
        Returns:
            Bot dictionary or None if not found
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute("SELECT * FROM bots WHERE id = ?", (bot_id,)) as cursor:
                    row = await cursor.fetchone()
                    
                    if row:
                        bot_dict = dict(row)
                        
                        # Convert JSON strings to Python objects
                        if bot_dict.get('categories'):
                            bot_dict['categories'] = json.loads(bot_dict['categories'])
                        if bot_dict.get('following'):
                            bot_dict['following'] = json.loads(bot_dict['following'])
                        if bot_dict.get('api_data'):
                            bot_dict['api_data'] = json.loads(bot_dict['api_data'])
                        
                        return bot_dict
                    
                    return None
        
        except Exception as e:
            logger.error(f"Error getting bot {bot_id}: {str(e)}")
            return None
    
    async def add_bot(self, bot_data: Dict[str, Any]) -> int:
        """
        Add a new bot to the database.
        
        Args:
            bot_data: Bot data dictionary
            
        Returns:
            Bot ID
        """
        try:
            # Prepare data for insertion
            categories_json = json.dumps(bot_data.get('categories', []))
            following_json = json.dumps(bot_data.get('following', []))
            api_data_json = json.dumps(bot_data.get('api_data', {}))
            
            created_at = bot_data.get('created_at', datetime.now().isoformat())
            last_active = bot_data.get('last_active', datetime.now().isoformat())
            
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute('''
                INSERT INTO bots (
                    name, full_name, avatar, age, gender, categories, description,
                    created_at, last_active, following, followers_count, posts_count,
                    likes_given, comments_given, reposts_given,
                    like_probability, comment_probability, post_probability,
                    follow_probability, unfollow_probability, repost_probability,
                    api_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    bot_data.get('name', ''),
                    bot_data.get('full_name', ''),
                    bot_data.get('avatar', ''),
                    bot_data.get('age', 0),
                    bot_data.get('gender', ''),
                    categories_json,
                    bot_data.get('description', ''),
                    created_at,
                    last_active,
                    following_json,
                    bot_data.get('followers_count', 0),
                    bot_data.get('posts_count', 0),
                    bot_data.get('likes_given', 0),
                    bot_data.get('comments_given', 0),
                    bot_data.get('reposts_given', 0),
                    bot_data.get('like_probability', 0.5),
                    bot_data.get('comment_probability', 0.2),
                    bot_data.get('post_probability', 0.1),
                    bot_data.get('follow_probability', 0.3),
                    bot_data.get('unfollow_probability', 0.1),
                    bot_data.get('repost_probability', 0.05),
                    api_data_json
                ))
                
                await db.commit()
                return cursor.lastrowid
        
        except Exception as e:
            logger.error(f"Error adding bot: {str(e)}")
            return -1
    
    async def update_bot(self, bot_id: int, updates: Dict[str, Any]) -> bool:
        """
        Update a bot in the database.
        
        Args:
            bot_id: Bot ID
            updates: Dictionary of fields to update
            
        Returns:
            Boolean indicating success
        """
        try:
            # Prepare SET clause and parameters
            set_clauses = []
            params = []
            
            for key, value in updates.items():
                # Convert Python objects to JSON strings
                if key == 'categories' and isinstance(value, list):
                    value = json.dumps(value)
                elif key == 'following' and isinstance(value, list):
                    value = json.dumps(value)
                elif key == 'api_data' and isinstance(value, dict):
                    value = json.dumps(value)
                elif key in ('created_at', 'last_active') and isinstance(value, datetime):
                    value = value.isoformat()
                
                set_clauses.append(f"{key} = ?")
                params.append(value)
            
            # Add bot_id to parameters
            params.append(bot_id)
            
            # Execute update
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(f'''
                UPDATE bots SET {', '.join(set_clauses)} WHERE id = ?
                ''', params)
                
                await db.commit()
                return True
        
        except Exception as e:
            logger.error(f"Error updating bot {bot_id}: {str(e)}")
            return False
    
    async def delete_bot(self, bot_id: int) -> bool:
        """
        Delete a bot from the database.
        
        Args:
            bot_id: Bot ID
            
        Returns:
            Boolean indicating success
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("DELETE FROM bots WHERE id = ?", (bot_id,))
                await db.commit()
                return True
        
        except Exception as e:
            logger.error(f"Error deleting bot {bot_id}: {str(e)}")
            return False
    
    async def get_posts(self, processed: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get posts from the database.
        
        Args:
            processed: Optional filter for processed status
            
        Returns:
            List of post dictionaries
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                
                query = "SELECT * FROM posts"
                params = []
                
                if processed is not None:
                    query += " WHERE processed = ?"
                    params.append(processed)
                
                async with db.execute(query, params) as cursor:
                    rows = await cursor.fetchall()
                    
                    posts = []
                    for row in rows:
                        post_dict = dict(row)
                        
                        # Convert JSON strings to Python objects
                        if post_dict.get('api_data'):
                            post_dict['api_data'] = json.loads(post_dict['api_data'])
                        
                        posts.append(post_dict)
                    
                    return posts
        
        except Exception as e:
            logger.error(f"Error getting posts: {str(e)}")
            return []
    
    async def get_post(self, post_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific post by ID.
        
        Args:
            post_id: Post ID
            
        Returns:
            Post dictionary or None if not found
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)) as cursor:
                    row = await cursor.fetchone()
                    
                    if row:
                        post_dict = dict(row)
                        
                        # Convert JSON strings to Python objects
                        if post_dict.get('api_data'):
                            post_dict['api_data'] = json.loads(post_dict['api_data'])
                        
                        return post_dict
                    
                    return None
        
        except Exception as e:
            logger.error(f"Error getting post {post_id}: {str(e)}")
            return None
    
    async def add_post(self, post_data: Dict[str, Any]) -> int:
        """
        Add a new post to the database.
        
        Args:
            post_data: Post data dictionary
            
        Returns:
            Post ID
        """
        try:
            # Prepare data for insertion
            api_data_json = json.dumps(post_data.get('api_data', {}))
            
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute('''
                INSERT INTO posts (
                    post_id, user_name, full_name, avatar, text, on_date, processed, api_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    post_data.get('post_id', 0),
                    post_data.get('user_name', ''),
                    post_data.get('full_name', ''),
                    post_data.get('avatar', ''),
                    post_data.get('text', ''),
                    post_data.get('on_date', datetime.now().isoformat()),
                    post_data.get('processed', False),
                    api_data_json
                ))
                
                await db.commit()
                return cursor.lastrowid
        
        except Exception as e:
            logger.error(f"Error adding post: {str(e)}")
            return -1
    
    async def update_post(self, post_id: int, updates: Dict[str, Any]) -> bool:
        """
        Update a post in the database.
        
        Args:
            post_id: Post ID
            updates: Dictionary of fields to update
            
        Returns:
            Boolean indicating success
        """
        try:
            # Prepare SET clause and parameters
            set_clauses = []
            params = []
            
            for key, value in updates.items():
                # Convert Python objects to JSON strings
                if key == 'api_data' and isinstance(value, dict):
                    value = json.dumps(value)
                
                set_clauses.append(f"{key} = ?")
                params.append(value)
            
            # Add post_id to parameters
            params.append(post_id)
            
            # Execute update
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(f'''
                UPDATE posts SET {', '.join(set_clauses)} WHERE id = ?
                ''', params)
                
                await db.commit()
                return True
        
        except Exception as e:
            logger.error(f"Error updating post {post_id}: {str(e)}")
            return False
    
    async def add_reaction(self, reaction_data: Dict[str, Any]) -> int:
        """
        Add a new reaction to the database.
        
        Args:
            reaction_data: Reaction data dictionary
            
        Returns:
            Reaction ID
        """
        try:
            timestamp = reaction_data.get('timestamp', datetime.now().isoformat())
            
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute('''
                INSERT INTO reactions (
                    bot_id, post_id, reaction_type, content, timestamp
                ) VALUES (?, ?, ?, ?, ?)
                ''', (
                    reaction_data.get('bot_id', 0),
                    reaction_data.get('post_id', 0),
                    reaction_data.get('reaction_type', ''),
                    reaction_data.get('content', ''),
                    timestamp
                ))
                
                await db.commit()
                return cursor.lastrowid
        
        except Exception as e:
            logger.error(f"Error adding reaction: {str(e)}")
            return -1
    
    async def get_reactions(self, bot_id: Optional[int] = None, post_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get reactions from the database.
        
        Args:
            bot_id: Optional bot ID filter
            post_id: Optional post ID filter
            
        Returns:
            List of reaction dictionaries
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                
                query = "SELECT * FROM reactions"
                params = []
                
                if bot_id is not None and post_id is not None:
                    query += " WHERE bot_id = ? AND post_id = ?"
                    params.extend([bot_id, post_id])
                elif bot_id is not None:
                    query += " WHERE bot_id = ?"
                    params.append(bot_id)
                elif post_id is not None:
                    query += " WHERE post_id = ?"
                    params.append(post_id)
                
                async with db.execute(query, params) as cursor:
                    rows = await cursor.fetchall()
                    return [dict(row) for row in rows]
        
        except Exception as e:
            logger.error(f"Error getting reactions: {str(e)}")
            return []
    
    async def add_interaction(self, interaction_data: Dict[str, Any]) -> int:
        """
        Add a new interaction to the database.
        
        Args:
            interaction_data: Interaction data dictionary
            
        Returns:
            Interaction ID
        """
        try:
            timestamp = interaction_data.get('timestamp', datetime.now().isoformat())
            
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute('''
                INSERT INTO interactions (
                    bot_id, user_name, interaction_type, content, timestamp
                ) VALUES (?, ?, ?, ?, ?)
                ''', (
                    interaction_data.get('bot_id', 0),
                    interaction_data.get('user_name', ''),
                    interaction_data.get('interaction_type', ''),
                    interaction_data.get('content', ''),
                    timestamp
                ))
                
                await db.commit()
                return cursor.lastrowid
        
        except Exception as e:
            logger.error(f"Error adding interaction: {str(e)}")
            return -1
    
    async def get_interactions(self, bot_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get interactions for a specific bot.
        
        Args:
            bot_id: Bot ID
            limit: Maximum number of interactions to return
            
        Returns:
            List of interaction dictionaries
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    "SELECT * FROM interactions WHERE bot_id = ? ORDER BY timestamp DESC LIMIT ?",
                    (bot_id, limit)
                ) as cursor:
                    rows = await cursor.fetchall()
                    return [dict(row) for row in rows]
        
        except Exception as e:
            logger.error(f"Error getting interactions for bot {bot_id}: {str(e)}")
            return []
    
    async def get_system_state(self, key: str) -> Optional[str]:
        """
        Get a system state value.
        
        Args:
            key: State key
            
        Returns:
            State value or None if not found
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute("SELECT value FROM system_state WHERE key = ?", (key,)) as cursor:
                    row = await cursor.fetchone()
                    return row[0] if row else None
        
        except Exception as e:
            logger.error(f"Error getting system state {key}: {str(e)}")
            return None
    
    async def set_system_state(self, key: str, value: str) -> bool:
        """
        Set a system state value.
        
        Args:
            key: State key
            value: State value
            
        Returns:
            Boolean indicating success
        """
        try:
            updated_at = datetime.now().isoformat()
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('''
                INSERT OR REPLACE INTO system_state (key, value, updated_at)
                VALUES (?, ?, ?)
                ''', (key, value, updated_at))
                
                await db.commit()
                return True
        
        except Exception as e:
            logger.error(f"Error setting system state {key}: {str(e)}")
            return False
    
    async def count_bots(self) -> int:
        """
        Count the total number of bots.
        
        Returns:
            Total number of bots
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute("SELECT COUNT(*) FROM bots") as cursor:
                    row = await cursor.fetchone()
                    return row[0] if row else 0
        
        except Exception as e:
            logger.error(f"Error counting bots: {str(e)}")
            return 0
