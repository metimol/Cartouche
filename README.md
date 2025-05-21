# Cartouche

**Cartouche** — an open-source social network simulator with one real account and thousands of autonomous AI bots. Each bot has its own memory, personality, behavior, and reacts to your posts like a real audience: likes, comments, ignores, argues, supports, hates, etc.

> The project is actively being developed. Part of it will be in Python, and part in C#.

---

## Key Features

- One real user, all others are AI bots
- Each bot: unique nickname, avatar, bio, age, gender, categories, memory, personality
- Bot categories: fans, haters, silent, random, neutral, humorous, provocative, role-players
- Realistic dynamics: delays, reaction waves, bots appearing/disappearing, following/unfollowing
- Memory and personality: bots remember history, can change attitude towards the user, react to topic changes
- Avatar and description generation via external/local AI services (can be cached offline)
- The entire system can work fully locally, all data stays on the user's device

---

## Technologies

- Python 3.10+, FastAPI, LangChain, OpenAI/Gemini/LLama.cpp, SQLite (or PostgreSQL/Redis), asyncio
- All bot logic, memory, and generation — in the Python service
- C# backend — only for data storage and command proxying
- Can be run via Docker Compose

---

## How It Works

1. The C# backend calls the Python service via REST API (JSON)
2. The Python service creates/updates bots, generates reactions, comments, posts
3. All bot actions are returned as ready-to-use JSON events
4. Bots live autonomously, react to posts, evolve, have memory and personality

## License

Open source, non-commercial use.

---

Backend MVP is under active development. The API is stable for basic operations. Frontend and advanced features are in progress.