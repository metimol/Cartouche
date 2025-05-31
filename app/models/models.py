"""
Pydantic models for the Cartouche Bot Service.
Defines data validation and serialization schemas.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator


# Bot Models
class BotBase(BaseModel):
    """Base model for bot data."""

    name: str
    full_name: str
    avatar: str
    age: int
    gender: str
    prompt: str
    category: str
    description: Optional[str] = None


class BotCreate(BotBase):
    """Model for creating a new bot."""

    pass


class BotUpdate(BaseModel):
    """Model for updating an existing bot."""

    full_name: Optional[str] = None
    avatar: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    prompt: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    like_probability: Optional[float] = None
    comment_probability: Optional[float] = None
    follow_probability: Optional[float] = None
    unfollow_probability: Optional[float] = None
    post_probability: Optional[float] = None


class BotResponse(BotBase):
    """Model for bot responses."""

    id: int
    created_at: datetime
    last_active: datetime
    like_probability: float
    comment_probability: float
    follow_probability: float
    unfollow_probability: float
    post_probability: float

    class Config:
        from_attributes = True


# Memory Models
class MemoryBase(BaseModel):
    """Base model for bot memory entries."""

    content: str
    context_type: str
    context_id: str


class MemoryCreate(MemoryBase):
    """Model for creating a new memory entry."""

    bot_id: int


class MemoryResponse(MemoryBase):
    """Model for memory responses."""

    bot_id: int

    class Config:
        from_attributes = True


# Activity Models
class ActivityBase(BaseModel):
    """Base model for bot activity records."""

    activity_type: str
    target_id: str
    content: Optional[str] = None


class ActivityCreate(ActivityBase):
    """Model for creating a new activity record."""

    bot_id: int


class ActivityResponse(ActivityBase):
    """Model for activity responses."""

    id: int
    bot_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Post Models (for interacting with C# API)
class Comment(BaseModel):
    """Model for post comments."""

    Name: str
    FullName: str
    Avatar: str
    Text: str
    OnDate: str = ""
    LikeComment: str = "LikeComment"
    Reply: str = "Reply"


class Post(BaseModel):
    """Model for posts."""

    Name: str
    FullName: str
    Avatar: str
    Text: str
    OnDate: str
    NewComment: str = "New Comment"
    Follow: str = "Follow"
    Unfollow: str = "Unfollow"
    LikePost: str = "LikePost"
    Comments: Optional[List[Comment]] = None
    Likes: Optional[List[str]] = None


# LLM Configuration Models
class LLMConfigBase(BaseModel):
    """Base model for LLM configuration."""

    provider: str
    api_key: str
    base_url: Optional[str] = None
    models: List[str]
    is_active: bool = True


class LLMConfigCreate(LLMConfigBase):
    """Model for creating a new LLM configuration."""

    pass


class LLMConfigUpdate(BaseModel):
    """Model for updating an existing LLM configuration."""

    api_key: Optional[str] = None
    base_url: Optional[str] = None
    models: Optional[List[str]] = None
    is_active: Optional[bool] = None


class LLMConfigResponse(LLMConfigBase):
    """Model for LLM configuration responses."""

    id: int
    updated_at: datetime

    class Config:
        from_attributes = True


# System Configuration Models
class SystemConfigBase(BaseModel):
    """Base model for system configuration."""

    key: str
    value: str
    description: Optional[str] = None


class SystemConfigCreate(SystemConfigBase):
    """Model for creating a new system configuration."""

    pass


class SystemConfigUpdate(BaseModel):
    """Model for updating an existing system configuration."""

    value: str
    description: Optional[str] = None


class SystemConfigResponse(SystemConfigBase):
    """Model for system configuration responses."""

    id: int
    updated_at: datetime

    class Config:
        from_attributes = True
