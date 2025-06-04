import unittest
from unittest.mock import patch, MagicMock

from app.services.memory_service import MemoryService
from app.core.exceptions import DatabaseError
# We'll need a way to represent qdrant's collection list
from qdrant_client.http.models import CollectionsResponse, CollectionDescription

class TestMemoryService(unittest.TestCase):

    def setUp(self):
        # Patch QDRANT_HOST and QDRANT_PORT as they are used in __init__ before client mock
        self.qdrant_host_patcher = patch('app.services.memory_service.QDRANT_HOST', 'mock_host')
        self.qdrant_port_patcher = patch('app.services.memory_service.QDRANT_PORT', 1234)
        self.mock_qdrant_host = self.qdrant_host_patcher.start()
        self.mock_qdrant_port = self.qdrant_port_patcher.start()

        self.memory_service = MemoryService()

    def tearDown(self):
        self.qdrant_host_patcher.stop()
        self.qdrant_port_patcher.stop()

    @patch('app.services.memory_service.QdrantClient')
    def test_get_all_bot_collection_names_no_collections(self, MockQdrantClient):
        mock_qdrant_instance = MockQdrantClient.return_value
        mock_qdrant_instance.get_collections.return_value = CollectionsResponse(collections=[])

        # Replace the client instance in memory_service with the mocked one
        self.memory_service.qdrant_client = mock_qdrant_instance

        result = self.memory_service.get_all_bot_collection_names()
        self.assertEqual(result, [])

    @patch('app.services.memory_service.QdrantClient')
    def test_get_all_bot_collection_names_valid_names(self, MockQdrantClient):
        mock_qdrant_instance = MockQdrantClient.return_value
        mock_collections = [
            CollectionDescription(name="bot_1"),
            CollectionDescription(name="bot_23"),
            CollectionDescription(name="bot_456"),
        ]
        mock_qdrant_instance.get_collections.return_value = CollectionsResponse(collections=mock_collections)
        self.memory_service.qdrant_client = mock_qdrant_instance

        result = self.memory_service.get_all_bot_collection_names()
        self.assertEqual(sorted(result), sorted([1, 23, 456]))

    @patch('app.services.memory_service.QdrantClient')
    def test_get_all_bot_collection_names_invalid_names(self, MockQdrantClient):
        mock_qdrant_instance = MockQdrantClient.return_value
        mock_collections = [
            CollectionDescription(name="user_1"),
            CollectionDescription(name="bot_abc"),
            CollectionDescription(name="random_collection"),
            CollectionDescription(name="bot_"), # Edge case
            CollectionDescription(name="bot_1x"), # Invalid int
        ]
        mock_qdrant_instance.get_collections.return_value = CollectionsResponse(collections=mock_collections)
        self.memory_service.qdrant_client = mock_qdrant_instance

        result = self.memory_service.get_all_bot_collection_names()
        self.assertEqual(result, [])

    @patch('app.services.memory_service.QdrantClient')
    def test_get_all_bot_collection_names_mixed_names(self, MockQdrantClient):
        mock_qdrant_instance = MockQdrantClient.return_value
        mock_collections = [
            CollectionDescription(name="bot_7"),
            CollectionDescription(name="user_2"),
            CollectionDescription(name="bot_88"),
            CollectionDescription(name="bot_xyz"),
            CollectionDescription(name="another_one"),
            CollectionDescription(name="bot_999"),
        ]
        mock_qdrant_instance.get_collections.return_value = CollectionsResponse(collections=mock_collections)
        self.memory_service.qdrant_client = mock_qdrant_instance

        result = self.memory_service.get_all_bot_collection_names()
        self.assertEqual(sorted(result), sorted([7, 88, 999]))

    @patch('app.services.memory_service.QdrantClient')
    def test_get_all_bot_collection_names_qdrant_api_error(self, MockQdrantClient):
        mock_qdrant_instance = MockQdrantClient.return_value
        mock_qdrant_instance.get_collections.side_effect = Exception("Qdrant connection failed")
        self.memory_service.qdrant_client = mock_qdrant_instance

        with self.assertRaises(DatabaseError) as context:
            self.memory_service.get_all_bot_collection_names()
        self.assertIn("Failed to retrieve collections: Qdrant connection failed", str(context.exception))

if __name__ == "__main__":
    unittest.main()
