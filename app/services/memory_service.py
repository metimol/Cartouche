"""
Memory service for the Cartouche Bot Service.
Handles vector storage and retrieval of bot memories.
"""

from typing import Dict, List, Any

from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

from app.core.settings import QDRANT_HOST, QDRANT_PORT
from app.core.exceptions import DatabaseError

from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()


class MemoryService:
    """Service for managing bot memory using Qdrant Cloud vector storage."""

    def __init__(self):
        """
        Initialize the memory service for Qdrant Cloud.
        """
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        # Single QdrantClient for all bots (cloud)
        self.qdrant_client = QdrantClient(
            url=QDRANT_HOST,
            port=QDRANT_PORT,
        )

    def _get_bot_vector_store(self, bot_id: int) -> QdrantVectorStore:
        """
        Get or create vector store for a specific bot (cloud collection).

        Args:
            bot_id: Bot ID

        Returns:
            Vector store instance
        """
        collection_name = f"bot_{bot_id}"
        try:
            collections = [
                c.name for c in self.qdrant_client.get_collections().collections
            ]
            if collection_name not in collections:
                self.qdrant_client.create_collection(
                    collection_name=collection_name,
                    vectors_config={
                        "size": len(self.embeddings.embed_query("test")),
                        "distance": "Cosine",
                    },
                )
            return QdrantVectorStore(
                client=self.qdrant_client,
                embedding=self.embeddings,
                collection_name=collection_name,
            )
        except Exception as e:
            logger.error(
                f"Failed to create/load vector store for bot {bot_id}: {str(e)}"
            )
            raise DatabaseError(f"Failed to create/load vector store: {str(e)}")

    async def add_memory(self, bot_id: int, text: str, metadata: Dict[str, Any]) -> str:
        try:
            vector_store = self._get_bot_vector_store(bot_id)
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
        try:
            vector_store = self._get_bot_vector_store(bot_id)
            try:
                results = vector_store.similarity_search_with_score(query=query, k=limit)
            except Exception as inner_e:
                # Qdrant 404: collection exists, but no points (empty collection)
                if '404' in str(inner_e) or 'Not Found' in str(inner_e):
                    return []
                raise
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
        try:
            collection_name = f"bot_{bot_id}"
            self.qdrant_client.delete_collection(collection_name=collection_name)
            return True
        except Exception as e:
            logger.error(f"Failed to delete memories for bot {bot_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete memories: {str(e)}")
