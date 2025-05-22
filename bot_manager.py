"""
Bot manager for the Cartouche Autonomous Service.
Handles bot creation, management, and retrieval.
"""
import logging
import random
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

from database import Database
from api_client import APIClient
from config import (
    BOT_CATEGORIES, INITIAL_BOTS_COUNT, DAILY_BOTS_GROWTH_MIN, 
    DAILY_BOTS_GROWTH_MAX, MAX_BOTS_COUNT
)

logger = logging.getLogger(__name__)

class BotManager:
    """Manager for bot operations."""
    
    def __init__(self, database: Optional[Database] = None, api_client: Optional[APIClient] = None):
        """
        Initialize the bot manager.
        
        Args:
            database: Database instance
            api_client: API client instance
        """
        self.database = database or Database()
        self.api_client = api_client or APIClient()
    
    async def initialize_bots(self) -> bool:
        """
        Initialize the bot population with the initial set of bots.
        
        Returns:
            Boolean indicating success
        """
        try:
            # Check if bots already exist
            bot_count = await self.database.count_bots()
            
            if bot_count > 0:
                logger.info(f"Bots already initialized ({bot_count} bots exist)")
                return True
            
            # Create initial bots
            logger.info(f"Initializing {INITIAL_BOTS_COUNT} bots")
            
            for _ in range(INITIAL_BOTS_COUNT):
                await self.create_bot()
            
            return True
        
        except Exception as e:
            logger.error(f"Error initializing bots: {str(e)}")
            return False
    
    async def create_bot(self, bot_data: Optional[Dict[str, Any]] = None) -> int:
        """
        Create a new bot.
        
        Args:
            bot_data: Optional bot data dictionary
            
        Returns:
            Bot ID
        """
        try:
            # Generate bot data if not provided
            if not bot_data:
                bot_data = self._generate_bot_data()
            
            # Add bot to API
            async with self.api_client as client:
                api_response = await client.add_bot(bot_data)
            
            # Store bot in database
            bot_data['api_data'] = api_response
            bot_id = await self.database.add_bot(bot_data)
            
            logger.info(f"Created new bot: {bot_data.get('name')} (ID: {bot_id})")
            return bot_id
        
        except Exception as e:
            logger.error(f"Error creating bot: {str(e)}")
            return -1
    
    async def grow_bot_population(self) -> int:
        """
        Grow the bot population by adding new bots.
        
        Returns:
            Number of new bots created
        """
        try:
            # Check current bot count
            current_count = await self.database.count_bots()
            
            # If we've reached the maximum, don't add more
            if current_count >= MAX_BOTS_COUNT:
                logger.info(f"Maximum bot count reached ({current_count}/{MAX_BOTS_COUNT})")
                return 0
            
            # Determine how many bots to add
            growth_count = random.randint(DAILY_BOTS_GROWTH_MIN, DAILY_BOTS_GROWTH_MAX)
            
            # Ensure we don't exceed the maximum
            growth_count = min(growth_count, MAX_BOTS_COUNT - current_count)
            
            logger.info(f"Growing bot population by {growth_count} bots")
            
            # Create new bots
            new_bots = 0
            for _ in range(growth_count):
                bot_id = await self.create_bot()
                if bot_id > 0:
                    new_bots += 1
            
            logger.info(f"Added {new_bots} new bots")
            return new_bots
        
        except Exception as e:
            logger.error(f"Error growing bot population: {str(e)}")
            return 0
    
    async def get_bots(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get bots from the database.
        
        Args:
            category: Optional category filter
            
        Returns:
            List of bot dictionaries
        """
        try:
            bots = await self.database.get_bots()
            
            if category:
                # Filter bots by category
                bots = [bot for bot in bots if category in bot.get('categories', [])]
            
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
            return await self.database.get_bot(bot_id)
        
        except Exception as e:
            logger.error(f"Error getting bot {bot_id}: {str(e)}")
            return None
    
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
            return await self.database.update_bot(bot_id, updates)
        
        except Exception as e:
            logger.error(f"Error updating bot {bot_id}: {str(e)}")
            return False
    
    async def process_subscriptions(self) -> int:
        """
        Process bot subscriptions (follow/unfollow).
        
        Returns:
            Number of subscription actions performed
        """
        try:
            # Get all bots
            bots = await self.database.get_bots()
            
            # Get all users
            async with self.api_client as client:
                users = await client.get_users()
            
            # Process each bot's subscriptions
            actions_performed = 0
            
            for bot in bots:
                # Determine if the bot should follow or unfollow someone
                should_follow = random.random() < bot.get('follow_probability', 0.3)
                should_unfollow = random.random() < bot.get('unfollow_probability', 0.1)
                
                if should_follow:
                    # Find a user to follow
                    following = bot.get('following', [])
                    potential_users = [user for user in users if user.get('Name') not in following]
                    
                    if potential_users:
                        user_to_follow = random.choice(potential_users)
                        
                        # Update bot's following list
                        following.append(user_to_follow.get('Name'))
                        await self.database.update_bot(bot['id'], {'following': following})
                        
                        # TODO: Implement API call to follow user
                        
                        actions_performed += 1
                
                if should_unfollow and bot.get('following'):
                    # Find a user to unfollow
                    following = bot.get('following', [])
                    
                    if following:
                        user_to_unfollow = random.choice(following)
                        
                        # Update bot's following list
                        following.remove(user_to_unfollow)
                        await self.database.update_bot(bot['id'], {'following': following})
                        
                        # TODO: Implement API call to unfollow user
                        
                        actions_performed += 1
            
            logger.info(f"Processed {actions_performed} subscription actions")
            return actions_performed
        
        except Exception as e:
            logger.error(f"Error processing subscriptions: {str(e)}")
            return 0
    
    def _generate_bot_data(self) -> Dict[str, Any]:
        """
        Generate random data for a new bot.
        
        Returns:
            Bot data dictionary
        """
        # Generate random age between 18 and 65
        age = random.randint(18, 65)
        
        # Generate random gender
        gender = random.choice(['Male', 'Female', 'Other'])
        
        # Generate random name
        if gender == 'Male':
            first_names = ['John', 'Michael', 'David', 'James', 'Robert', 'William', 'Richard', 'Joseph', 'Thomas', 'Charles']
        elif gender == 'Female':
            first_names = ['Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen']
        else:
            first_names = ['Alex', 'Jordan', 'Taylor', 'Casey', 'Riley', 'Avery', 'Quinn', 'Skyler', 'Reese', 'Morgan']
        
        last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor']
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        full_name = f"{first_name} {last_name}"
        
        # Generate username
        username = f"{first_name.lower()}{random.randint(1, 999)}"
        
        # Generate random categories (1-3)
        num_categories = random.randint(1, 3)
        categories = random.sample(BOT_CATEGORIES, num_categories)
        
        # Generate avatar filename
        avatar = f"{username}.jpg"
        
        # Generate probabilities based on categories
        like_probability = 0.5
        comment_probability = 0.2
        post_probability = 0.1
        follow_probability = 0.3
        unfollow_probability = 0.1
        repost_probability = 0.05
        
        # Adjust probabilities based on categories
        if 'fan' in categories:
            like_probability += 0.2
            comment_probability += 0.1
        if 'hater' in categories:
            like_probability -= 0.2
            comment_probability += 0.1
        if 'silent' in categories:
            comment_probability -= 0.1
            post_probability -= 0.05
        if 'humorous' in categories:
            comment_probability += 0.2
        if 'provocative' in categories:
            comment_probability += 0.2
        
        # Ensure probabilities are within valid range [0, 1]
        like_probability = max(0.1, min(0.9, like_probability))
        comment_probability = max(0.05, min(0.8, comment_probability))
        post_probability = max(0.01, min(0.5, post_probability))
        
        # Generate prompt for bot personality
        prompt = self._generate_personality_prompt(categories, age, gender)
        
        # Create bot data dictionary
        bot_data = {
            "Age": age,
            "Avatar": avatar,
            "FullName": full_name,
            "Gender": gender,
            "IsBot": True,
            "Name": username,
            "OnDate": datetime.now().strftime("%m/%d/%Y"),
            "Password": "bot",
            "Prompt": prompt,
            "Following": [],
            "categories": categories,
            "like_probability": like_probability,
            "comment_probability": comment_probability,
            "post_probability": post_probability,
            "follow_probability": follow_probability,
            "unfollow_probability": unfollow_probability,
            "repost_probability": repost_probability
        }
        
        return bot_data
    
    def _generate_personality_prompt(self, categories: List[str], age: int, gender: str) -> str:
        """
        Generate a personality prompt for a bot.
        
        Args:
            categories: Bot categories
            age: Bot age
            gender: Bot gender
            
        Returns:
            Personality prompt
        """
        prompts = {
            'fan': [
                "энтузиаст, который поддерживает других",
                "позитивный человек, который видит хорошее во всем",
                "преданный поклонник, который всегда поддерживает"
            ],
            'hater': [
                "критически настроенный скептик",
                "человек, который часто не согласен с большинством",
                "циничный критик"
            ],
            'silent': [
                "молчаливый наблюдатель",
                "интроверт, который редко комментирует",
                "тихий созерцатель"
            ],
            'random': [
                "непредсказуемый и эксцентричный",
                "человек с переменчивым настроением",
                "спонтанный и непоследовательный"
            ],
            'neutral': [
                "объективный и беспристрастный",
                "рациональный аналитик",
                "сбалансированный в своих взглядах"
            ],
            'humorous': [
                "шутник с хорошим чувством юмора",
                "саркастичный комментатор",
                "любитель мемов и шуток"
            ],
            'provocative': [
                "провокатор, который любит вызывать дискуссии",
                "задает сложные вопросы",
                "любит играть роль адвоката дьявола"
            ],
            'roleplay': [
                "часто притворяется кем-то другим",
                "любит примерять разные роли",
                "меняет свою личность в зависимости от контекста"
            ]
        }
        
        # Select random prompt for each category
        selected_prompts = []
        for category in categories:
            if category in prompts:
                selected_prompts.append(random.choice(prompts[category]))
        
        # Add age and gender context
        age_context = ""
        if age < 25:
            age_context = "молодой"
        elif age < 40:
            age_context = "взрослый"
        elif age < 60:
            age_context = "зрелый"
        else:
            age_context = "пожилой"
        
        gender_context = ""
        if gender == "Male":
            gender_context = "мужчина"
        elif gender == "Female":
            gender_context = "женщина"
        else:
            gender_context = "человек"
        
        # Combine prompts
        combined_prompt = f"{age_context} {gender_context}, {', '.join(selected_prompts)}"
        
        return combined_prompt
