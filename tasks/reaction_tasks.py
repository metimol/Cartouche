"""
Tasks related to bot reactions to posts.
Handles processing of likes, comments, and reposts.
"""
import logging
import random
from typing import Dict, List, Any, Optional
from datetime import datetime

from celery import shared_task
from models import Post, Bot
from bot_manager.bot_manager import BotManager
from reaction_engine.reaction_engine import ReactionEngine
from content_generator.llm_service import LLMService
from utils.http_client import HttpClient
from config import settings

logger = logging.getLogger(__name__)

@shared_task
def process_post_reactions(post_id: int, post_content: str, user_id: str) -> Dict[str, Any]:
    """
    Process bot reactions to a new post.
    
    Args:
        post_id: Post ID
        post_content: Post content
        user_id: User ID who created the post
        
    Returns:
        Dictionary with status and reaction results
    """
    try:
        bot_manager = BotManager()
        reaction_engine = ReactionEngine()
        
        # Get all bots
        bots = bot_manager.get_all_bots()
        
        # Create post object
        post = Post(
            id=post_id,
            content=post_content,
            user_id=user_id,
            timestamp=datetime.now()
        )
        
        # Process reactions
        likes = []
        comments = []
        reposts = []
        
        for bot in bots:
            # Check if bot should like the post
            if should_like_post(bot, post):
                # Add like
                like_result = reaction_engine.add_like(bot, post)
                likes.append({
                    "bot_id": bot.get("id"),
                    "bot_name": bot.get("name"),
                    "post_id": post.id,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Check if bot should comment on the post
            if should_comment_on_post(bot, post):
                # Add comment
                comment_text = reaction_engine.generate_comment(bot, post)
                comment_result = reaction_engine.add_comment(bot, post, comment_text)
                comments.append({
                    "bot_id": bot.get("id"),
                    "bot_name": bot.get("name"),
                    "post_id": post.id,
                    "comment": comment_text,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Check if bot should repost the post
            if should_repost_post(bot, post):
                # Add repost
                repost_result = reaction_engine.add_repost(bot, post)
                reposts.append({
                    "bot_id": bot.get("id"),
                    "bot_name": bot.get("name"),
                    "post_id": post.id,
                    "timestamp": datetime.now().isoformat()
                })
        
        return {
            "status": "success",
            "post_id": post.id,
            "likes": likes,
            "comments": comments,
            "reposts": reposts
        }
    
    except Exception as e:
        logger.error(f"Error processing post reactions: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

def should_like_post(bot: Dict[str, Any], post: Post) -> bool:
    """
    Determine if a bot should like a post based on probability.
    
    Args:
        bot: Bot data
        post: Post data
        
    Returns:
        Boolean indicating whether the bot should like the post
    """
    # Get bot's like probability
    like_probability = bot.get("like_probability", 0.5)
    
    # Adjust probability based on post content (could be more sophisticated)
    # For now, just use the base probability
    
    # Make probabilistic decision
    return random.random() < like_probability

def should_comment_on_post(bot: Dict[str, Any], post: Post) -> bool:
    """
    Determine if a bot should comment on a post based on probability.
    
    Args:
        bot: Bot data
        post: Post data
        
    Returns:
        Boolean indicating whether the bot should comment on the post
    """
    # Get bot's comment probability
    comment_probability = bot.get("comment_probability", 0.3)
    
    # Adjust probability based on post content (could be more sophisticated)
    # For now, just use the base probability
    
    # Make probabilistic decision
    return random.random() < comment_probability

def should_repost_post(bot: Dict[str, Any], post: Post) -> bool:
    """
    Determine if a bot should repost a post based on probability.
    
    Args:
        bot: Bot data
        post: Post data
        
    Returns:
        Boolean indicating whether the bot should repost the post
    """
    # Get bot's repost probability
    repost_probability = bot.get("repost_probability", 0.2)
    
    # Adjust probability based on post content (could be more sophisticated)
    # For now, just use the base probability
    
    # Make probabilistic decision
    return random.random() < repost_probability
