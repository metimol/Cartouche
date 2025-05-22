"""
Main application for the Cartouche Bot Service.
"""
import logging
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any

from models import (
    Post, Bot, BotCreationRequest, APIResponse, 
    PostProcessingRequest, FeedRequest
)
from api.api_interface import verify_api_key
from tasks.reaction_tasks import process_post_reactions
from tasks.bot_tasks import grow_bots, create_bot
from tasks.post_tasks import generate_bot_posts
from tasks.subscription_tasks import process_subscriptions
from bot_manager.bot_manager import BotManager
from config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=settings.LOG_FILE,
    filemode='a'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Cartouche Bot Service",
    description="API for autonomous bot service in Cartouche social network",
    version="1.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/v1/health", response_model=APIResponse)
async def health_check():
    """Check if the service is healthy."""
    return APIResponse(status="success", message="Service is healthy")

# Process post endpoint
@app.post("/api/v1/posts/process", response_model=APIResponse)
async def process_post(
    request: PostProcessingRequest,
    background_tasks: BackgroundTasks,
    authorization: Optional[str] = Header(None),
    api_key: str = Depends(verify_api_key)
):
    """
    Process a new post and generate bot reactions.
    
    This endpoint accepts a new post and starts an asynchronous task
    to generate bot reactions (likes, comments, reposts).
    """
    try:
        # Start asynchronous task
        task = process_post_reactions.delay(request.post.dict())
        
        return APIResponse(
            status="success",
            message="Post processing started",
            data={"task_id": task.id}
        )
    
    except Exception as e:
        logger.error(f"Error processing post: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Get task status endpoint
@app.get("/api/v1/tasks/{task_id}", response_model=APIResponse)
async def get_task_status(
    task_id: str,
    authorization: Optional[str] = Header(None),
    api_key: str = Depends(verify_api_key)
):
    """
    Get the status of an asynchronous task.
    
    This endpoint returns the status and result of a task.
    """
    try:
        from celery_app import app as celery_app
        task = celery_app.AsyncResult(task_id)
        
        if task.state == 'PENDING':
            response = {
                "status": "pending",
                "message": "Task is pending"
            }
        elif task.state == 'FAILURE':
            response = {
                "status": "error",
                "error": str(task.info)
            }
        else:
            response = {
                "status": task.state.lower(),
                "result": task.result
            }
        
        return APIResponse(
            status="success",
            data=response
        )
    
    except Exception as e:
        logger.error(f"Error getting task status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Get bots endpoint
@app.get("/api/v1/bots", response_model=APIResponse)
async def get_bots(
    limit: int = 100,
    offset: int = 0,
    category: Optional[str] = None,
    authorization: Optional[str] = Header(None),
    api_key: str = Depends(verify_api_key)
):
    """
    Get a list of bots.
    
    This endpoint returns a list of bots with pagination.
    """
    try:
        bot_manager = BotManager()
        
        if category:
            bots = bot_manager.get_bots_by_category(category)
        else:
            bots = bot_manager.get_all_bots()
        
        total = len(bots)
        bots = bots[offset:offset+limit]
        
        return APIResponse(
            status="success",
            data={
                "total": total,
                "bots": bots
            }
        )
    
    except Exception as e:
        logger.error(f"Error getting bots: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Get bot endpoint
@app.get("/api/v1/bots/{bot_id}", response_model=APIResponse)
async def get_bot(
    bot_id: int,
    authorization: Optional[str] = Header(None),
    api_key: str = Depends(verify_api_key)
):
    """
    Get a specific bot.
    
    This endpoint returns information about a specific bot.
    """
    try:
        bot_manager = BotManager()
        bot = bot_manager.get_bot(bot_id)
        
        if not bot:
            raise HTTPException(status_code=404, detail=f"Bot {bot_id} not found")
        
        return APIResponse(
            status="success",
            data=bot
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error getting bot {bot_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Create bot endpoint
@app.post("/api/v1/bots", response_model=APIResponse)
async def create_new_bot(
    request: BotCreationRequest,
    background_tasks: BackgroundTasks,
    authorization: Optional[str] = Header(None),
    api_key: str = Depends(verify_api_key)
):
    """
    Create a new bot.
    
    This endpoint creates a new bot with the specified characteristics.
    """
    try:
        # Start asynchronous task
        task = create_bot.delay(request.dict())
        
        return APIResponse(
            status="success",
            message="Bot creation started",
            data={"task_id": task.id}
        )
    
    except Exception as e:
        logger.error(f"Error creating bot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Initialize bots endpoint
@app.post("/api/v1/bots/initialize", response_model=APIResponse)
async def initialize_bots(
    background_tasks: BackgroundTasks,
    authorization: Optional[str] = Header(None),
    api_key: str = Depends(verify_api_key)
):
    """
    Initialize bots.
    
    This endpoint creates the initial set of bots.
    """
    try:
        bot_manager = BotManager()
        current_count = bot_manager.count_bots()
        
        if current_count > 0:
            return APIResponse(
                status="success",
                message=f"Bots already initialized ({current_count} bots exist)"
            )
        
        # Start asynchronous task
        for _ in range(settings.INITIAL_BOTS_COUNT):
            create_bot.delay()
        
        return APIResponse(
            status="success",
            message=f"Bot initialization started ({settings.INITIAL_BOTS_COUNT} bots)"
        )
    
    except Exception as e:
        logger.error(f"Error initializing bots: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Generate feed endpoint
@app.get("/api/v1/feed", response_model=APIResponse)
async def generate_feed(
    limit: int = 20,
    user_id: Optional[str] = None,
    language: str = "en",
    authorization: Optional[str] = Header(None),
    api_key: str = Depends(verify_api_key)
):
    """
    Generate a feed with bot posts.
    
    This endpoint generates a feed with posts from bots.
    """
    try:
        # Start asynchronous task
        task = generate_bot_posts.delay(limit, user_id, language)
        
        return APIResponse(
            status="success",
            message="Feed generation started",
            data={"task_id": task.id}
        )
    
    except Exception as e:
        logger.error(f"Error generating feed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Process subscriptions endpoint
@app.post("/api/v1/subscriptions/process", response_model=APIResponse)
async def process_bot_subscriptions(
    background_tasks: BackgroundTasks,
    authorization: Optional[str] = Header(None),
    api_key: str = Depends(verify_api_key)
):
    """
    Process bot subscriptions.
    
    This endpoint starts an asynchronous task to process bot subscriptions.
    """
    try:
        # Start asynchronous task
        task = process_subscriptions.delay()
        
        return APIResponse(
            status="success",
            message="Subscription processing started",
            data={"task_id": task.id}
        )
    
    except Exception as e:
        logger.error(f"Error processing subscriptions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Grow bots endpoint
@app.post("/api/v1/bots/grow", response_model=APIResponse)
async def grow_bot_population(
    background_tasks: BackgroundTasks,
    authorization: Optional[str] = Header(None),
    api_key: str = Depends(verify_api_key)
):
    """
    Grow the bot population.
    
    This endpoint starts an asynchronous task to grow the bot population.
    """
    try:
        # Start asynchronous task
        task = grow_bots.delay()
        
        return APIResponse(
            status="success",
            message="Bot growth started",
            data={"task_id": task.id}
        )
    
    except Exception as e:
        logger.error(f"Error growing bots: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
