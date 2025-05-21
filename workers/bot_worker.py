# Background worker for running bots
import asyncio
from services.memory_service import BotMemoryService
from services.llm_service import LLMService
from services.bot_engine import BotEngine

class BotWorker:
    def __init__(self):
        self.memory_service = BotMemoryService()
        self.llm_service = LLMService()
        self.engine = BotEngine(self.memory_service, self.llm_service)

    async def start(self, bot_ids):
        await self.memory_service.init_db()
        tasks = [self.engine.bot_life(bot_id) for bot_id in bot_ids]
        await asyncio.gather(*tasks)
