"""
Memory repository for the Cartouche Bot Service.
Handles database operations for bot memories.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.models import BotMemory
from app.core.exceptions import DatabaseError

class MemoryRepository:
    """Repository for bot memory operations."""
    
    def __init__(self, db: Session):
        """
        Initialize the repository.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def get_memories_by_bot_id(self, bot_id: int, skip: int = 0, limit: int = 100) -> List[BotMemory]:
        """
        Get memories for a specific bot.
        
        Args:
            bot_id: Bot ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of memories
        """
        return self.db.query(BotMemory).filter(BotMemory.bot_id == bot_id).offset(skip).limit(limit).all()
    
    def get_memory_by_id(self, memory_id: int) -> Optional[BotMemory]:
        """
        Get a memory by ID.
        
        Args:
            memory_id: Memory ID
            
        Returns:
            Memory or None if not found
        """
        return self.db.query(BotMemory).filter(BotMemory.id == memory_id).first()
    
    def create_memory(self, memory_data: Dict[str, Any]) -> BotMemory:
        """
        Create a new memory.
        
        Args:
            memory_data: Memory data dictionary
            
        Returns:
            Created memory
            
        Raises:
            DatabaseError: If memory creation fails
        """
        try:
            memory = BotMemory(**memory_data)
            self.db.add(memory)
            self.db.commit()
            self.db.refresh(memory)
            return memory
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create memory: {str(e)}")
    
    def delete_memory(self, memory_id: int) -> bool:
        """
        Delete a memory.
        
        Args:
            memory_id: Memory ID
            
        Returns:
            True if successful
            
        Raises:
            DatabaseError: If memory deletion fails
        """
        try:
            memory = self.get_memory_by_id(memory_id)
            if not memory:
                raise DatabaseError(f"Memory with ID {memory_id} not found")
            
            self.db.delete(memory)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to delete memory: {str(e)}")
    
    def get_memories_by_context(self, bot_id: int, context_type: str, context_id: str) -> List[BotMemory]:
        """
        Get memories by context.
        
        Args:
            bot_id: Bot ID
            context_type: Context type (post, comment, user, etc.)
            context_id: Context ID
            
        Returns:
            List of memories
        """
        return self.db.query(BotMemory).filter(
            BotMemory.bot_id == bot_id,
            BotMemory.context_type == context_type,
            BotMemory.context_id == context_id
        ).all()
    
    def count_memories_by_bot(self, bot_id: int) -> int:
        """
        Count memories for a specific bot.
        
        Args:
            bot_id: Bot ID
            
        Returns:
            Memory count
        """
        return self.db.query(func.count(BotMemory.id)).filter(BotMemory.bot_id == bot_id).scalar()
    
    def delete_memories_by_bot(self, bot_id: int) -> int:
        """
        Delete all memories for a specific bot.
        
        Args:
            bot_id: Bot ID
            
        Returns:
            Number of deleted memories
            
        Raises:
            DatabaseError: If memory deletion fails
        """
        try:
            count = self.count_memories_by_bot(bot_id)
            self.db.query(BotMemory).filter(BotMemory.bot_id == bot_id).delete()
            self.db.commit()
            return count
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to delete memories: {str(e)}")
