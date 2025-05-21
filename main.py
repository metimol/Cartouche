from fastapi import FastAPI
from routes import bots, posts
from storage.memory import bots_db
import asyncio
from workers.bot_worker import BotWorker
from contextlib import asynccontextmanager

bot_worker = BotWorker()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background bot life for all bots in DB
    bot_ids = list(bots_db.keys())
    if bot_ids:
        asyncio.create_task(bot_worker.start(bot_ids))
    yield

app = FastAPI(title="Cartouche Bot Engine", lifespan=lifespan)

app.include_router(bots.router)
app.include_router(posts.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
