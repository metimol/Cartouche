"""
Monitor module for the Cartouche Autonomous Service.
Handles monitoring of posts and other content in the social network.
"""
import logging
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

from database import Database
from api_client import APIClient
from reaction_engine import ReactionEngine
from config import MONITORING_INTERVAL

logger = logging.getLogger(__name__)

class Monitor:
    """Monitor for social network content."""
    
    def __init__(
        self, 
        database: Optional[Database] = None, 
        api_client: Optional[APIClient] = None,
        reaction_engine: Optional[ReactionEngine] = None
    ):
        """
        Initialize the monitor.
        
        Args:
            database: Database instance
            api_client: API client instance
            reaction_engine: Reaction engine instance
        """
        self.database = database or Database()
        self.api_client = api_client or APIClient()
        self.reaction_engine = reaction_engine or ReactionEngine()
        self.running = False
        self.last_post_id = 0
    
    async def start(self):
        """Start the monitoring process."""
        if self.running:
            logger.warning("Monitor is already running")
            return
        
        self.running = True
        logger.info("Starting monitor")
        
        # Get last processed post ID from system state
        last_id_str = await self.database.get_system_state("last_processed_post_id")
        if last_id_str:
            self.last_post_id = int(last_id_str)
        
        # Start monitoring loop
        while self.running:
            try:
                await self._check_for_new_posts()
                await asyncio.sleep(MONITORING_INTERVAL)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                await asyncio.sleep(MONITORING_INTERVAL * 2)  # Wait longer on error
    
    async def stop(self):
        """Stop the monitoring process."""
        if not self.running:
            logger.warning("Monitor is not running")
            return
        
        self.running = False
        logger.info("Stopping monitor")
    
    async def _check_for_new_posts(self):
        """Check for new posts in the social network."""
        try:
            # Get posts from API
            async with self.api_client as client:
                posts = await client.get_posts()
            
            # Sort posts by ID
            posts.sort(key=lambda p: p.get('id', 0))
            
            # Process new posts
            new_posts = 0
            for post in posts:
                post_id = post.get('id', 0)
                
                # Skip posts we've already processed
                if post_id <= self.last_post_id:
                    continue
                
                # Process post
                logger.info(f"Processing new post: {post_id}")
                result = await self.reaction_engine.process_post(post)
                
                # Update last processed post ID
                if post_id > self.last_post_id:
                    self.last_post_id = post_id
                    await self.database.set_system_state("last_processed_post_id", str(self.last_post_id))
                
                new_posts += 1
                
                # Log result
                logger.info(f"Post {post_id} processed: {result}")
            
            if new_posts > 0:
                logger.info(f"Processed {new_posts} new posts")
            else:
                logger.debug("No new posts found")
        
        except Exception as e:
            logger.error(f"Error checking for new posts: {str(e)}")
