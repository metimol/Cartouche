import unittest
from unittest.mock import MagicMock, patch, AsyncMock, call # Added call for checking multiple calls
import aiohttp # For mocking client session

# Use IsolatedAsyncioTestCase for async methods
from unittest import IsolatedAsyncioTestCase

# Defer import of BotManager until patches are applied
# from app.services.bot_manager import BotManager
from app.services.memory_service import MemoryService # Used for spec
from app.db.repositories.bot_repository import BotRepository # Used for spec
from app.db.repositories.activity_repository import ActivityRepository
from app.services.content_generator import ContentGenerator
from app.clients.cartouche_api import CartoucheAPIClient

# A simple mock for bot objects
class MockBot:
    def __init__(self, id, name):
        self.id = id
        self.name = name

# Apply patches at the module level to affect imports
module_level_patches = [
    patch('app.core.settings.API_TOKEN', 'test_api_token'),
    patch('app.core.settings.QDRANT_HOST', 'test_qdrant_host'),
    patch('app.core.settings.GOOGLE_API_KEY', 'test_google_key'),
    patch('app.core.settings.DB_PATH', 'sqlite:///./test_temp_db.sqlite3'),
    patch('app.core.settings.validate_settings', MagicMock()) # Bypass validation
]

BotManager = None # Global variable to hold the imported class

def setUpModule():
    global BotManager
    for p in module_level_patches:
        p.start()
    # Now that settings are patched, we can import BotManager
    from app.services.bot_manager import BotManager as BM
    BotManager = BM

def tearDownModule():
    for p in module_level_patches:
        p.stop()

class TestBotManager(IsolatedAsyncioTestCase):

    def setUp(self):
        if BotManager is None:
            raise RuntimeError("BotManager not imported. setUpModule might have failed.")
        self.mock_bot_repository = MagicMock(spec=BotRepository)
        self.mock_activity_repository = MagicMock(spec=ActivityRepository)
        self.mock_content_generator = MagicMock(spec=ContentGenerator)
        self.mock_api_client = MagicMock(spec=CartoucheAPIClient)
        self.mock_memory_service = MagicMock(spec=MemoryService)

        # Make sure async methods in mocks are AsyncMock
        self.mock_memory_service.delete_bot_memories = AsyncMock()
        self.mock_memory_service._get_bot_vector_store = AsyncMock() # From sync_bots_with_external_api

        # Mock methods used by sync_bots_with_external_api
        self.mock_bot_repository.get_all_bots = MagicMock()
        self.mock_bot_repository.create_bot = MagicMock()
        self.mock_bot_repository.update_bot = MagicMock()
        self.mock_bot_repository.delete_bot = MagicMock()

        self.mock_memory_service.get_all_bot_collection_names = MagicMock()


        self.bot_manager = BotManager(
            bot_repository=self.mock_bot_repository,
            activity_repository=self.mock_activity_repository,
            content_generator=self.mock_content_generator,
            api_client=self.mock_api_client,
            memory_service=self.mock_memory_service
        )

    # Helper to mock aiohttp response
    def _get_mock_aiohttp_response(self, json_data, status_code):
        mock_response = MagicMock(spec=aiohttp.ClientResponse)
        mock_response.status = status_code
        mock_response.json = AsyncMock(return_value=json_data)

        mock_session_get = AsyncMock()
        mock_session_get.return_value.__aenter__.return_value = mock_response # Simulate async context manager
        mock_session_get.return_value.__aexit__.return_value = None
        return mock_session_get

    @patch('aiohttp.ClientSession.get') # Patch where it's used
    async def test_sync_orphaned_collections_exist(self, mock_get):
        # Simulate external API response (e.g., two bots)
        mock_get.side_effect = self._get_mock_aiohttp_response(
            json_data=[
                {"json": {"Name": "bot1", "IsBot": True, "Settings": {}}}, # Bot 1 from API
                {"json": {"Name": "bot2", "IsBot": True, "Settings": {}}}, # Bot 2 from API
            ],
            status_code=200
        )

        # Simulate local DB having bot1 (id=1) and bot2 (id=2) after sync from API
        # This means create_bot or update_bot would have been called for these.
        # For the purpose of testing cleanup, we care about the state of get_all_bots *after* the main sync loop.
        self.mock_bot_repository.get_all_bots.side_effect = [
            [], # Initial call before sync loop might return something, for simplicity empty.
                 # The crucial one is the call *during* the cleanup phase.
            [MockBot(id=1, name="bot1"), MockBot(id=2, name="bot2")] # Bots in DB for cleanup phase
        ]
        # Simulate bot creation/update mapping names to IDs for the test
        self.mock_bot_repository.create_bot.side_effect = lambda data: MockBot(id=1 if data['name'] == 'bot1' else 2, name=data['name'])


        # qDrant has collections for bots 1, 2, 3 (orphaned), 4 (orphaned)
        self.mock_memory_service.get_all_bot_collection_names.return_value = [1, 2, 3, 4]

        await self.bot_manager.sync_bots_with_external_api()

        # Assert delete_bot_memories was called for orphaned bots 3 and 4
        self.mock_memory_service.delete_bot_memories.assert_has_calls([
            call(3),
            call(4)
        ], any_order=True)
        self.assertEqual(self.mock_memory_service.delete_bot_memories.call_count, 2)


    @patch('aiohttp.ClientSession.get')
    async def test_sync_no_orphaned_collections(self, mock_get):
        mock_get.side_effect = self._get_mock_aiohttp_response(
            json_data=[
                {"json": {"Name": "bot1", "IsBot": True, "Settings": {}}},
            ],
            status_code=200
        )
        self.mock_bot_repository.get_all_bots.side_effect = [
            [],
            [MockBot(id=1, name="bot1")]
        ]
        self.mock_bot_repository.create_bot.return_value = MockBot(id=1, name="bot1")

        self.mock_memory_service.get_all_bot_collection_names.return_value = [1] # Only bot 1 in qdrant

        await self.bot_manager.sync_bots_with_external_api()

        self.mock_memory_service.delete_bot_memories.assert_not_called()

    @patch('aiohttp.ClientSession.get')
    async def test_sync_qdrant_returns_empty_list(self, mock_get):
        mock_get.side_effect = self._get_mock_aiohttp_response(
            json_data=[
                {"json": {"Name": "bot1", "IsBot": True, "Settings": {}}},
            ],
            status_code=200
        )
        self.mock_bot_repository.get_all_bots.side_effect = [
            [],
            [MockBot(id=1, name="bot1")]
        ]
        self.mock_bot_repository.create_bot.return_value = MockBot(id=1, name="bot1")
        self.mock_memory_service.get_all_bot_collection_names.return_value = [] # qDrant is empty

        await self.bot_manager.sync_bots_with_external_api()

        self.mock_memory_service.delete_bot_memories.assert_not_called()

    @patch('aiohttp.ClientSession.get')
    async def test_sync_local_db_no_bots_qdrant_has_collections(self, mock_get):
        # API returns no bots
        mock_get.side_effect = self._get_mock_aiohttp_response(json_data=[], status_code=200)

        # Local DB is empty after sync from API
        self.mock_bot_repository.get_all_bots.return_value = [] # Empty throughout

        # qDrant has collections for bots 1, 2
        self.mock_memory_service.get_all_bot_collection_names.return_value = [1, 2]

        await self.bot_manager.sync_bots_with_external_api()

        # Assert delete_bot_memories was called for orphaned bots 1 and 2
        self.mock_memory_service.delete_bot_memories.assert_has_calls([
            call(1),
            call(2)
        ], any_order=True)
        self.assertEqual(self.mock_memory_service.delete_bot_memories.call_count, 2)

    @patch('aiohttp.ClientSession.get')
    async def test_sync_api_call_fails(self, mock_get):
        # Simulate API failure
        mock_get.side_effect = self._get_mock_aiohttp_response(json_data={"error": "failure"}, status_code=500)

        # Even if API fails, cleanup should ideally not run or not fail if it does.
        # For this test, we assume it might not proceed to cleanup if API fails early.
        # Or, if it does, it should use the current state of DB (empty if sync failed)
        self.mock_bot_repository.get_all_bots.return_value = []
        self.mock_memory_service.get_all_bot_collection_names.return_value = [101, 102] # Some qdrant collections

        await self.bot_manager.sync_bots_with_external_api()

        # Given the current implementation, if API call fails, external_bots is empty.
        # The sync loop for adding/updating bots won't run.
        # The sync loop for deleting local bots *not* in external_bots will run.
        # Then the qdrant cleanup runs.
        # If local DB was empty and API fails, local DB remains empty.
        # So, qdrant collections 101, 102 would be deleted.
        self.mock_memory_service.delete_bot_memories.assert_has_calls([
            call(101),
            call(102)
        ], any_order=True)
        self.assertEqual(self.mock_memory_service.delete_bot_memories.call_count, 2)


if __name__ == '__main__':
    unittest.main()
