"""
Reaction engine for the Cartouche Autonomous Service.
Handles bot reactions to posts and other content.
"""
import logging
import random
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

from database import Database
from api_client import APIClient
from content_generator import ContentGenerator
from config import REACTION_DELAY_MIN, REACTION_DELAY_MAX

logger = logging.getLogger(__name__)

class ReactionEngine:
    """Engine for generating bot reactions to content."""
    
    def __init__(
        self, 
        database: Optional[Database] = None, 
        api_client: Optional[APIClient] = None,
        content_generator: Optional[ContentGenerator] = None
    ):
        """
        Initialize the reaction engine.
        
        Args:
            database: Database instance
            api_client: API client instance
            content_generator: Content generator instance
        """
        self.database = database or Database()
        self.api_client = api_client or APIClient()
        self.content_generator = content_generator or ContentGenerator()
    
    async def process_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a post and generate bot reactions.
        
        Args:
            post_data: Post data dictionary
            
        Returns:
            Dictionary with reaction statistics
        """
        try:
            # Store post in database
            post_id = await self.database.add_post({
                'post_id': post_data.get('id', 0),
                'user_name': post_data.get('Name', ''),
                'full_name': post_data.get('FullName', ''),
                'avatar': post_data.get('Avatar', ''),
                'text': post_data.get('Text', ''),
                'on_date': post_data.get('OnDate', datetime.now().isoformat()),
                'processed': False,
                'api_data': post_data
            })
            
            # Get bots from database
            bots = await self.database.get_bots()
            
            # Determine which bots will see the post (random subset)
            # In a real system, this would be based on following relationships
            num_bots_to_see = min(len(bots), random.randint(5, 20))
            bots_to_process = random.sample(bots, num_bots_to_see)
            
            # Process reactions
            likes = 0
            comments = 0
            reposts = 0
            
            for bot in bots_to_process:
                # Determine actions based on probability
                should_like = self._should_like_post(bot, post_data)
                should_comment = self._should_comment_on_post(bot, post_data)
                should_repost = self._should_repost_post(bot, post_data)
                
                # Add random delay to make reactions more natural
                delay = random.randint(REACTION_DELAY_MIN, REACTION_DELAY_MAX)
                await asyncio.sleep(delay)
                
                # Process like
                if should_like:
                    try:
                        async with self.api_client as client:
                            await client.like_post(post_data.get('id', 0), bot.get('name', ''))
                        
                        # Record reaction in database
                        await self.database.add_reaction({
                            'bot_id': bot.get('id', 0),
                            'post_id': post_id,
                            'reaction_type': 'like',
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        # Update bot stats
                        await self.database.update_bot(
                            bot.get('id', 0), 
                            {'likes_given': bot.get('likes_given', 0) + 1}
                        )
                        
                        # Record interaction
                        await self.database.add_interaction({
                            'bot_id': bot.get('id', 0),
                            'user_name': post_data.get('Name', ''),
                            'interaction_type': 'like',
                            'content': post_data.get('Text', ''),
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        likes += 1
                    except Exception as e:
                        logger.error(f"Error processing like: {str(e)}")
                
                # Process comment
                if should_comment:
                    try:
                        # Get bot's interaction history with this user
                        interactions = await self.database.get_interactions(bot.get('id', 0), 5)
                        history = "\n".join([f"{i.get('interaction_type')}: {i.get('content')}" for i in interactions])
                        
                        # Generate comment
                        comment_text = await self.content_generator.generate_comment(
                            bot, post_data.get('Text', ''), history
                        )
                        
                        # Create comment data
                        comment_data = {
                            'Name': bot.get('name', ''),
                            'FullName': bot.get('full_name', ''),
                            'Avatar': bot.get('avatar', ''),
                            'Text': comment_text,
                            'OnDate': datetime.now().strftime("%m/%d/%Y"),
                            'LikeComment': 'LikeComment',
                            'Reply': 'Reply'
                        }
                        
                        # Add comment to post
                        async with self.api_client as client:
                            await client.add_comment(post_data.get('id', 0), comment_data)
                        
                        # Record reaction in database
                        await self.database.add_reaction({
                            'bot_id': bot.get('id', 0),
                            'post_id': post_id,
                            'reaction_type': 'comment',
                            'content': comment_text,
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        # Update bot stats
                        await self.database.update_bot(
                            bot.get('id', 0), 
                            {'comments_given': bot.get('comments_given', 0) + 1}
                        )
                        
                        # Record interaction
                        await self.database.add_interaction({
                            'bot_id': bot.get('id', 0),
                            'user_name': post_data.get('Name', ''),
                            'interaction_type': 'comment',
                            'content': f"Post: {post_data.get('Text', '')}\nComment: {comment_text}",
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        comments += 1
                    except Exception as e:
                        logger.error(f"Error processing comment: {str(e)}")
                
                # Process repost (not implemented in API yet)
                if should_repost:
                    try:
                        # Record reaction in database
                        await self.database.add_reaction({
                            'bot_id': bot.get('id', 0),
                            'post_id': post_id,
                            'reaction_type': 'repost',
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        # Update bot stats
                        await self.database.update_bot(
                            bot.get('id', 0), 
                            {'reposts_given': bot.get('reposts_given', 0) + 1}
                        )
                        
                        # Record interaction
                        await self.database.add_interaction({
                            'bot_id': bot.get('id', 0),
                            'user_name': post_data.get('Name', ''),
                            'interaction_type': 'repost',
                            'content': post_data.get('Text', ''),
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        reposts += 1
                    except Exception as e:
                        logger.error(f"Error processing repost: {str(e)}")
            
            # Mark post as processed
            await self.database.update_post(post_id, {'processed': True})
            
            # Return statistics
            return {
                'post_id': post_id,
                'bots_processed': len(bots_to_process),
                'likes': likes,
                'comments': comments,
                'reposts': reposts
            }
        
        except Exception as e:
            logger.error(f"Error processing post: {str(e)}")
            return {
                'post_id': -1,
                'bots_processed': 0,
                'likes': 0,
                'comments': 0,
                'reposts': 0,
                'error': str(e)
            }
    
    def _should_like_post(self, bot: Dict[str, Any], post: Dict[str, Any]) -> bool:
        """
        Determine if a bot should like a post based on probability.
        
        Args:
            bot: Bot data
            post: Post data
            
        Returns:
            Boolean indicating whether the bot should like the post
        """
        # Base probability from bot's characteristics
        base_probability = bot.get("like_probability", 0.5)
        
        # Adjust based on bot category
        category_adjustment = 0
        categories = bot.get("categories", [])
        
        if "fan" in categories:
            category_adjustment += 0.3
        if "hater" in categories:
            category_adjustment -= 0.3
        if "neutral" in categories:
            category_adjustment += 0.0  # No change
        if "silent" in categories:
            category_adjustment -= 0.1
        
        # Adjust based on post content length
        content_adjustment = 0
        post_text = post.get("Text", "")
        if len(post_text) > 200:
            content_adjustment += 0.05  # Slightly more likely to like longer posts
        
        # Calculate final probability
        final_probability = base_probability + category_adjustment + content_adjustment
        
        # Ensure probability is within valid range [0, 1]
        final_probability = max(0.0, min(1.0, final_probability))
        
        # Make decision based on probability
        return random.random() < final_probability
    
    def _should_comment_on_post(self, bot: Dict[str, Any], post: Dict[str, Any]) -> bool:
        """
        Determine if a bot should comment on a post based on probability.
        
        Args:
            bot: Bot data
            post: Post data
            
        Returns:
            Boolean indicating whether the bot should comment on the post
        """
        # Base probability from bot's characteristics
        base_probability = bot.get("comment_probability", 0.2)
        
        # Adjust based on bot category
        category_adjustment = 0
        categories = bot.get("categories", [])
        
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
        
        # Adjust based on post content length
        content_adjustment = 0
        post_text = post.get("Text", "")
        if len(post_text) > 100:
            content_adjustment += 0.1  # More likely to comment on substantial posts
        
        # Calculate final probability
        final_probability = base_probability + category_adjustment + content_adjustment
        
        # Ensure probability is within valid range [0, 1]
        final_probability = max(0.0, min(1.0, final_probability))
        
        # Make decision based on probability
        return random.random() < final_probability
    
    def _should_repost_post(self, bot: Dict[str, Any], post: Dict[str, Any]) -> bool:
        """
        Determine if a bot should repost a post based on probability.
        
        Args:
            bot: Bot data
            post: Post data
            
        Returns:
            Boolean indicating whether the bot should repost the post
        """
        # Base probability (reposting is less common than liking)
        base_probability = bot.get("repost_probability", 0.1)
        
        # Adjust based on bot category
        category_adjustment = 0
        categories = bot.get("categories", [])
        
        if "fan" in categories:
            category_adjustment += 0.15
        if "hater" in categories:
            category_adjustment -= 0.05
        if "neutral" in categories:
            category_adjustment += 0.0  # No change
        if "silent" in categories:
            category_adjustment -= 0.08  # Silent bots repost less
        
        # Calculate final probability
        final_probability = base_probability + category_adjustment
        
        # Ensure probability is within valid range [0, 1]
        final_probability = max(0.0, min(1.0, final_probability))
        
        # Make decision based on probability
        return random.random() < final_probability
