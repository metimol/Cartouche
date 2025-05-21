from pydantic import BaseModel
from typing import List, Optional

class Post(BaseModel):
    id: Optional[int] = None
    name: str
    full_name: Optional[str] = None
    avatar: Optional[str] = None
    text: str
    on_date: str
    likes: Optional[List[str]] = []
    comments: Optional[List[dict]] = []

class Reaction(BaseModel):
    post_id: int
    reaction_type: str  # like, dislike, ignore, repost

class Comment(BaseModel):
    post_id: int
    text: str
    on_date: str
