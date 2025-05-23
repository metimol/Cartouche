"""
SQLAlchemy models for the Cartouche Bot Service.
Defines database tables and relationships.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class Bot(Base):
    """Bot model representing an AI user in the system."""

    __tablename__ = "bots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    full_name = Column(String)
    avatar = Column(String)
    age = Column(Integer)
    gender = Column(String)
    prompt = Column(Text)
    category = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)

    # Probabilities for different actions
    like_probability = Column(Float)
    comment_probability = Column(Float)
    follow_probability = Column(Float)
    unfollow_probability = Column(Float)
    repost_probability = Column(Float)

    # Relationships
    memories = relationship(
        "BotMemory", back_populates="bot", cascade="all, delete-orphan"
    )
    activities = relationship(
        "BotActivity", back_populates="bot", cascade="all, delete-orphan"
    )

    def to_dict(self):
        """Convert bot to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "avatar": self.avatar,
            "age": self.age,
            "gender": self.gender,
            "category": self.category,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
            "like_probability": self.like_probability,
            "comment_probability": self.comment_probability,
            "follow_probability": self.follow_probability,
            "unfollow_probability": self.unfollow_probability,
            "repost_probability": self.repost_probability,
        }


class BotMemory(Base):
    """Memory entries for bots to remember past interactions."""

    __tablename__ = "bot_memories"

    id = Column(Integer, primary_key=True, index=True)
    bot_id = Column(Integer, ForeignKey("bots.id"))
    content = Column(Text)
    context_type = Column(String)  # post, comment, user, etc.
    context_id = Column(String)  # ID of the related entity
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    bot = relationship("Bot", back_populates="memories")


class BotActivity(Base):
    """Record of bot activities for tracking and preventing duplicates."""

    __tablename__ = "bot_activities"

    id = Column(Integer, primary_key=True, index=True)
    bot_id = Column(Integer, ForeignKey("bots.id"))
    activity_type = Column(String)  # like, comment, follow, unfollow, post
    target_id = Column(String)  # ID of the target (post ID, user ID)
    content = Column(Text, nullable=True)  # For comments
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    bot = relationship("Bot", back_populates="activities")


class LLMConfig(Base):
    """Configuration for LLM providers."""

    __tablename__ = "llm_configs"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, unique=True)
    api_key = Column(String)
    base_url = Column(String, nullable=True)
    models = Column(JSON)  # List of available models
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SystemConfig(Base):
    """System-wide configuration settings."""

    __tablename__ = "system_configs"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True)
    value = Column(String)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
