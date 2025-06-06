"""
Monitoring API routes for the Cartouche Bot Service.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import psutil
import time
from datetime import datetime

from app.db.session import get_db
from app.db.repositories.bot_repository import BotRepository
from app.db.repositories.activity_repository import ActivityRepository

from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()

router = APIRouter()

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
        "uptime_seconds": time.time() - SERVICE_START_TIME,
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
    disk_info = psutil.disk_usage("/")

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": time.time() - SERVICE_START_TIME,
        "bot_stats": {"total_bots": bot_count, "categories": bot_categories},
        "activity_stats": {"recent_activities": recent_activity_count},
        "system_stats": {
            "cpu_percent": cpu_percent,
            "memory_percent": memory_info.percent,
            "disk_percent": disk_info.percent,
        },
    }


@router.get("/logs")
async def get_logs(
    lines: int = Query(100, ge=1, le=1000),
    level: str = Query("INFO", regex="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"),
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
