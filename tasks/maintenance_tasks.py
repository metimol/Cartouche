"""
Maintenance tasks for the Cartouche Bot Service.
Handles periodic maintenance operations like cache cleanup, bot growth, etc.
"""
import logging
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from celery import shared_task
from bot_manager.bot_manager import BotManager
from content_generator.llm_service import LLMService
from utils.cache_service import CacheService
from config import settings

logger = logging.getLogger(__name__)

@shared_task
def cleanup_cache() -> Dict[str, Any]:
    """
    Clean up expired cache entries.
    
    Returns:
        Dictionary with status and cleanup results
    """
    try:
        cache_service = CacheService()
        
        # Clear expired cache entries (older than 1 day)
        cleared_count = cache_service.clear_expired(86400)  # 24 hours in seconds
        
        return {
            "status": "success",
            "cleared_count": cleared_count
        }
    
    except Exception as e:
        logger.error(f"Error cleaning up cache: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

@shared_task
def grow_bot_population() -> Dict[str, Any]:
    """
    Grow the bot population by creating new bots.
    
    Returns:
        Dictionary with status and new bots
    """
    try:
        bot_manager = BotManager()
        llm_service = LLMService()
        
        # Get current bot count
        bots = bot_manager.get_all_bots()
        current_count = len(bots)
        
        # Determine how many new bots to create (random, but max 30 per day)
        max_new_bots = settings.MAX_DAILY_NEW_BOTS
        new_bot_count = random.randint(1, max_new_bots)
        
        logger.info(f"Growing bot population by {new_bot_count} new bots")
        
        # Create new bots
        new_bots = []
        for _ in range(new_bot_count):
            # Generate bot characteristics
            gender = random.choice(["male", "female", "non-binary"])
            age = random.randint(18, 65)
            
            # Personality types with probabilities
            personality_types = {
                "fan": 0.3,       # Fans are more common
                "hater": 0.1,     # Haters are less common
                "neutral": 0.4,   # Neutral users are most common
                "troll": 0.05,    # Trolls are rare
                "intellectual": 0.15  # Intellectuals are somewhat common
            }
            
            personality = random.choices(
                list(personality_types.keys()),
                weights=list(personality_types.values()),
                k=1
            )[0]
            
            # Generate probabilities for different actions
            like_probability = _generate_probability_for_personality(personality, "like")
            comment_probability = _generate_probability_for_personality(personality, "comment")
            repost_probability = _generate_probability_for_personality(personality, "repost")
            follow_probability = _generate_probability_for_personality(personality, "follow")
            unfollow_probability = _generate_probability_for_personality(personality, "unfollow")
            post_probability = _generate_probability_for_personality(personality, "post")
            
            # Generate name and description using LLM
            bot_profile = llm_service.generate_bot_profile(gender, age, personality)
            
            # Generate avatar URL using DiceBear
            avatar_url = _generate_avatar(gender)
            
            # Create bot
            bot_data = {
                "name": bot_profile.get("name"),
                "description": bot_profile.get("description"),
                "gender": gender,
                "age": age,
                "personality": personality,
                "avatar": avatar_url,
                "like_probability": like_probability,
                "comment_probability": comment_probability,
                "repost_probability": repost_probability,
                "follow_probability": follow_probability,
                "unfollow_probability": unfollow_probability,
                "post_probability": post_probability,
                "created_at": datetime.now(),
                "followers_count": 0,
                "following": [],
                "posts_count": 0
            }
            
            # Save bot to database
            bot_id = bot_manager.create_bot(bot_data)
            
            # Add to result
            bot_data["id"] = bot_id
            new_bots.append(bot_data)
            
            # Send to main app
            _send_bot_to_main_app(bot_data)
        
        return {
            "status": "success",
            "current_count": current_count,
            "new_count": new_bot_count,
            "new_bots": new_bots
        }
    
    except Exception as e:
        logger.error(f"Error growing bot population: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

def _generate_probability_for_personality(personality: str, action: str) -> float:
    """
    Generate probability for a specific action based on personality.
    
    Args:
        personality: Bot personality
        action: Action type
        
    Returns:
        Probability value between 0 and 1
    """
    # Base probabilities for different personalities and actions
    base_probabilities = {
        "fan": {
            "like": 0.8,
            "comment": 0.6,
            "repost": 0.4,
            "follow": 0.7,
            "unfollow": 0.05,
            "post": 0.3
        },
        "hater": {
            "like": 0.1,
            "comment": 0.7,
            "repost": 0.2,
            "follow": 0.3,
            "unfollow": 0.4,
            "post": 0.4
        },
        "neutral": {
            "like": 0.5,
            "comment": 0.3,
            "repost": 0.2,
            "follow": 0.4,
            "unfollow": 0.2,
            "post": 0.2
        },
        "troll": {
            "like": 0.3,
            "comment": 0.8,
            "repost": 0.1,
            "follow": 0.2,
            "unfollow": 0.6,
            "post": 0.5
        },
        "intellectual": {
            "like": 0.6,
            "comment": 0.7,
            "repost": 0.3,
            "follow": 0.5,
            "unfollow": 0.1,
            "post": 0.6
        }
    }
    
    # Get base probability
    base_prob = base_probabilities.get(personality, {}).get(action, 0.3)
    
    # Add some randomness (±20%)
    variation = base_prob * 0.2
    final_prob = base_prob + random.uniform(-variation, variation)
    
    # Ensure probability is between 0 and 1
    return max(0.01, min(0.99, final_prob))

def _generate_avatar(gender: str) -> str:
    """
    Generate avatar URL using DiceBear API.
    
    Args:
        gender: Bot gender
        
    Returns:
        Avatar URL
    """
    # Choose appropriate avatar style based on gender
    if gender == "male":
        style = random.choice(["avataaars", "bottts", "pixel-art-neutral", "adventurer-neutral"])
    elif gender == "female":
        style = random.choice(["avataaars", "bottts", "pixel-art-neutral", "adventurer-neutral"])
    else:
        style = random.choice(["avataaars", "bottts", "pixel-art-neutral", "adventurer-neutral"])
    
    # Generate random seed
    seed = f"cartouche-{random.randint(1000, 9999)}"
    
    # Generate avatar URL
    return f"https://api.dicebear.com/7.x/{style}/svg?seed={seed}"

def _send_bot_to_main_app(bot_data: Dict[str, Any]) -> bool:
    """
    Send a bot to the main app.
    
    Args:
        bot_data: Bot data
        
    Returns:
        Boolean indicating success
    """
    try:
        import requests
        
        # Prepare bot data
        send_data = {
            "id": bot_data.get("id"),
            "name": bot_data.get("name"),
            "description": bot_data.get("description"),
            "gender": bot_data.get("gender"),
            "age": bot_data.get("age"),
            "personality": bot_data.get("personality"),
            "avatar": bot_data.get("avatar"),
            "created_at": bot_data.get("created_at").isoformat() if isinstance(bot_data.get("created_at"), datetime) else bot_data.get("created_at")
        }
        
        # Send bot to main app
        response = requests.post(
            f"{settings.MAIN_APP_URL}/api/bots",
            json=send_data,
            headers={
                "Authorization": f"Bearer {settings.MAIN_APP_API_KEY}",
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code == 200:
            logger.info(f"Bot {bot_data.get('id')} sent to main app")
            return True
        else:
            logger.warning(f"Failed to send bot to main app: {response.status_code} {response.text}")
            return False
    
    except Exception as e:
        logger.error(f"Error sending bot to main app: {str(e)}")
        return False
