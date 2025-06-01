"""
Memory service for the Cartouche Bot Service.
Handles vector storage and retrieval of bot memories.
"""

from typing import Dict, List, Any
import os
from pathlib import Path
import asyncio

from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

from app.core.settings import VECTOR_DB_PATH
from app.core.exceptions import DatabaseError

from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()


class MemoryService:
    """Service for managing bot memory using vector storage."""

    def __init__(self, vector_db_path: str = VECTOR_DB_PATH):
        """
        Initialize the memory service.

        Args:
            vector_db_path: Path to vector database
        """
        self.vector_db_path = vector_db_path
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # Ensure vector store directory exists
        Path(vector_db_path).mkdir(parents=True, exist_ok=True)

        # Initialize vector stores for each bot as needed
        self.vector_stores = {}
        self.qdrant_clients = {}  # Cache QdrantClient per bot
        self._bot_locks: Dict[int, asyncio.Lock] = {}  # Lock per bot for queueing

    def _get_bot_vector_store(self, bot_id: int) -> QdrantVectorStore:
        """
        Get or create vector store for a specific bot.

        Args:
            bot_id: Bot ID

        Returns:
            Vector store instance
        """
        if bot_id not in self.vector_stores:
            try:
                collection_path = os.path.join(self.vector_db_path, f"bot_{bot_id}")
                Path(collection_path).mkdir(parents=True, exist_ok=True)

                # Use cached QdrantClient if available
                if bot_id not in self.qdrant_clients:
                    self.qdrant_clients[bot_id] = QdrantClient(path=collection_path)
                client = self.qdrant_clients[bot_id]

                collection_name = f"bot_{bot_id}"
                if collection_name not in [
                    c.name for c in client.get_collections().collections
                ]:
                    client.create_collection(
                        collection_name=collection_name,
                        vectors_config={
                            "size": len(self.embeddings.embed_query("test")),
                            "distance": "Cosine",
                        },
                    )

                # Create or load vector store
                self.vector_stores[bot_id] = QdrantVectorStore(
                    client=client,
                    embedding=self.embeddings,
                    collection_name=collection_name,
                )
            except Exception as e:
                logger.error(
                    f"Failed to create vector store for bot {bot_id}: {str(e)}"
                )
                raise DatabaseError(f"Failed to create vector store: {str(e)}")

        return self.vector_stores[bot_id]

    def _get_bot_lock(self, bot_id: int) -> asyncio.Lock:
        if bot_id not in self._bot_locks:
            self._bot_locks[bot_id] = asyncio.Lock()
        return self._bot_locks[bot_id]

    async def add_memory(self, bot_id: int, text: str, metadata: Dict[str, Any]) -> str:
        lock = self._get_bot_lock(bot_id)
        async with lock:
            try:
                vector_store = self._get_bot_vector_store(bot_id)

                # Add document to vector store
                ids = vector_store.add_texts(texts=[text], metadatas=[metadata])

                return ids[0]
            except Exception as e:
                logger.error(f"Failed to add memory for bot {bot_id}: {str(e)}")
                raise DatabaseError(f"Failed to add memory: {str(e)}")

    async def search_memories(
        self, bot_id: int, query: str, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search memories by similarity.

        Args:
            bot_id: Bot ID
            query: Search query
            limit: Maximum number of results

        Returns:
            List of memory documents

        Raises:
            DatabaseError: If search fails
        """
        lock = self._get_bot_lock(bot_id)
        async with lock:
            try:
                vector_store = self._get_bot_vector_store(bot_id)

                # Search vector store
                results = vector_store.similarity_search_with_score(query=query, k=limit)

                # Format results
                memories = []
                for doc, score in results:
                    memories.append(
                        {
                            "text": doc.page_content,
                            "metadata": doc.metadata,
                            "relevance": float(score),
                        }
                    )

                return memories
            except Exception as e:
                logger.error(f"Failed to search memories for bot {bot_id}: {str(e)}")
                raise DatabaseError(f"Failed to search memories: {str(e)}")

    async def delete_bot_memories(self, bot_id: int) -> bool:
        """
        Delete all memories for a specific bot.

        Args:
            bot_id: Bot ID

        Returns:
            True if successful

        Raises:
            DatabaseError: If deletion fails
        """
        lock = self._get_bot_lock(bot_id)
        async with lock:
            try:
                # Remove from cache
                if bot_id in self.vector_stores:
                    del self.vector_stores[bot_id]
                if bot_id in self.qdrant_clients:
                    del self.qdrant_clients[bot_id]

                # Delete collection directory
                collection_path = os.path.join(self.vector_db_path, f"bot_{bot_id}")
                if os.path.exists(collection_path):
                    import shutil

                    shutil.rmtree(collection_path)

                return True
            except Exception as e:
                logger.error(f"Failed to delete memories for bot {bot_id}: {str(e)}")
                raise DatabaseError(f"Failed to delete memories: {str(e)}")
