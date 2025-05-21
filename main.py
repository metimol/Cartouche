from fastapi import FastAPI
from routes import bots, posts
from storage.memory import bots_db
import asyncio
from workers.bot_worker import BotWorker

app = FastAPI(title="Cartouche Bot Engine")

bot_worker = BotWorker()

@app.on_event("startup")
async def start_bot_workers():
    # Start background bot life for all bots in DB
    bot_ids = list(bots_db.keys())
    if bot_ids:
        asyncio.create_task(bot_worker.start(bot_ids))

app.include_router(bots.router)
app.include_router(posts.router)
