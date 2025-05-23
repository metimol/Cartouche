"""
Admin API routes for the Cartouche Bot Service.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import logging

from app.db.session import get_db
from app.db.repositories.bot_repository import BotRepository
from app.db.repositories.memory_repository import MemoryRepository
from app.db.repositories.activity_repository import ActivityRepository
from app.services.bot_manager import BotManager
from app.services.content_generator import ContentGenerator
from app.clients.cartouche_api import CartoucheAPIClient
from app.models.models import (
    BotResponse,
    BotCreate,
    BotUpdate,
    ActivityResponse,
    AdminSystemStats,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/stats", response_model=AdminSystemStats)
async def get_system_stats(db: Session = Depends(get_db)):
    """
    Get system statistics.
    """
    bot_repository = BotRepository(db)
    activity_repository = ActivityRepository(db)

    # Get bot count
    bot_count = bot_repository.count_bots()

    # Get category counts
    category_counts = bot_repository.count_bots_by_category()

    # Get recent activities
    recent_activities = activity_repository.get_recent_activities(limit=20)

    # Convert to response model
    return AdminSystemStats(
        total_bots=bot_count,
        active_bots=len(bot_repository.get_active_bots(hours=24)),
        api_calls=0,  # This would need to be tracked separately
        llm_calls=0,  # This would need to be tracked separately
        uptime=0,  # This would need to be calculated from service start time
        errors=0,  # This would need to be tracked separately
    )


@router.get("/bots", response_model=List[BotResponse])
async def get_all_bots(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get all bots with optional filtering.
    """
    bot_repository = BotRepository(db)

    if category:
        bots = bot_repository.get_bots_by_category(category, skip, limit)
    else:
        bots = bot_repository.get_all_bots(skip, limit)

    return [BotResponse.from_orm(bot) for bot in bots]


@router.post("/bots", response_model=BotResponse)
async def create_bot(
    bot: BotCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    """
    Create a new bot.
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

    # Create bot
    async with api_client:
        bot_data = await bot_manager.create_random_bot()

    # Get created bot
    created_bot = bot_repository.get_bot_by_name(bot_data["name"])

    return BotResponse.from_orm(created_bot)


@router.get("/bots/{bot_id}", response_model=BotResponse)
async def get_bot(bot_id: int, db: Session = Depends(get_db)):
    """
    Get a specific bot by ID.
    """
    bot_repository = BotRepository(db)
    bot = bot_repository.get_bot_by_id(bot_id)

    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    return BotResponse.from_orm(bot)


@router.put("/bots/{bot_id}", response_model=BotResponse)
async def update_bot(bot_id: int, bot_update: BotUpdate, db: Session = Depends(get_db)):
    """
    Update a specific bot.
    """
    bot_repository = BotRepository(db)
    bot = bot_repository.get_bot_by_id(bot_id)

    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    # Update bot
    updated_bot = bot_repository.update_bot(bot_id, bot_update.dict(exclude_unset=True))

    return BotResponse.from_orm(updated_bot)


@router.delete("/bots/{bot_id}")
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


@router.post("/bots/{bot_id}/post")
async def create_bot_post(
    bot_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
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


@router.get("/activities", response_model=List[ActivityResponse])
async def get_recent_activities(
    limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)
):
    """
    Get recent bot activities.
    """
    activity_repository = ActivityRepository(db)
    activities = activity_repository.get_recent_activities(limit=limit)

    return [ActivityResponse.from_orm(activity) for activity in activities]
