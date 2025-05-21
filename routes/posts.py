from fastapi import APIRouter
from models.post import Post
from storage.memory import posts_db
from typing import List

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/new", response_model=Post)
def create_post(post: Post):
    post_id = len(posts_db) + 1
    post.id = post_id
    posts_db[post_id] = post
    return post

@router.get("/", response_model=List[Post])
def get_posts():
    return list(posts_db.values())

@router.get("/unread", response_model=List[Post])
def get_unread_posts():
    return list(posts_db.values())
