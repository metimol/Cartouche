# Bot memory and profile management

import aiosqlite
from langchain.memory import ConversationBufferMemory
from services.gemini_llm import GeminiLLM

class BotMemoryService:
    def __init__(self, db_path="bot_memory.db", google_api_key=None):
        self.db_path = db_path
        self.llm = GeminiLLM(google_api_key=google_api_key)
        self.memories = {}

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS bot_memory (
                bot_id INTEGER PRIMARY KEY,
                memory TEXT
            )''')
            await db.commit()

    async def get_memory(self, bot_id: int):
        if bot_id in self.memories:
            return self.memories[bot_id]
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT memory FROM bot_memory WHERE bot_id=?", (bot_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    memory = ConversationBufferMemory()
                    memory.buffer = row[0]
                    self.memories[bot_id] = memory
                    return memory
        memory = ConversationBufferMemory()
        self.memories[bot_id] = memory
        return memory

    async def save_memory(self, bot_id: int, memory):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("REPLACE INTO bot_memory (bot_id, memory) VALUES (?, ?)", (bot_id, memory.buffer))
            await db.commit()

    async def add_message(self, bot_id: int, message: str):
        memory = await self.get_memory(bot_id)
        memory.save_context({"input": message}, {"output": ""})
        await self.save_memory(bot_id, memory)

    async def generate_response(self, bot_id: int, prompt: str):
        memory = await self.get_memory(bot_id)
        response = self.llm(prompt + "\n" + memory.buffer)
        await self.add_message(bot_id, response)
        return response
