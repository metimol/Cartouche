from fastapi import APIRouter, HTTPException
from models.bot import BotProfile
from models.post import Reaction, Comment, Post
from storage.memory import bots_db, posts_db
from typing import List
import random
from utils.random_utils import random_name, random_category, random_gender

router = APIRouter(prefix="/bots", tags=["bots"])

@router.post("/new", response_model=BotProfile)
def create_bot(bot: BotProfile = None):
    """
    Create a new bot with random profile if not provided.
    """
    bot_id = len(bots_db) + 1
    if bot is None or not bot.name:
        # Generate random bot profile
        name = random_name()
        bot = BotProfile(
            id=bot_id,
            name=name,
            full_name=name + " Bot",
            avatar="default.jpg",
            age=random.randint(16, 60),
            gender=random_gender(),
            is_bot=True,
            prompt=f"{name}, {random.randint(16, 60)} years old, {random_category()}",
            following=[],
            description=f"This is a {random_category()} bot.",
            category=[random_category()],
            memory={}
        )
    else:
        bot.id = bot_id
    bots_db[bot_id] = bot
    return bot

@router.get("/", response_model=List[BotProfile])
def get_bots():
    """
    Get all bots (for debugging and admin purposes).
    """
    return list(bots_db.values())

@router.post("/{bot_id}/react")
def bot_react(bot_id: int, reaction: Reaction):
    if bot_id not in bots_db:
        raise HTTPException(status_code=404, detail="Bot not found")
    return {"status": "ok", "bot_id": bot_id, "reaction": reaction}

@router.post("/{bot_id}/comment")
def bot_comment(bot_id: int, comment: Comment):
    if bot_id not in bots_db:
        raise HTTPException(status_code=404, detail="Bot not found")
    return {"status": "ok", "bot_id": bot_id, "comment": comment}

@router.post("/{bot_id}/post")
def bot_post(bot_id: int, post: Post):
    if bot_id not in bots_db:
        raise HTTPException(status_code=404, detail="Bot not found")
    post_id = len(posts_db) + 1
    post.id = post_id
    posts_db[post_id] = post
    return post

@router.post("/{bot_id}/auto_react")
def bot_auto_react(bot_id: int, post: Post):
    if bot_id not in bots_db:
        raise HTTPException(status_code=404, detail="Bot not found")
    bot = bots_db[bot_id]
    # Simple random reaction logic for MVP
    reaction_type = random.choices(
        ["like", "dislike", "ignore", "repost"],
        weights=[0.5, 0.1, 0.3, 0.1],
        k=1
    )[0]
    comment_text = None
    if reaction_type == "like":
        # Add bot to post likes
        if bot.name not in post.likes:
            post.likes.append(bot.name)
    elif reaction_type == "dislike":
        # No explicit dislike in post, just return
        pass
    elif reaction_type == "repost":
        # For MVP, just mark as reposted
        pass
    # 20% chance to comment
    if random.random() < 0.2:
        comment_text = f"{bot.name} says: Nice post!"
        post.comments.append({
            "Name": bot.name,
            "FullName": bot.full_name,
            "Avatar": bot.avatar,
            "Text": comment_text,
            "OnDate": post.on_date,
            "Likes": []
        })
    return {
        "status": "ok",
        "bot_id": bot_id,
        "reaction": reaction_type,
        "comment": comment_text
    }
