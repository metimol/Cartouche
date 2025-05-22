"""
Monitoring API routes for the Cartouche Bot Service.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import logging
import psutil
import time
from datetime import datetime, timedelta

from app.db.session import get_db
from app.db.repositories.bot_repository import BotRepository
from app.db.repositories.activity_repository import ActivityRepository
from app.services.reaction_engine import ReactionEngine
from app.services.bot_manager import BotManager
from app.services.content_generator import ContentGenerator
from app.clients.cartouche_api import CartoucheAPIClient

router = APIRouter()
logger = logging.getLogger(__name__)

# Track service start time
SERVICE_START_TIME = time.time()

@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": time.time() - SERVICE_START_TIME
    }

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Get system statistics.
    """
    bot_repository = BotRepository(db)
    activity_repository = ActivityRepository(db)
    
    # Get bot statistics
    bot_count = bot_repository.count_bots()
    bot_categories = bot_repository.count_bots_by_category()
    
    # Get activity statistics
    recent_activities = activity_repository.get_recent_activities(limit=10)
    recent_activity_count = len(recent_activities)
    
    # Get system resource usage
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": time.time() - SERVICE_START_TIME,
        "bot_stats": {
            "total_bots": bot_count,
            "categories": bot_categories
        },
        "activity_stats": {
            "recent_activities": recent_activity_count
        },
        "system_stats": {
            "cpu_percent": cpu_percent,
            "memory_percent": memory_info.percent,
            "disk_percent": disk_info.percent
        }
    }

@router.get("/reactions")
async def get_pending_reactions(db: Session = Depends(get_db)):
    """
    Get pending reactions.
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
        api_client=api_client
    )
    
    reaction_engine = ReactionEngine(
        bot_repository=bot_repository,
        bot_manager=bot_manager
    )
    
    # Get scheduled reactions
    scheduled_reactions = reaction_engine.get_scheduled_reactions()
    pending_count = reaction_engine.get_pending_reactions_count()
    
    return {
        "pending_count": pending_count,
        "scheduled_reactions": scheduled_reactions
    }

@router.get("/logs")
async def get_logs(
    lines: int = Query(100, ge=1, le=1000),
    level: str = Query("INFO", regex="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
):
    """
    Get application logs.
    """
    from app.core.settings import LOG_FILE
    import os
    
    if not os.path.exists(LOG_FILE):
        return {"logs": [], "message": "Log file not found"}
    
    try:
        with open(LOG_FILE, "r") as f:
            all_lines = f.readlines()
            
        # Filter by level if specified
        if level:
            filtered_lines = [line for line in all_lines if f"| {level}" in line]
        else:
            filtered_lines = all_lines
        
        # Get the last N lines
        last_lines = filtered_lines[-lines:]
        
        return {"logs": last_lines}
    except Exception as e:
        logger.error(f"Failed to read logs: {str(e)}")
        return {"logs": [], "error": str(e)}
