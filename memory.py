"""
Memory module for the Cartouche Autonomous Service.
Handles vector storage and retrieval for bot memory.
"""
import logging
import os
from typing import Dict, List, Any, Optional
import numpy as np
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

from config import VECTOR_DB_PATH

logger = logging.getLogger(__name__)

class Memory:
    """Vector memory for bots."""
    
    def __init__(self, vector_db_path: str = VECTOR_DB_PATH):
        """
        Initialize the memory module.
        
        Args:
            vector_db_path: Path to the vector database
        """
        self.vector_db_path = vector_db_path
        self.embeddings = None
        self.vector_store = None
        self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """Initialize embeddings model."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(self.vector_db_path, exist_ok=True)
            
            # Initialize embeddings model
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            
            logger.info("Embeddings model initialized successfully")
        
        except Exception as e:
            logger.error(f"Error initializing embeddings model: {str(e)}")
            self.embeddings = None
    
    async def store_memory(self, bot_id: int, memory_text: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Store a memory for a bot.
        
        Args:
            bot_id: Bot ID
            memory_text: Memory text
            metadata: Optional metadata
            
        Returns:
            Boolean indicating success
        """
        try:
            if not self.embeddings:
                logger.error("Embeddings model not initialized")
                return False
            
            # Create metadata if not provided
            if metadata is None:
                metadata = {}
            
            # Add bot_id to metadata
            metadata["bot_id"] = bot_id
            
            # Create document
            doc = Document(page_content=memory_text, metadata=metadata)
            
            # Get vector store for this bot
            vector_store = self._get_vector_store(bot_id)
            
            # Add document to vector store
            vector_store.add_documents([doc])
            
            # Save vector store
            self._save_vector_store(bot_id, vector_store)
            
            return True
        
        except Exception as e:
            logger.error(f"Error storing memory: {str(e)}")
            return False
    
    async def retrieve_memories(self, bot_id: int, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve memories for a bot based on a query.
        
        Args:
            bot_id: Bot ID
            query: Query text
            k: Number of results to return
            
        Returns:
            List of memory dictionaries
        """
        try:
            if not self.embeddings:
                logger.error("Embeddings model not initialized")
                return []
            
            # Get vector store for this bot
            vector_store = self._get_vector_store(bot_id)
            
            # If vector store is empty, return empty list
            if not vector_store:
                return []
            
            # Search for similar documents
            docs = vector_store.similarity_search(query, k=k)
            
            # Convert documents to dictionaries
            memories = []
            for doc in docs:
                memories.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata
                })
            
            return memories
        
        except Exception as e:
            logger.error(f"Error retrieving memories: {str(e)}")
            return []
    
    def _get_vector_store(self, bot_id: int) -> Optional[FAISS]:
        """
        Get vector store for a bot.
        
        Args:
            bot_id: Bot ID
            
        Returns:
            FAISS vector store or None if not found
        """
        try:
            # Check if vector store exists
            bot_vector_path = os.path.join(self.vector_db_path, f"bot_{bot_id}")
            
            if os.path.exists(bot_vector_path):
                # Load existing vector store
                return FAISS.load_local(bot_vector_path, self.embeddings)
            else:
                # Create new vector store
                return FAISS.from_documents([], self.embeddings)
        
        except Exception as e:
            logger.error(f"Error getting vector store: {str(e)}")
            return None
    
    def _save_vector_store(self, bot_id: int, vector_store: FAISS) -> bool:
        """
        Save vector store for a bot.
        
        Args:
            bot_id: Bot ID
            vector_store: FAISS vector store
            
        Returns:
            Boolean indicating success
        """
        try:
            # Create directory if it doesn't exist
            bot_vector_path = os.path.join(self.vector_db_path, f"bot_{bot_id}")
            os.makedirs(os.path.dirname(bot_vector_path), exist_ok=True)
            
            # Save vector store
            vector_store.save_local(bot_vector_path)
            
            return True
        
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            return False
