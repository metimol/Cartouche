"""
Main application module for the Cartouche Autonomous Service.
Handles service initialization and orchestration.
"""
import os
import asyncio
import logging
from datetime import datetime
import signal
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from config import LOG_LEVEL, LOG_FILE, LOG_FORMAT
from database import Database
from api_client import APIClient
from bot_manager import BotManager
from content_generator import ContentGenerator
from reaction_engine import ReactionEngine
from monitor import Monitor
from memory import Memory

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class CartoucheService:
    """Main service class for the Cartouche Autonomous Service."""
    
    def __init__(self):
        """Initialize the service."""
        # Load environment variables
        load_dotenv()
        
        # Initialize components
        self.database = Database()
        self.api_client = APIClient()
        self.content_generator = ContentGenerator()
        self.memory = Memory()
        self.bot_manager = BotManager(self.database, self.api_client)
        self.reaction_engine = ReactionEngine(self.database, self.api_client, self.content_generator)
        self.monitor = Monitor(self.database, self.api_client, self.reaction_engine)
        
        # Initialize scheduler
        self.scheduler = AsyncIOScheduler()
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("Cartouche Autonomous Service initialized")
    
    async def start(self):
        """Start the service."""
        try:
            logger.info("Starting Cartouche Autonomous Service")
            
            # Initialize bots
            await self.bot_manager.initialize_bots()
            
            # Schedule bot population growth
            self.scheduler.add_job(
                self.bot_manager.grow_bot_population,
                'cron',
                hour=3,  # Run at 3 AM
                id='grow_bot_population'
            )
            
            # Schedule subscription processing
            self.scheduler.add_job(
                self.bot_manager.process_subscriptions,
                'interval',
                hours=4,
                id='process_subscriptions'
            )
            
            # Start scheduler
            self.scheduler.start()
            logger.info("Scheduler started")
            
            # Start monitor
            await self.monitor.start()
            
            logger.info("Cartouche Autonomous Service started")
        
        except Exception as e:
            logger.error(f"Error starting service: {str(e)}")
    
    async def stop(self):
        """Stop the service."""
        try:
            logger.info("Stopping Cartouche Autonomous Service")
            
            # Stop monitor
            await self.monitor.stop()
            
            # Shutdown scheduler
            self.scheduler.shutdown()
            
            logger.info("Cartouche Autonomous Service stopped")
        
        except Exception as e:
            logger.error(f"Error stopping service: {str(e)}")
    
    def _signal_handler(self, sig, frame):
        """Handle signals for graceful shutdown."""
        logger.info(f"Received signal {sig}, shutting down...")
        asyncio.create_task(self.stop())

async def main():
    """Main entry point for the service."""
    service = CartoucheService()
    
    try:
        await service.start()
        
        # Keep the service running
        while True:
            await asyncio.sleep(60)
    
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down...")
    
    finally:
        await service.stop()

if __name__ == "__main__":
    asyncio.run(main())
