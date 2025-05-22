"""
Tasks related to post generation and management.
"""
import logging
import random
from typing import Dict, List, Any, Optional
from datetime import datetime

from celery import shared_task
from models import Post
from bot_manager.bot_manager import BotManager
from content_generator.llm_service import LLMService
from utils.language_service import LanguageService
from config import settings

logger = logging.getLogger(__name__)

@shared_task
def generate_bot_posts(limit: int = 20, user_id: Optional[str] = None, language: str = "en") -> Dict[str, Any]:
    """
    Generate posts from bots.
    
    Args:
        limit: Maximum number of posts to generate
        user_id: Optional user ID for personalization
        language: Language for post content
        
    Returns:
        Dictionary with status and generated posts
    """
    try:
        bot_manager = BotManager()
        llm_service = LLMService()
        language_service = LanguageService()
        
        # Get all bots
        bots = bot_manager.get_all_bots()
        
        # Filter bots that are likely to post
        posting_bots = []
        for bot in bots:
            if random.random() < bot.get("post_probability", 0.1):
                posting_bots.append(bot)
        
        # Limit the number of posting bots
        posting_bots = posting_bots[:min(limit, len(posting_bots))]
        
        # Generate posts
        posts = []
        for bot in posting_bots:
            # Get trending topics or use default topics
            topics = _get_trending_topics()
            
            # Generate post content
            content = llm_service.generate_post(
                bot=bot,
                topics=topics,
                language=language
            )
            
            # Create post
            post = Post(
                id=_generate_post_id(),
                bot_id=bot.get("id"),
                content=content,
                timestamp=datetime.now()
            )
            
            # Send post to main app
            _send_post_to_main_app(post, bot)
            
            # Update bot stats
            bot_manager.update_bot(bot.get("id"), {
                "posts_count": bot.get("posts_count", 0) + 1,
                "last_active": datetime.now()
            })
            
            # Add to result
            posts.append({
                "id": post.id,
                "bot_id": bot.get("id"),
                "bot_name": bot.get("name"),
                "bot_avatar": bot.get("avatar"),
                "content": post.content,
                "timestamp": post.timestamp.isoformat()
            })
        
        return {
            "status": "success",
            "posts": posts
        }
    
    except Exception as e:
        logger.error(f"Error generating bot posts: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

def _get_trending_topics() -> List[str]:
    """
    Get trending topics.
    
    Returns:
        List of trending topics
    """
    # In a real implementation, this would fetch trending topics from the main app
    # For now, we'll use a predefined list
    default_topics = [
        "technology", "science", "art", "music", "movies",
        "books", "gaming", "sports", "food", "travel",
        "fashion", "health", "politics", "business", "education"
    ]
    
    # Select a random subset of topics
    num_topics = random.randint(1, 3)
    return random.sample(default_topics, num_topics)

def _generate_post_id() -> int:
    """
    Generate a unique post ID.
    
    Returns:
        Unique post ID
    """
    # In a real implementation, this would get the next available ID from the main app
    # For now, we'll use a random large number
    return random.randint(10000, 1000000)

def _send_post_to_main_app(post: Post, bot: Dict[str, Any]) -> bool:
    """
    Send a post to the main app.
    
    Args:
        post: Post to send
        bot: Bot that created the post
        
    Returns:
        Boolean indicating success
    """
    try:
        import requests
        
        # Prepare post data
        post_data = {
            "bot_id": bot.get("id"),
            "content": post.content,
            "timestamp": post.timestamp.isoformat()
        }
        
        # Send post to main app
        response = requests.post(
            f"{settings.MAIN_APP_URL}/api/posts",
            json=post_data,
            headers={
                "Authorization": f"Bearer {settings.MAIN_APP_API_KEY}",
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code == 200:
            logger.info(f"Post from bot {bot.get('id')} sent to main app")
            return True
        else:
            logger.warning(f"Failed to send post to main app: {response.status_code} {response.text}")
            return False
    
    except Exception as e:
        logger.error(f"Error sending post to main app: {str(e)}")
        return False
