"""
Bot manager service for the Cartouche Bot Service.
Handles creation, management, and scheduling of bots.
"""

from typing import Dict, Any
import random
from datetime import datetime, timedelta
import aiohttp
from sqlalchemy.exc import SQLAlchemyError

from app.db.repositories.bot_repository import BotRepository
from app.db.repositories.activity_repository import ActivityRepository
from app.services.content_generator import ContentGenerator
from app.utils.avatar_generator import AvatarGenerator
from app.utils.username_generator import UsernameGenerator
from app.clients.cartouche_api import CartoucheAPIClient
from app.core.settings import (
    SOCIAL_NETWORK_URL,
    API_KEY,
    BOT_CATEGORIES,
    INITIAL_BOTS_COUNT,
    DAILY_BOTS_GROWTH_MIN,
    DAILY_BOTS_GROWTH_MAX,
    MAX_BOTS_COUNT,
    AVATAR_STYLES,
    BOT_PROMPTS,
    REACTION_DELAY_MIN,
    REACTION_DELAY_MAX,
    MAX_COMMENTS_PER_POST,
)
from app.models.models import BotResponse
from app.core.exceptions import BotError
from app.core.logging import setup_logging
from app.services.memory_service import MemoryService

# Setup logging
logger = setup_logging()


class BotManager:
    """Service for managing bots."""

    def __init__(
        self,
        bot_repository: BotRepository,
        activity_repository: ActivityRepository,
        content_generator: ContentGenerator,
        api_client: CartoucheAPIClient,
        memory_service: MemoryService,
    ):
        """
        Initialize the bot manager.

        Args:
            bot_repository: Bot repository
            activity_repository: Activity repository
            content_generator: Content generator
            api_client: API client
        """
        self.bot_repository = bot_repository
        self.activity_repository = activity_repository
        self.content_generator = content_generator
        self.api_client = api_client
        self.memory_service = memory_service

    async def initialize_bots(self) -> int:
        """
        Initialize the bot population if needed.

        Returns:
            Number of bots created
        """
        bot_count = self.bot_repository.count_bots()

        if bot_count < INITIAL_BOTS_COUNT:
            bots_to_create = INITIAL_BOTS_COUNT - bot_count
            logger.info(f"Initializing {bots_to_create} bots")

            created_count = 0
            for _ in range(bots_to_create):
                try:
                    await self.create_random_bot()
                    created_count += 1
                except Exception as e:
                    logger.error(f"Failed to create bot: {str(e)}")

            return created_count

        return 0

    async def daily_growth(self) -> int:
        """
        Handle daily growth of bot population.

        Returns:
            Number of bots created
        """
        bot_count = self.bot_repository.count_bots()

        if bot_count >= MAX_BOTS_COUNT:
            logger.info(f"Maximum bot count reached: {bot_count}")
            return 0

        growth = random.randint(DAILY_BOTS_GROWTH_MIN, DAILY_BOTS_GROWTH_MAX)
        growth = min(growth, MAX_BOTS_COUNT - bot_count)

        logger.info(f"Daily growth: creating {growth} new bots")

        created_count = 0
        for _ in range(growth):
            try:
                await self.create_random_bot()
                created_count += 1
            except Exception as e:
                logger.error(f"Failed to create bot: {str(e)}")

        return created_count

    async def create_random_bot(self) -> Dict[str, Any]:
        """
        Create a random bot with generated attributes.

        Returns:
            Created bot data

        Raises:
            BotError: If bot creation fails
        """
        try:
            # Generate random attributes
            category = random.choice(list(BOT_CATEGORIES.keys()))
            gender = random.choice(["Male", "Female"])
            age = random.randint(18, 65)

            # Generate unique username and description
            username = await UsernameGenerator.generate_username(self.bot_repository)
            full_name = await self.content_generator.generate_full_name(gender, age)
            description = await self.content_generator.generate_bot_description(
                category, age, gender
            )

            # Generate avatar
            avatar_style = random.choice(AVATAR_STYLES)
            avatar = await AvatarGenerator.generate_dicebear_avatar(avatar_style)

            # Set probabilities based on category
            category_probs = BOT_CATEGORIES.get(category, {})
            like_probability = category_probs.get("like_probability", 0.5)
            comment_probability = category_probs.get("comment_probability", 0.3)
            follow_probability = category_probs.get("follow_probability", 0.4)
            unfollow_probability = category_probs.get("unfollow_probability", 0.2)
            post_probability = category_probs.get("post_probability", 0.1)

            # Add some randomness to probabilities
            like_probability += random.uniform(-0.1, 0.1)
            comment_probability += random.uniform(-0.1, 0.1)
            follow_probability += random.uniform(-0.1, 0.1)
            unfollow_probability += random.uniform(-0.1, 0.1)
            post_probability += random.uniform(-0.05, 0.05)

            # Ensure probabilities are within bounds
            like_probability = max(0.1, min(0.9, like_probability))
            comment_probability = max(0.1, min(0.9, comment_probability))
            follow_probability = max(0.1, min(0.9, follow_probability))
            unfollow_probability = max(0.1, min(0.9, unfollow_probability))
            post_probability = max(0.0, min(0.3, post_probability))

            # Create bot in local database
            bot_data = {
                "name": username,
                "full_name": full_name,
                "avatar": avatar,
                "age": age,
                "gender": gender,
                "prompt": BOT_PROMPTS.get(category, ""),
                "category": category,
                "description": description,
                "like_probability": like_probability,
                "comment_probability": comment_probability,
                "follow_probability": follow_probability,
                "unfollow_probability": unfollow_probability,
                "post_probability": post_probability,
            }

            bot = self.bot_repository.create_bot(bot_data)

            # Create bot in C# API
            api_bot_data = {
                "Age": age,
                "Avatar": avatar,
                "FullName": full_name,
                "Gender": gender,
                "IsBot": True,
                "Name": username,
                "OnDate": datetime.utcnow().strftime("%m/%d/%Y"),
                "Password": "bot",
                "Prompt": BOT_PROMPTS.get(category, ""),
                "Description": description,
                "Category": category,
                "Following": [],
                "Settings": {
                    "like_probability": like_probability,
                    "comment_probability": comment_probability,
                    "follow_probability": follow_probability,
                    "unfollow_probability": unfollow_probability,
                    "post_probability": post_probability,
                },
            }

            await self.api_client.add_bot(api_bot_data)

            return BotResponse.from_orm(bot)

        except Exception as e:
            logger.error(f"Failed to create random bot: {str(e)}")
            raise BotError(f"Failed to create random bot: {str(e)}")

    async def schedule_bot_activities(self) -> None:
        """
        Schedule activities for all bots.
        This should be called periodically to ensure bots remain active.
        """
        bots = self.bot_repository.get_all_bots(limit=MAX_BOTS_COUNT)

        for bot in bots:
            # Schedule next activity time
            hours_delay = random.uniform(0.1, 3)  # Between 6 minutes and 3 hours
            next_activity = datetime.utcnow() + timedelta(hours=hours_delay)

            # Update bot's last active time
            self.bot_repository.update_bot(bot.id, {"last_active": next_activity})

    async def process_bot_activity(self, bot_id: int) -> Dict[str, Any]:
        """
        Process activity for a specific bot.

        Args:
            bot_id: Bot ID

        Returns:
            Activity result

        Raises:
            BotError: If activity processing fails
        """
        try:
            bot_id_val = int(bot_id) if not isinstance(bot_id, int) else bot_id
            bot = self.bot_repository.get_bot_by_id(bot_id_val)
            if not bot:
                raise BotError(f"Bot with ID {bot_id} not found")

            # Update last active time
            self.bot_repository.update_last_active(bot_id_val)

            # Get recent posts
            posts = await self.api_client.get_posts()
            if not posts:
                logger.info(f"No posts available for bot {getattr(bot, 'name', '')} to react to")
                return {"status": "no_posts", "bot_id": bot_id_val}

            # Filter posts from the last 3 days (including today)
            now = datetime.utcnow()
            three_days_ago = now - timedelta(days=2)
            recent_posts = []
            for post in posts:
                on_date_str = post.get("date")
                post_date = None
                if on_date_str:
                    try:
                        post_date = datetime.strptime(on_date_str[:19], "%Y-%m-%dT%H:%M:%S")
                    except Exception:
                        continue
                if (
                    post_date
                    and three_days_ago.date() <= post_date.date() <= now.date()
                ):
                    recent_posts.append(post)

            if not recent_posts:
                logger.info(
                    f"No recent posts (last 3 days) for bot {getattr(bot, 'name', '')} to react to"
                )
                return {"status": "no_recent_posts", "bot_id": bot_id_val}

            # Select a random recent post
            post = random.choice(recent_posts)
            post_id = post.get("id")

            # Split the post into parts (new structure)
            text = post.get("content", "")
            user = post.get("user", {})
            author = user.get("name", "")
            author_name = user.get("username", None)
            date = post.get("date", "")
            comments_count = post.get("comments_count", 0)
            likes = post.get("reactions_count", 0)

            formatted_comments = f"Comments count: {comments_count}" if comments_count else "No comments"

            post_info = f"Author: {author}\nDate: {date}\nText: {text}\nComments:\n{formatted_comments}\nLikes: {likes}"

            # Check if bot has already interacted with this post
            has_liked = bool(self.activity_repository.check_activity_exists(
                bot_id_val, "like", post_id
            ))
            comment_activities = self.activity_repository.get_activities_by_type(
                bot_id_val, "comment", 0, 1000
            )
            comment_count_on_post = sum(
                1 for a in comment_activities if str(a.target_id) == str(post_id)
            )

            comment_probability = float(getattr(bot, "comment_probability", 0.3)) * (0.5 ** comment_count_on_post)
            has_followed = bool(self.activity_repository.check_activity_exists(
                bot_id_val, "follow", author_name
            ))

            action_taken = False

            # Try to like
            if not has_liked and random.random() < float(getattr(bot, "like_probability", 0.5)):
                try:
                    await self.api_client.like_post(post_id, str(getattr(bot, "name", "")))
                    self.activity_repository.create_activity(
                        {
                            "bot_id": bot_id_val,
                            "activity_type": "like",
                            "target_id": str(post_id),
                        }
                    )
                    memory_text = await self.content_generator.generate_memory(
                        str(getattr(bot, "category", "")), text, "post"
                    )
                    await self.memory_service.add_memory(
                        bot_id_val,
                        memory_text,
                        {"context_type": "post", "context_id": str(post_id)},
                    )
                    action_taken = True
                    logger.info(f"Bot {getattr(bot, 'name', '')} liked post {post_id}")
                except Exception as e:
                    logger.error(f"Failed to like post: {str(e)}")

            # Try to comment
            if (
                comment_count_on_post < MAX_COMMENTS_PER_POST
                and random.random() < comment_probability
            ):
                try:
                    search_results = await self.memory_service.search_memories(
                        bot_id_val, text, limit=3
                    )
                    memory_texts = [m["text"] for m in search_results]
                    comment_text = await self.content_generator.generate_comment(
                        str(getattr(bot, "category", "")), post_info, memory_texts
                    )
                    comment_data = {
                        "Name": str(getattr(bot, "name", "")),
                        "Text": comment_text,
                        "OnDate": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                    }
                    await self.api_client.add_comment(post_id, comment_data)
                    self.activity_repository.create_activity(
                        {
                            "bot_id": bot_id_val,
                            "activity_type": "comment",
                            "target_id": str(post_id),
                            "content": comment_text,
                        }
                    )
                    action_taken = True
                    logger.info(f"Bot {getattr(bot, 'name', '')} commented on post {post_id}")
                except Exception as e:
                    logger.error(f"Failed to comment on post: {str(e)}")

                # Try to follow the post author (if not self, and not already followed)
                if (
                    not has_followed
                    and author_name
                    and author_name != str(getattr(bot, "name", ""))
                    and random.random() < float(getattr(bot, "follow_probability", 0.4))
                ):
                    try:
                        await self.api_client.follow_user(author_name, str(getattr(bot, "name", "")))
                        self.activity_repository.create_activity(
                            {
                                "bot_id": bot_id_val,
                                "activity_type": "follow",
                                "target_id": str(author_name),
                            }
                        )
                        logger.info(f"Bot {getattr(bot, 'name', '')} followed user {author_name}")
                        return {
                            "status": "followed",
                            "bot_id": bot_id_val,
                            "user_id": author_name,
                        }
                    except Exception as e:
                        logger.error(f"Failed to follow user: {str(e)}")

            if not action_taken:
                logger.info(
                    f"Bot {getattr(bot, 'name', '')} decided not to interact with post {post_id}"
                )
                return {"status": "no_action", "bot_id": bot_id_val}

            return {"status": "success", "bot_id": bot_id_val, "post_id": post_id}

    async def create_bot_post(self, bot_id: int) -> Dict[str, Any]:
        """
        Create a post for a specific bot.

        Args:
            bot_id: Bot ID

        Returns:
            Post data

        Raises:
            BotError: If post creation fails
        """
        try:
            bot_id_val = int(bot_id) if not isinstance(bot_id, int) else bot_id
            bot = self.bot_repository.get_bot_by_id(bot_id_val)
            if not bot:
                raise BotError(f"Bot with ID {bot_id} not found")

            # Generate post content
            post_text = await self.content_generator.generate_post(str(getattr(bot, "category", "")))

            # Create post data
            post_data = {
                "Name": str(getattr(bot, "name", "")),
                "Text": post_text,
                "OnDate": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
            }

            # Add post to API
            response = await self.api_client.add_post(post_data)

            # Record activity
            self.activity_repository.create_activity(
                {
                    "bot_id": bot_id_val,
                    "activity_type": "post",
                    "target_id": str(response.get("docID", "")),
                    "content": post_text,
                }
            )

            logger.info(f"Bot {getattr(bot, 'name', '')} created post")

            return {"status": "success", "bot_id": bot_id_val, "post": post_data}

        except Exception as e:
            logger.error(f"Failed to create bot post: {str(e)}")
            raise BotError(f"Failed to create bot post: {str(e)}")

    async def run_due_bot_activities(self) -> None:
        """
        Run activities for all bots whose scheduled activity time has come.
        This should be called periodically to make bots act autonomously.
        """
        now = datetime.utcnow()
        bots = self.bot_repository.get_all_bots(limit=10000)
        for bot in bots:
            last_active = getattr(bot, "last_active", None)
            if last_active is None or last_active <= now:
                try:
                    await self.process_bot_activity(int(getattr(bot, "id")))
                    # Occasionally the bot makes a post
                    if random.random() < float(getattr(bot, "post_probability", 0.1)):
                        await self.create_bot_post(int(getattr(bot, "id")))
                except Exception as e:
                    logger.error(
                        f"Failed to run activity for bot {getattr(bot, 'name', getattr(bot, 'id', ''))}: {str(e)}"
                    )
                # Reschedule the next activity time
                minutes_delay = random.uniform(REACTION_DELAY_MIN, REACTION_DELAY_MAX)
                next_activity = now + timedelta(minutes=minutes_delay)
                self.bot_repository.update_bot(int(getattr(bot, "id")), {"last_active": next_activity})

    async def sync_bots_with_external_api(self) -> int:
        """
        Synchronize bots with the main API (fetch all bots with IsBot=true and update local DB).
        Returns:
            Number of bots synchronized
        """
        from app.core.settings import API_KEY as API_TOKEN, SOCIAL_NETWORK_URL as API_BASE_URL
        url = f'{API_BASE_URL}/GetDocuments/Users/?token={API_TOKEN}&query={{"IsBot":true}}'
        logger.info("Starting bot synchronization with external API...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        logger.error(
                            f"Failed to fetch bots from API: {response.status}"
                        )
                        return 0
                    data = await response.json()
        except Exception as e:
            logger.error(f"Error fetching bots from API: {str(e)}")
            return 0

        external_bots = {
            item["json"]["Name"]: item
            for item in data
            if "json" in item and item["json"].get("IsBot")
        }
        local_bots = {b.name: b for b in self.bot_repository.get_all_bots(limit=10000)}

        updated = 0
        for name, ext in external_bots.items():
            ext_json = ext["json"]
            bot_data = {
                "name": ext_json["Name"],
                "full_name": ext_json.get("FullName", ""),
                "avatar": ext_json.get("Avatar", ""),
                "age": ext_json.get("Age", 0),
                "gender": ext_json.get("Gender", ""),
                "prompt": ext_json.get("Prompt", ""),
                "category": ext_json.get("Category", ""),
                "description": ext_json.get("Description", ""),
                "like_probability": ext_json.get("Settings", {}).get(
                    "like_probability", 0.0
                ),
                "comment_probability": ext_json.get("Settings", {}).get(
                    "comment_probability", 0.0
                ),
                "follow_probability": ext_json.get("Settings", {}).get(
                    "follow_probability", 0.0
                ),
                "unfollow_probability": ext_json.get("Settings", {}).get(
                    "unfollow_probability", 0.0
                ),
                "post_probability": ext_json.get("Settings", {}).get(
                    "post_probability", 0.0
                ),
            }
            if name in local_bots:
                try:
                    self.bot_repository.update_bot(int(getattr(local_bots[name], "id")), bot_data)
                    self.memory_service._get_bot_vector_store(int(getattr(local_bots[name], "id")))
                    updated += 1
                except SQLAlchemyError as e:
                    logger.error(f"Failed to update bot {name}: {str(e)}")
            else:
                try:
                    new_bot = self.bot_repository.create_bot(bot_data)
                    self.memory_service._get_bot_vector_store(int(getattr(new_bot, "id")))
                    updated += 1
                except SQLAlchemyError as e:
                    logger.error(f"Failed to create bot {name}: {str(e)}")

        for name, bot in local_bots.items():
            if name not in external_bots:
                self.bot_repository.delete_bot(int(getattr(bot, "id")))

        logger.info(f"Bot synchronization with external API and local DB complete. Synced {updated} bots.")

        try:
            logger.info("Starting qDrant collections cleanup...")
            local_db_bots = self.bot_repository.get_all_bots(limit=10000)
            local_bot_ids = [int(getattr(bot, "id")) for bot in local_db_bots]

            qdrant_bot_ids = self.memory_service.get_all_bot_collection_names()

            deleted_collections_count = 0
            for bot_id_qdrant in qdrant_bot_ids:
                if bot_id_qdrant not in local_bot_ids:
                    try:
                        await self.memory_service.delete_bot_memories(bot_id_qdrant)
                        logger.info(f"Deleted qDrant collection for bot_id {bot_id_qdrant} as bot no longer exists in local DB.")
                        deleted_collections_count +=1
                    except Exception as e:
                        logger.error(f"Failed to delete qDrant collection for bot_id qdrant: {str(e)}")

            if deleted_collections_count > 0:
                logger.info(f"qDrant collections cleanup complete. Deleted {deleted_collections_count} collections.")
            else:
                logger.info("qDrant collections cleanup complete. No orphaned collections found.")

        except Exception as e:
            logger.error(f"An error occurred during qDrant collections cleanup: {str(e)}")

        return updated
