"""
Tasks related to bot management for the Cartouche Bot Service.
"""
import random
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import aiohttp

from celery_app import app
from models import Bot, BotCreationRequest
from content_generator.llm_service import LLMService
from memory_service.memory_service import MemoryService
from bot_manager.bot_manager import BotManager
from config import settings

logger = logging.getLogger(__name__)

@app.task(name="tasks.bot_tasks.grow_bots")
def grow_bots() -> Dict[str, Any]:
    """
    Grow the number of bots by creating new ones.
    
    Returns:
        Dictionary with growth results
    """
    logger.info("Starting bot growth task")
    
    try:
        # Get bot manager instance
        bot_manager = BotManager()
        
        # Get current bot count
        current_count = len(bot_manager.get_all_bots())
        
        # Check if we've reached the maximum number of bots
        if current_count >= settings.MAX_BOTS_COUNT:
            logger.info(f"Maximum bot count reached ({current_count}/{settings.MAX_BOTS_COUNT}). No new bots created.")
            return {
                "status": "success",
                "message": "Maximum bot count reached",
                "current_count": current_count,
                "new_bots": 0
            }
        
        # Determine number of new bots to create (random, but limited)
        max_new_bots = min(
            settings.MAX_NEW_BOTS_PER_DAY,
            settings.MAX_BOTS_COUNT - current_count
        )
        
        # Random number between 1 and max_new_bots
        new_bots_count = random.randint(1, max_new_bots)
        
        logger.info(f"Creating {new_bots_count} new bots")
        
        # Create new bots
        new_bots = []
        for _ in range(new_bots_count):
            bot = _create_new_bot(bot_manager)
            if bot:
                new_bots.append(bot)
        
        return {
            "status": "success",
            "message": f"Created {len(new_bots)} new bots",
            "current_count": current_count + len(new_bots),
            "new_bots": len(new_bots)
        }
    
    except Exception as e:
        logger.error(f"Error growing bots: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

@app.task(name="tasks.bot_tasks.create_bot")
def create_bot(request_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Create a new bot.
    
    Args:
        request_data: Optional bot creation request data
        
    Returns:
        Dictionary with created bot data
    """
    logger.info("Creating new bot")
    
    try:
        # Get bot manager instance
        bot_manager = BotManager()
        
        # Create bot creation request if not provided
        if request_data:
            request = BotCreationRequest(**request_data)
        else:
            request = BotCreationRequest()
        
        # Create bot
        bot = _create_new_bot(bot_manager, request)
        
        if bot:
            return {
                "status": "success",
                "bot": bot.dict()
            }
        else:
            return {
                "status": "error",
                "error": "Failed to create bot"
            }
    
    except Exception as e:
        logger.error(f"Error creating bot: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

def _create_new_bot(bot_manager: BotManager, request: Optional[BotCreationRequest] = None) -> Optional[Bot]:
    """
    Create a new bot with random characteristics.
    
    Args:
        bot_manager: Bot manager instance
        request: Optional bot creation request
        
    Returns:
        Created bot or None if creation failed
    """
    try:
        # Get LLM service instance
        llm_service = LLMService()
        
        # Generate bot ID
        bot_id = bot_manager.get_next_bot_id()
        
        # Generate bot characteristics if not provided
        name = request.name if request and request.name else _generate_bot_name()
        full_name = request.full_name if request and request.full_name else _generate_bot_full_name()
        age = request.age if request and request.age else random.randint(18, 65)
        gender = request.gender if request and request.gender else random.choice(["Male", "Female", "Other"])
        
        # Generate bot category
        bot_categories = [
            "fan", "hater", "neutral", "humorous", 
            "provocative", "silent", "random", "roleplay"
        ]
        
        categories = request.category if request and request.category else random.sample(
            bot_categories, 
            k=random.randint(1, min(3, len(bot_categories)))
        )
        
        # Generate avatar URL using DiceBear
        avatar = _generate_avatar_url(name)
        
        # Generate bot description using LLM
        description = request.description if request and request.description else llm_service.generate_bot_description(
            name=name,
            age=age,
            gender=gender,
            categories=categories
        )
        
        # Set behavior probabilities based on category
        like_probability, comment_probability, post_probability, follow_probability, unfollow_probability, repost_probability = \
            _calculate_behavior_probabilities(categories)
        
        # Create bot
        bot = Bot(
            id=bot_id,
            name=name,
            full_name=full_name,
            avatar=avatar,
            age=age,
            gender=gender,
            category=categories,
            description=description,
            created_at=datetime.now(),
            last_active=datetime.now(),
            like_probability=like_probability,
            comment_probability=comment_probability,
            post_probability=post_probability,
            follow_probability=follow_probability,
            unfollow_probability=unfollow_probability,
            repost_probability=repost_probability,
            following=[],
            followers_count=0,
            posts_count=0,
            likes_given=0,
            comments_given=0,
            reposts_given=0
        )
        
        # Save bot
        bot_manager.add_bot(bot)
        
        logger.info(f"Created new bot: {bot.name} (ID: {bot.id})")
        
        return bot
    
    except Exception as e:
        logger.error(f"Error creating new bot: {str(e)}")
        return None

def _generate_bot_name() -> str:
    """
    Generate a random bot name.
    
    Returns:
        Generated name
    """
    # Simple name generation logic
    prefixes = ["Cool", "Super", "Mega", "Ultra", "Hyper", "Cyber", "Digital", "Tech", "Smart", "Clever"]
    suffixes = ["User", "Person", "Bot", "Friend", "Buddy", "Pal", "Mate", "Fan", "Guru", "Master"]
    numbers = [str(random.randint(1, 999)) for _ in range(3)]
    
    name_parts = [
        random.choice(prefixes),
        random.choice(suffixes),
        random.choice(numbers)
    ]
    
    # Randomly decide if we use prefix+suffix or just one of them with a number
    if random.random() < 0.5:
        return name_parts[0] + name_parts[1] + name_parts[2]
    else:
        return random.choice(name_parts[:2]) + name_parts[2]

def _generate_bot_full_name() -> str:
    """
    Generate a random full name for a bot.
    
    Returns:
        Generated full name
    """
    # Simple full name generation
    first_names = ["Alex", "Sam", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Quinn", "Avery", "Dakota"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson"]
    
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def _generate_avatar_url(name: str) -> str:
    """
    Generate an avatar URL using DiceBear API.
    
    Args:
        name: Bot name to use as seed
        
    Returns:
        Avatar URL
    """
    style = settings.DICEBEAR_STYLE
    api_url = settings.DICEBEAR_API_URL
    
    # Generate avatar URL
    return f"{api_url}/{style}/svg?seed={name}"

def _calculate_behavior_probabilities(categories: List[str]) -> tuple:
    """
    Calculate behavior probabilities based on bot categories.
    
    Args:
        categories: List of bot categories
        
    Returns:
        Tuple of (like_probability, comment_probability, post_probability, 
                 follow_probability, unfollow_probability, repost_probability)
    """
    # Default probabilities
    like_prob = 0.5
    comment_prob = 0.2
    post_prob = 0.1
    follow_prob = 0.3
    unfollow_prob = 0.1
    repost_prob = 0.05
    
    # Adjust based on categories
    for category in categories:
        if category == "fan":
            like_prob += 0.3
            comment_prob += 0.2
            follow_prob += 0.2
            repost_prob += 0.1
        elif category == "hater":
            like_prob -= 0.3
            comment_prob += 0.2
            unfollow_prob += 0.2
            repost_prob -= 0.02
        elif category == "neutral":
            # Neutral stays close to default
            pass
        elif category == "humorous":
            comment_prob += 0.3
            post_prob += 0.2
            repost_prob += 0.05
        elif category == "provocative":
            comment_prob += 0.3
            like_prob -= 0.1
            repost_prob += 0.1
        elif category == "silent":
            comment_prob -= 0.15
            post_prob -= 0.05
            like_prob += 0.1
            repost_prob -= 0.03
        elif category == "random":
            # Randomize a bit
            like_prob += random.uniform(-0.2, 0.2)
            comment_prob += random.uniform(-0.1, 0.1)
            post_prob += random.uniform(-0.05, 0.05)
            follow_prob += random.uniform(-0.1, 0.1)
            unfollow_prob += random.uniform(-0.05, 0.05)
            repost_prob += random.uniform(-0.03, 0.03)
        elif category == "roleplay":
            post_prob += 0.2
            comment_prob += 0.1
            repost_prob += 0.05
    
    # Ensure probabilities are within valid range [0, 1]
    like_prob = max(0.0, min(1.0, like_prob))
    comment_prob = max(0.0, min(1.0, comment_prob))
    post_prob = max(0.0, min(1.0, post_prob))
    follow_prob = max(0.0, min(1.0, follow_prob))
    unfollow_prob = max(0.0, min(1.0, unfollow_prob))
    repost_prob = max(0.0, min(1.0, repost_prob))
    
    return (like_prob, comment_prob, post_prob, follow_prob, unfollow_prob, repost_prob)
