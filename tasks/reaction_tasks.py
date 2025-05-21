"""
Tasks related to bot reactions for the Cartouche Bot Service.
"""
import random
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from celery_app import app
from models import Post, Reaction
from bot_manager.bot_manager import BotManager
from content_generator.llm_service import LLMService
from memory_service.memory_service import MemoryService
from utils.http_client import HttpClient
from config import settings

logger = logging.getLogger(__name__)

@app.task(name="tasks.reaction_tasks.process_post_reactions")
def process_post_reactions(post_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process reactions to a new post.
    
    Args:
        post_data: Post data from the main system
        
    Returns:
        Dictionary with processing results
    """
    logger.info(f"Processing reactions for post {post_data.get('id')}")
    
    try:
        # Create post object
        post = Post(**post_data)
        
        # Get bot manager instance
        bot_manager = BotManager()
        
        # Get memory service instance
        memory_service = MemoryService()
        
        # Get LLM service instance (only for comment generation)
        llm_service = LLMService()
        
        # Get all bots
        bots = bot_manager.get_all_bots()
        
        # Process reactions
        reactions = []
        
        for bot in bots:
            # Skip if the bot is the author of the post
            if post.bot_id and post.bot_id == bot.id:
                continue
            
            # Get interaction history
            history = memory_service.get_interaction_history(
                bot_id=bot.id,
                target_id=post.user_id or post.bot_id
            )
            
            # Determine actions based on probability
            should_like = _should_like_post(bot, post, history)
            should_comment = _should_comment_on_post(bot, post, history)
            should_repost = _should_repost_post(bot, post, history)
            
            # Process like
            if should_like:
                reaction = Reaction(
                    bot_id=bot.id,
                    post_id=post.id,
                    reaction_type="like",
                    timestamp=datetime.now()
                )
                reactions.append(reaction)
                
                # Update bot stats
                bot.likes_given += 1
                bot_manager.update_bot(bot.id, {"likes_given": bot.likes_given})
                
                # Add to memory
                memory_service.add_interaction(
                    bot_id=bot.id,
                    target_id=post.user_id or post.bot_id,
                    interaction_type="like",
                    content=post.content[:100]  # Store a snippet of the post
                )
            
            # Process comment
            if should_comment:
                # Generate comment using LLM
                comment_text = llm_service.generate_comment(
                    bot_profile=bot.dict(),
                    post_content=post.content,
                    history=history
                )
                
                reaction = Reaction(
                    bot_id=bot.id,
                    post_id=post.id,
                    reaction_type="comment",
                    content=comment_text,
                    timestamp=datetime.now()
                )
                reactions.append(reaction)
                
                # Update bot stats
                bot.comments_given += 1
                bot_manager.update_bot(bot.id, {"comments_given": bot.comments_given})
                
                # Add to memory
                memory_service.add_interaction(
                    bot_id=bot.id,
                    target_id=post.user_id or post.bot_id,
                    interaction_type="comment",
                    content=comment_text
                )
            
            # Process repost
            if should_repost:
                reaction = Reaction(
                    bot_id=bot.id,
                    post_id=post.id,
                    reaction_type="repost",
                    timestamp=datetime.now()
                )
                reactions.append(reaction)
                
                # Update bot stats
                bot.reposts_given += 1
                bot_manager.update_bot(bot.id, {"reposts_given": bot.reposts_given})
                
                # Add to memory
                memory_service.add_interaction(
                    bot_id=bot.id,
                    target_id=post.user_id or post.bot_id,
                    interaction_type="repost",
                    content=post.content[:100]  # Store a snippet of the post
                )
        
        # Send reactions to main app
        if reactions:
            _send_reactions_to_main_app(post.id, reactions)
        
        return {
            "status": "success",
            "post_id": post.id,
            "reactions_count": len(reactions)
        }
    
    except Exception as e:
        logger.error(f"Error processing post reactions: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

def _should_like_post(bot: Dict[str, Any], post: Post, history: str) -> bool:
    """
    Determine if a bot should like a post based on probability and characteristics.
    
    Args:
        bot: Bot data
        post: Post data
        history: Interaction history
        
    Returns:
        Boolean indicating whether the bot should like the post
    """
    # Base probability from bot's characteristics
    base_probability = bot.get("like_probability", 0.5)
    
    # Adjust based on bot category
    category_adjustment = 0
    categories = bot.get("category", [])
    
    if "fan" in categories:
        category_adjustment += 0.3
    if "hater" in categories:
        category_adjustment -= 0.3
    if "neutral" in categories:
        category_adjustment += 0.0  # No change
    if "silent" in categories:
        category_adjustment -= 0.1
    
    # Adjust based on previous interactions
    history_adjustment = 0
    if "LIKE" in history:
        history_adjustment += 0.1  # More likely to like if liked before
    
    # Adjust based on post content length
    content_adjustment = 0
    if len(post.content) > 200:
        content_adjustment += 0.05  # Slightly more likely to like longer posts
    
    # Calculate final probability
    final_probability = base_probability + category_adjustment + history_adjustment + content_adjustment
    
    # Ensure probability is within valid range [0, 1]
    final_probability = max(0.0, min(1.0, final_probability))
    
    # Make decision based on probability
    return random.random() < final_probability

def _should_comment_on_post(bot: Dict[str, Any], post: Post, history: str) -> bool:
    """
    Determine if a bot should comment on a post based on probability and characteristics.
    
    Args:
        bot: Bot data
        post: Post data
        history: Interaction history
        
    Returns:
        Boolean indicating whether the bot should comment on the post
    """
    # Base probability from bot's characteristics
    base_probability = bot.get("comment_probability", 0.2)
    
    # Adjust based on bot category
    category_adjustment = 0
    categories = bot.get("category", [])
    
    if "fan" in categories:
        category_adjustment += 0.2
    if "hater" in categories:
        category_adjustment += 0.2  # Haters also like to comment
    if "neutral" in categories:
        category_adjustment += 0.0  # No change
    if "silent" in categories:
        category_adjustment -= 0.15  # Silent bots comment less
    if "humorous" in categories:
        category_adjustment += 0.3  # Humorous bots comment more
    if "provocative" in categories:
        category_adjustment += 0.3  # Provocative bots comment more
    
    # Adjust based on previous interactions
    history_adjustment = 0
    if "COMMENT" in history:
        history_adjustment += 0.1  # More likely to comment if commented before
    
    # Adjust based on post content length
    content_adjustment = 0
    if len(post.content) > 100:
        content_adjustment += 0.1  # More likely to comment on substantial posts
    
    # Calculate final probability
    final_probability = base_probability + category_adjustment + history_adjustment + content_adjustment
    
    # Ensure probability is within valid range [0, 1]
    final_probability = max(0.0, min(1.0, final_probability))
    
    # Make decision based on probability
    return random.random() < final_probability

def _should_repost_post(bot: Dict[str, Any], post: Post, history: str) -> bool:
    """
    Determine if a bot should repost a post based on probability and characteristics.
    
    Args:
        bot: Bot data
        post: Post data
        history: Interaction history
        
    Returns:
        Boolean indicating whether the bot should repost the post
    """
    # Base probability (reposting is less common than liking)
    base_probability = bot.get("repost_probability", 0.1)
    
    # Adjust based on bot category
    category_adjustment = 0
    categories = bot.get("category", [])
    
    if "fan" in categories:
        category_adjustment += 0.15
    if "hater" in categories:
        category_adjustment -= 0.05
    if "neutral" in categories:
        category_adjustment += 0.0  # No change
    if "silent" in categories:
        category_adjustment -= 0.08  # Silent bots repost less
    
    # Adjust based on previous interactions
    history_adjustment = 0
    if "REPOST" in history:
        history_adjustment += 0.05  # More likely to repost if reposted before
    if "LIKE" in history:
        history_adjustment += 0.03  # More likely to repost if liked before
    
    # Calculate final probability
    final_probability = base_probability + category_adjustment + history_adjustment
    
    # Ensure probability is within valid range [0, 1]
    final_probability = max(0.0, min(1.0, final_probability))
    
    # Make decision based on probability
    return random.random() < final_probability

def _send_reactions_to_main_app(post_id: int, reactions: List[Reaction]) -> None:
    """
    Send reactions to the main app.
    
    Args:
        post_id: ID of the post
        reactions: List of reactions
    """
    try:
        # Prepare data
        data = {
            "post_id": post_id,
            "reactions": [reaction.dict() for reaction in reactions]
        }
        
        # Send to main app
        http_client = HttpClient()
        response = http_client.post(
            f"{settings.MAIN_APP_URL}/api/reactions",
            json=data,
            headers={"Authorization": f"Bearer {settings.MAIN_APP_API_KEY}"}
        )
        
        if response.status_code != 200:
            logger.error(f"Error sending reactions to main app: {response.text}")
    
    except Exception as e:
        logger.error(f"Error connecting to main app: {str(e)}")
