"""
Bot API routes for the Cartouche Bot Service.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.db.repositories.bot_repository import BotRepository
from app.db.repositories.memory_repository import MemoryRepository
from app.db.repositories.activity_repository import ActivityRepository
from app.services.bot_manager import BotManager
from app.services.reaction_engine import ReactionEngine
from app.services.content_generator import ContentGenerator
from app.clients.cartouche_api import CartoucheAPIClient
from app.models.models import (
    BotResponse,
    ActivityResponse,
    MemoryResponse,
)

from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()

router = APIRouter()


@router.get("/activities", response_model=List[ActivityResponse])
async def get_recent_activities(
    limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)
):
    """
    Get recent activities from all bots.
    """
    activity_repository = ActivityRepository(db)
    activities = activity_repository.get_recent_activities(limit=limit)

    return [ActivityResponse.from_orm(activity) for activity in activities]


@router.get("/", response_model=List[BotResponse])
async def get_bots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all bots with pagination.
    """
    bot_repository = BotRepository(db)
    bots = bot_repository.get_all_bots(skip, limit)

    return [BotResponse.from_orm(bot) for bot in bots]


@router.get("/{bot_id}", response_model=BotResponse)
async def get_bot(bot_id: int, db: Session = Depends(get_db)):
    """
    Get a specific bot by ID.
    """
    bot_repository = BotRepository(db)
    bot = bot_repository.get_bot_by_id(bot_id)

    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    return BotResponse.from_orm(bot)


@router.delete("/{bot_id}")
async def delete_bot(bot_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific bot.
    """
    bot_repository = BotRepository(db)
    bot = bot_repository.get_bot_by_id(bot_id)

    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    # Delete bot
    bot_repository.delete_bot(bot_id)

    return {"message": f"Bot {bot_id} deleted successfully"}


@router.get("/{bot_id}/activities", response_model=List[ActivityResponse])
async def get_bot_activities(
    bot_id: int,
    skip: int = 0,
    limit: int = 100,
    activity_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get activities for a specific bot.
    """
    bot_repository = BotRepository(db)
    activity_repository = ActivityRepository(db)

    bot = bot_repository.get_bot_by_id(bot_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    if activity_type:
        activities = activity_repository.get_activities_by_type(
            bot_id, activity_type, skip, limit
        )
    else:
        activities = activity_repository.get_activities_by_bot_id(bot_id, skip, limit)

    return [ActivityResponse.from_orm(activity) for activity in activities]


@router.get("/{bot_id}/memories", response_model=List[MemoryResponse])
async def get_bot_memories(
    bot_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Get memories for a specific bot.
    """
    bot_repository = BotRepository(db)
    memory_repository = MemoryRepository(db)

    bot = bot_repository.get_bot_by_id(bot_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    memories = memory_repository.get_memories_by_bot_id(bot_id, skip, limit)

    return [MemoryResponse.from_orm(memory) for memory in memories]


@router.post("/{bot_id}/react")
async def trigger_bot_reaction(bot_id: int, db: Session = Depends(get_db)):
    """
    Trigger a reaction from a specific bot to a post.
    """
    bot_repository = BotRepository(db)
    memory_repository = MemoryRepository(db)
    activity_repository = ActivityRepository(db)
    content_generator = ContentGenerator()
    api_client = CartoucheAPIClient()

    bot = bot_repository.get_bot_by_id(bot_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    bot_manager = BotManager(
        bot_repository=bot_repository,
        memory_repository=memory_repository,
        activity_repository=activity_repository,
        content_generator=content_generator,
        api_client=api_client,
    )

    # Process bot activity
    async with api_client:
        result = await bot_manager.process_bot_activity(bot_id)

    return result


@router.post("/{bot_id}/post")
async def create_bot_post(bot_id: int, db: Session = Depends(get_db)):
    """
    Create a post for a specific bot.
    """
    bot_repository = BotRepository(db)
    memory_repository = MemoryRepository(db)
    activity_repository = ActivityRepository(db)
    content_generator = ContentGenerator()
    api_client = CartoucheAPIClient()

    bot = bot_repository.get_bot_by_id(bot_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    bot_manager = BotManager(
        bot_repository=bot_repository,
        memory_repository=memory_repository,
        activity_repository=activity_repository,
        content_generator=content_generator,
        api_client=api_client,
    )

    # Create post
    async with api_client:
        result = await bot_manager.create_bot_post(bot_id)

    return result


@router.post("/react-to-post")
async def schedule_reactions_to_post(
    post_id: str, post_author: str, db: Session = Depends(get_db)
):
    """
    Schedule bot reactions to a new post.
    """
    bot_repository = BotRepository(db)
    memory_repository = MemoryRepository(db)
    activity_repository = ActivityRepository(db)
    content_generator = ContentGenerator()
    api_client = CartoucheAPIClient()

    bot_manager = BotManager(
        bot_repository=bot_repository,
        memory_repository=memory_repository,
        activity_repository=activity_repository,
        content_generator=content_generator,
        api_client=api_client,
    )

    reaction_engine = ReactionEngine(
        bot_repository=bot_repository, bot_manager=bot_manager
    )

    # Schedule reactions
    result = await reaction_engine.schedule_reactions_for_post(post_id, post_author)

    return result
