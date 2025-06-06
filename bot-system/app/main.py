"""
Main FastAPI application for the Cartouche Bot Service.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import setup_logging
from app.core.exceptions import setup_exception_handlers
from app.db.session import get_db, engine, Base, SessionLocal
from app.services.scheduler import Scheduler
from app.api.routes import router
from app.core.settings import MONITORING_INTERVAL

from app.services.bot_manager import BotManager
from app.services.content_generator import ContentGenerator
from app.clients.cartouche_api import CartoucheAPIClient
from app.db.repositories.bot_repository import BotRepository
from app.db.repositories.activity_repository import ActivityRepository
from app.services.memory_service import MemoryService

# Setup logging
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title="Cartouche Bot Service",
    description="API for managing autonomous AI bots in the Cartouche social network simulator",
    version="1.1.0",
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup exception handlers
setup_exception_handlers(app)

# Create scheduler instance
scheduler = Scheduler()

# Include routers
app.include_router(router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    logger.info("Starting Cartouche Bot Service")

    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Start scheduler
    await scheduler.start()

    # Initialize background tasks
    await initialize_background_tasks()


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Shutting down Cartouche Bot Service")

    # Stop scheduler
    await scheduler.stop()


async def initialize_background_tasks():
    """Initialize background tasks with sequential startup, then schedule periodic tasks."""
    # 1. First, synchronize with the external API
    await sync_bots_with_external_api_task()
    # 2. Then initialize bots
    await initialize_bots()
    # 3. Then run pending activities
    await run_due_bot_activities()

    # After the initial run, schedule tasks as periodic
    scheduler.schedule_task(
        sync_bots_with_external_api_task,
        delay=1800,  # In 30 minutes
        interval=1800,  # Every 30 minutes
        task_id="sync_bots_with_external_api",
    )
    scheduler.schedule_task(
        initialize_bots,
        delay=86400,  # In 24 hours
        interval=None,  # Only once
        task_id="initialize_bots",
    )
    scheduler.schedule_task(
        daily_bot_growth,
        delay=86400,  # In 24 hours
        interval=86400,  # Every day
        task_id="daily_bot_growth",
    )
    scheduler.schedule_task(
        run_due_bot_activities,
        delay=MONITORING_INTERVAL,  # In MONITORING_INTERVAL seconds
        interval=MONITORING_INTERVAL,  # Every MONITORING_INTERVAL seconds
        task_id="run_due_bot_activities",
    )


# Background Task Session Management:
# The following asynchronous functions are periodically executed as background tasks.
# Unlike FastAPI path operations that use dependency injection (e.g., Depends(get_db)),
# these tasks require manual database session management.
# Each task obtains a session directly using SessionLocal() and ensures it's closed
# in a try/finally block to prevent connection leaks.

async def initialize_bots():
    """Initialize bot population."""
    db = SessionLocal()
    try:
        # Create services
        content_generator = ContentGenerator()
        api_client = CartoucheAPIClient()
        bot_repository = BotRepository(db)
        activity_repository = ActivityRepository(db)
        memory_service = MemoryService()

        # Create bot manager
        bot_manager = BotManager(
            bot_repository=bot_repository,
            activity_repository=activity_repository,
            content_generator=content_generator,
            api_client=api_client,
            memory_service=memory_service,
        )

        # Initialize bots
        async with api_client:
            created_count = await bot_manager.initialize_bots()
            logger.info(f"Initialized {created_count} bots")

    except Exception as e:
        logger.error(f"Failed to initialize bots: {str(e)}")
    finally:
        db.close()


async def daily_bot_growth():
    """Handle daily growth of bot population."""
    db = SessionLocal()
    try:
        # Create services
        content_generator = ContentGenerator()
        api_client = CartoucheAPIClient()
        bot_repository = BotRepository(db)
        activity_repository = ActivityRepository(db)
        memory_service = MemoryService()

        # Create bot manager
        bot_manager = BotManager(
            bot_repository=bot_repository,
            activity_repository=activity_repository,
            content_generator=content_generator,
            api_client=api_client,
            memory_service=memory_service,
        )

        # Handle daily growth
        async with api_client:
            created_count = await bot_manager.daily_growth()
            logger.info(f"Daily growth: created {created_count} bots")

    except Exception as e:
        logger.error(f"Failed to handle daily bot growth: {str(e)}")
    finally:
        db.close()


async def run_due_bot_activities():
    """Run due bot activities for all bots whose time has come."""
    db = SessionLocal()
    try:
        content_generator = ContentGenerator()
        api_client = CartoucheAPIClient()
        bot_repository = BotRepository(db)
        activity_repository = ActivityRepository(db)
        memory_service = MemoryService()

        bot_manager = BotManager(
            bot_repository=bot_repository,
            activity_repository=activity_repository,
            content_generator=content_generator,
            api_client=api_client,
            memory_service=memory_service,
        )

        async with api_client:
            await bot_manager.run_due_bot_activities()
            logger.info("Ran due bot activities for all bots")
    except Exception as e:
        logger.error(f"Failed to run due bot activities: {str(e)}")
    finally:
        db.close()


async def sync_bots_with_external_api_task():
    """
    Background task for syncing bots with external API.
    """
    db = SessionLocal()
    try:
        content_generator = ContentGenerator()
        api_client = CartoucheAPIClient()
        bot_repository = BotRepository(db)
        activity_repository = ActivityRepository(db)
        memory_service = MemoryService()

        bot_manager = BotManager(
            bot_repository=bot_repository,
            activity_repository=activity_repository,
            content_generator=content_generator,
            api_client=api_client,
            memory_service=memory_service,
        )

        async with api_client:
            synced = await bot_manager.sync_bots_with_external_api()
            logger.info(f"Synchronized {synced} bots with external API")
    except Exception as e:
        logger.error(f"Failed to sync bots with external API: {str(e)}")
    finally:
        db.close()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Cartouche Bot Service"}
