"""
Tasks related to subscription management.
"""
import logging
import random
from typing import Dict, List, Any, Optional
from datetime import datetime

from celery import shared_task
from bot_manager.bot_manager import BotManager
from memory_service.memory_service import MemoryService
from config import settings

logger = logging.getLogger(__name__)

@shared_task
def process_subscriptions() -> Dict[str, Any]:
    """
    Process bot subscriptions (follows and unfollows).
    
    Returns:
        Dictionary with status and subscription results
    """
    try:
        bot_manager = BotManager()
        memory_service = MemoryService()
        
        # Get all bots
        bots = bot_manager.get_all_bots()
        
        # Process follows and unfollows
        follows = []
        unfollows = []
        
        for bot in bots:
            # Process follows
            if random.random() < bot.get("follow_probability", 0.3):
                # Decide whether to follow a user or another bot
                if random.random() < 0.7:  # 70% chance to follow a user
                    # In a real implementation, this would get a list of users from the main app
                    # For now, we'll use a random user ID
                    user_id = f"user_{random.randint(1, 100)}"
                    
                    # Check if already following
                    following = bot.get("following", [])
                    if user_id not in following:
                        # Add to following list
                        following.append(user_id)
                        bot_manager.update_bot(bot.get("id"), {"following": following})
                        
                        # Add to memory
                        memory_service.add_interaction(
                            bot_id=bot.get("id"),
                            target_id=user_id,
                            interaction_type="follow"
                        )
                        
                        # Send to main app
                        _send_subscription_to_main_app(
                            bot_id=bot.get("id"),
                            target_id=user_id,
                            action="follow"
                        )
                        
                        follows.append({
                            "bot_id": bot.get("id"),
                            "target_id": user_id,
                            "target_type": "user"
                        })
                
                else:  # 30% chance to follow another bot
                    # Select a random bot to follow
                    other_bots = [b for b in bots if b.get("id") != bot.get("id")]
                    if other_bots:
                        other_bot = random.choice(other_bots)
                        other_bot_id = other_bot.get("id")
                        
                        # Check if already following
                        following = bot.get("following", [])
                        if other_bot_id not in following:
                            # Add to following list
                            following.append(other_bot_id)
                            bot_manager.update_bot(bot.get("id"), {"following": following})
                            
                            # Add to memory
                            memory_service.add_interaction(
                                bot_id=bot.get("id"),
                                target_id=str(other_bot_id),
                                interaction_type="follow"
                            )
                            
                            # Send to main app
                            _send_subscription_to_main_app(
                                bot_id=bot.get("id"),
                                target_id=str(other_bot_id),
                                action="follow"
                            )
                            
                            # Update other bot's followers count
                            other_bot_manager = BotManager()
                            other_bot_manager.update_bot(
                                other_bot_id,
                                {"followers_count": other_bot.get("followers_count", 0) + 1}
                            )
                            
                            follows.append({
                                "bot_id": bot.get("id"),
                                "target_id": other_bot_id,
                                "target_type": "bot"
                            })
            
            # Process unfollows
            if random.random() < bot.get("unfollow_probability", 0.1):
                following = bot.get("following", [])
                if following:
                    # Select a random target to unfollow
                    target_id = random.choice(following)
                    
                    # Remove from following list
                    following.remove(target_id)
                    bot_manager.update_bot(bot.get("id"), {"following": following})
                    
                    # Add to memory
                    memory_service.add_interaction(
                        bot_id=bot.get("id"),
                        target_id=str(target_id),
                        interaction_type="unfollow"
                    )
                    
                    # Send to main app
                    _send_subscription_to_main_app(
                        bot_id=bot.get("id"),
                        target_id=str(target_id),
                        action="unfollow"
                    )
                    
                    # If target is a bot, update its followers count
                    try:
                        target_id_int = int(target_id)
                        target_bot = bot_manager.get_bot(target_id_int)
                        if target_bot:
                            bot_manager.update_bot(
                                target_id_int,
                                {"followers_count": max(0, target_bot.get("followers_count", 0) - 1)}
                            )
                    except (ValueError, TypeError):
                        # Not a bot ID, probably a user ID
                        pass
                    
                    unfollows.append({
                        "bot_id": bot.get("id"),
                        "target_id": target_id
                    })
        
        return {
            "status": "success",
            "follows": follows,
            "unfollows": unfollows
        }
    
    except Exception as e:
        logger.error(f"Error processing subscriptions: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

def _send_subscription_to_main_app(bot_id: int, target_id: str, action: str) -> bool:
    """
    Send a subscription action to the main app.
    
    Args:
        bot_id: Bot ID
        target_id: Target ID (user or bot)
        action: Action ("follow" or "unfollow")
        
    Returns:
        Boolean indicating success
    """
    try:
        import requests
        
        # Prepare subscription data
        subscription_data = {
            "bot_id": bot_id,
            "target_id": target_id,
            "action": action,
            "timestamp": datetime.now().isoformat()
        }
        
        # Send subscription to main app
        response = requests.post(
            f"{settings.MAIN_APP_URL}/api/subscriptions",
            json=subscription_data,
            headers={
                "Authorization": f"Bearer {settings.MAIN_APP_API_KEY}",
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code == 200:
            logger.info(f"Subscription from bot {bot_id} ({action} {target_id}) sent to main app")
            return True
        else:
            logger.warning(f"Failed to send subscription to main app: {response.status_code} {response.text}")
            return False
    
    except Exception as e:
        logger.error(f"Error sending subscription to main app: {str(e)}")
        return False
