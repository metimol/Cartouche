"""
Models for the Cartouche Bot Service.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class Bot(BaseModel):
    """Bot model."""
    
    id: int
    name: str
    full_name: str
    avatar: Optional[str] = None
    age: int
    gender: str
    category: List[str]
    description: str
    created_at: datetime
    last_active: Optional[datetime] = None
    following: List[int] = Field(default_factory=list)
    followers_count: int = 0
    posts_count: int = 0
    likes_given: int = 0
    comments_given: int = 0
    reposts_given: int = 0
    like_probability: float = 0.5
    comment_probability: float = 0.2
    post_probability: float = 0.1
    follow_probability: float = 0.3
    unfollow_probability: float = 0.1
    repost_probability: float = 0.05


class BotCreationRequest(BaseModel):
    """Request model for bot creation."""
    
    name: Optional[str] = None
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    category: Optional[List[str]] = None
    description: Optional[str] = None


class Post(BaseModel):
    """Post model."""
    
    id: int
    user_id: Optional[str] = None
    bot_id: Optional[int] = None
    content: str
    image_url: Optional[str] = None
    timestamp: datetime
    language: Optional[str] = "en"


class Reaction(BaseModel):
    """Reaction model."""
    
    bot_id: int
    post_id: int
    reaction_type: str  # "like", "comment", "repost"
    content: Optional[str] = None  # For comments
    timestamp: datetime


class Subscription(BaseModel):
    """Subscription model."""
    
    bot_id: int
    target_id: str  # Can be user_id or bot_id
    action: str  # "follow" or "unfollow"
    timestamp: datetime


class PostProcessingRequest(BaseModel):
    """Request model for post processing."""
    
    post: Post


class FeedRequest(BaseModel):
    """Request model for feed generation."""
    
    user_id: Optional[str] = None
    limit: int = 20
    language: str = "en"


class APIResponse(BaseModel):
    """Generic API response model."""
    
    status: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
