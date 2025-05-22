"""
Main FastAPI application for the Cartouche Bot Service.
"""
import logging
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import asyncio

from app.core.logging import setup_logging
from app.core.exceptions import setup_exception_handlers
from app.db.session import get_db, engine, Base
from app.db.models import Bot, BotMemory, BotActivity, LLMConfig, SystemConfig
from app.services.scheduler import Scheduler
from app.api.routes import admin, bots, monitoring

# Setup logging
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title="Cartouche Bot Service",
    description="API for managing autonomous AI bots in the Cartouche social network simulator",
    version="1.0.0"
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup exception handlers
setup_exception_handlers(app)

# Create scheduler instance
scheduler = Scheduler()

# Include routers
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(bots.router, prefix="/api/bots", tags=["bots"])
app.include_router(monitoring.router, prefix="/api/monitoring", tags=["monitoring"])

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
    """Initialize background tasks."""
    # Schedule bot initialization
    scheduler.schedule_task(
        initialize_bots,
        delay=5,  # Start after 5 seconds
        interval=None,  # Run once
        task_id="initialize_bots"
    )
    
    # Schedule daily bot growth
    scheduler.schedule_task(
        daily_bot_growth,
        delay=3600,  # Start after 1 hour
        interval=86400,  # Run daily
        task_id="daily_bot_growth"
    )
    
    # Schedule reaction processing
    scheduler.schedule_task(
        process_reactions,
        delay=30,  # Start after 30 seconds
        interval=60,  # Run every minute
        task_id="process_reactions"
    )
    
    # Schedule bot activity
    scheduler.schedule_task(
        schedule_bot_activities,
        delay=300,  # Start after 5 minutes
        interval=3600,  # Run hourly
        task_id="schedule_bot_activities"
    )

async def initialize_bots():
    """Initialize bot population."""
    from app.services.bot_manager import BotManager
    from app.services.content_generator import ContentGenerator
    from app.clients.cartouche_api import CartoucheAPIClient
    from app.db.repositories.bot_repository import BotRepository
    from app.db.repositories.memory_repository import MemoryRepository
    from app.db.repositories.activity_repository import ActivityRepository
    
    try:
        # Get database session
        db = next(get_db())
        
        # Create services
        content_generator = ContentGenerator()
        api_client = CartoucheAPIClient()
        bot_repository = BotRepository(db)
        memory_repository = MemoryRepository(db)
        activity_repository = ActivityRepository(db)
        
        # Create bot manager
        bot_manager = BotManager(
            bot_repository=bot_repository,
            memory_repository=memory_repository,
            activity_repository=activity_repository,
            content_generator=content_generator,
            api_client=api_client
        )
        
        # Initialize bots
        async with api_client:
            created_count = await bot_manager.initialize_bots()
            logger.info(f"Initialized {created_count} bots")
    
    except Exception as e:
        logger.error(f"Failed to initialize bots: {str(e)}")

async def daily_bot_growth():
    """Handle daily growth of bot population."""
    from app.services.bot_manager import BotManager
    from app.services.content_generator import ContentGenerator
    from app.clients.cartouche_api import CartoucheAPIClient
    from app.db.repositories.bot_repository import BotRepository
    from app.db.repositories.memory_repository import MemoryRepository
    from app.db.repositories.activity_repository import ActivityRepository
    
    try:
        # Get database session
        db = next(get_db())
        
        # Create services
        content_generator = ContentGenerator()
        api_client = CartoucheAPIClient()
        bot_repository = BotRepository(db)
        memory_repository = MemoryRepository(db)
        activity_repository = ActivityRepository(db)
        
        # Create bot manager
        bot_manager = BotManager(
            bot_repository=bot_repository,
            memory_repository=memory_repository,
            activity_repository=activity_repository,
            content_generator=content_generator,
            api_client=api_client
        )
        
        # Handle daily growth
        async with api_client:
            created_count = await bot_manager.daily_growth()
            logger.info(f"Daily growth: created {created_count} bots")
    
    except Exception as e:
        logger.error(f"Failed to handle daily bot growth: {str(e)}")

async def process_reactions():
    """Process due reactions."""
    from app.services.reaction_engine import ReactionEngine
    from app.services.bot_manager import BotManager
    from app.services.content_generator import ContentGenerator
    from app.clients.cartouche_api import CartoucheAPIClient
    from app.db.repositories.bot_repository import BotRepository
    from app.db.repositories.memory_repository import MemoryRepository
    from app.db.repositories.activity_repository import ActivityRepository
    
    try:
        # Get database session
        db = next(get_db())
        
        # Create services
        content_generator = ContentGenerator()
        api_client = CartoucheAPIClient()
        bot_repository = BotRepository(db)
        memory_repository = MemoryRepository(db)
        activity_repository = ActivityRepository(db)
        
        # Create bot manager
        bot_manager = BotManager(
            bot_repository=bot_repository,
            memory_repository=memory_repository,
            activity_repository=activity_repository,
            content_generator=content_generator,
            api_client=api_client
        )
        
        # Create reaction engine
        reaction_engine = ReactionEngine(
            bot_repository=bot_repository,
            bot_manager=bot_manager
        )
        
        # Process reactions
        async with api_client:
            results = await reaction_engine.process_due_reactions()
            if results:
                logger.info(f"Processed {len(results)} reactions")
    
    except Exception as e:
        logger.error(f"Failed to process reactions: {str(e)}")

async def schedule_bot_activities():
    """Schedule activities for all bots."""
    from app.services.bot_manager import BotManager
    from app.services.content_generator import ContentGenerator
    from app.clients.cartouche_api import CartoucheAPIClient
    from app.db.repositories.bot_repository import BotRepository
    from app.db.repositories.memory_repository import MemoryRepository
    from app.db.repositories.activity_repository import ActivityRepository
    
    try:
        # Get database session
        db = next(get_db())
        
        # Create services
        content_generator = ContentGenerator()
        api_client = CartoucheAPIClient()
        bot_repository = BotRepository(db)
        memory_repository = MemoryRepository(db)
        activity_repository = ActivityRepository(db)
        
        # Create bot manager
        bot_manager = BotManager(
            bot_repository=bot_repository,
            memory_repository=memory_repository,
            activity_repository=activity_repository,
            content_generator=content_generator,
            api_client=api_client
        )
        
        # Schedule activities
        await bot_manager.schedule_bot_activities()
        logger.info("Scheduled bot activities")
    
    except Exception as e:
        logger.error(f"Failed to schedule bot activities: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Cartouche Bot Service"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}
