"""
Tests for the Cartouche Bot Service v2.
"""
import pytest
import random
from unittest.mock import MagicMock, patch
from datetime import datetime

from models import Bot, Post, Reaction
from bot_manager.bot_manager import BotManager
from content_generator.llm_service import LLMService
from memory_service.memory_service import MemoryService
from utils.language_service import LanguageService
from tasks.reaction_tasks import (
    process_post_reactions,
    _should_like_post,
    _should_comment_on_post,
    _should_repost_post
)
from tasks.bot_tasks import (
    grow_bots,
    create_bot,
    _generate_bot_name,
    _generate_avatar_url,
    _calculate_behavior_probabilities
)


@pytest.fixture
def bot_manager():
    """Fixture for bot manager with test bots."""
    manager = BotManager()
    
    # Mock methods
    manager.get_all_bots = MagicMock(return_value=[
        {
            "id": 1,
            "name": "TestBot1",
            "full_name": "Test Bot One",
            "age": 25,
            "gender": "Male",
            "category": ["fan"],
            "description": "Test bot for fans",
            "created_at": datetime.now(),
            "like_probability": 0.8,
            "comment_probability": 0.5,
            "post_probability": 0.3,
            "follow_probability": 0.4,
            "unfollow_probability": 0.1,
            "repost_probability": 0.2
        },
        {
            "id": 2,
            "name": "TestBot2",
            "full_name": "Test Bot Two",
            "age": 30,
            "gender": "Female",
            "category": ["hater"],
            "description": "Test bot for haters",
            "created_at": datetime.now(),
            "like_probability": 0.2,
            "comment_probability": 0.7,
            "post_probability": 0.1,
            "follow_probability": 0.2,
            "unfollow_probability": 0.3,
            "repost_probability": 0.1
        }
    ])
    
    manager.get_next_bot_id = MagicMock(return_value=3)
    manager.add_bot = MagicMock()
    manager.update_bot = MagicMock()
    
    return manager


@pytest.fixture
def llm_service():
    """Fixture for LLM service with mocked responses."""
    service = LLMService()
    
    # Mock methods
    service.generate_comment = MagicMock(return_value="This is a test comment")
    service.generate_post = MagicMock(return_value="This is a test post")
    service.generate_bot_description = MagicMock(return_value="This is a test description")
    
    return service


@pytest.fixture
def memory_service():
    """Fixture for memory service."""
    service = MemoryService()
    
    # Mock methods
    service.get_interaction_history = MagicMock(return_value="LIKE: Test post\nCOMMENT: Nice post!")
    service.add_interaction = MagicMock()
    
    return service


@pytest.fixture
def language_service():
    """Fixture for language service."""
    service = LanguageService()
    
    return service


@pytest.fixture
def post():
    """Fixture for a test post."""
    return Post(
        id=1,
        user_id="user1",
        content="This is a test post",
        timestamp=datetime.now()
    )


def test_should_like_post():
    """Test the probability-based decision for liking a post."""
    # Test with fan bot (high probability)
    bot = {
        "id": 1,
        "category": ["fan"],
        "like_probability": 0.8
    }
    post = Post(id=1, content="Test post")
    history = "LIKE: Previous post"
    
    # Run multiple times to account for randomness
    like_count = 0
    for _ in range(100):
        if _should_like_post(bot, post, history):
            like_count += 1
    
    # Fan bot should like posts more often than not
    assert like_count > 50
    
    # Test with hater bot (low probability)
    bot = {
        "id": 2,
        "category": ["hater"],
        "like_probability": 0.2
    }
    
    like_count = 0
    for _ in range(100):
        if _should_like_post(bot, post, history):
            like_count += 1
    
    # Hater bot should like posts less often
    assert like_count < 50


def test_should_comment_on_post():
    """Test the probability-based decision for commenting on a post."""
    # Test with humorous bot (high probability)
    bot = {
        "id": 1,
        "category": ["humorous"],
        "comment_probability": 0.7
    }
    post = Post(id=1, content="Test post")
    history = "COMMENT: Previous post"
    
    # Run multiple times to account for randomness
    comment_count = 0
    for _ in range(100):
        if _should_comment_on_post(bot, post, history):
            comment_count += 1
    
    # Humorous bot should comment more often
    assert comment_count > 50
    
    # Test with silent bot (low probability)
    bot = {
        "id": 2,
        "category": ["silent"],
        "comment_probability": 0.1
    }
    
    comment_count = 0
    for _ in range(100):
        if _should_comment_on_post(bot, post, history):
            comment_count += 1
    
    # Silent bot should comment less often
    assert comment_count < 30


def test_should_repost_post():
    """Test the probability-based decision for reposting a post."""
    # Test with fan bot (medium probability)
    bot = {
        "id": 1,
        "category": ["fan"],
        "repost_probability": 0.3
    }
    post = Post(id=1, content="Test post")
    history = "REPOST: Previous post"
    
    # Run multiple times to account for randomness
    repost_count = 0
    for _ in range(100):
        if _should_repost_post(bot, post, history):
            repost_count += 1
    
    # Fan bot should repost sometimes
    assert 20 < repost_count < 80
    
    # Test with silent bot (low probability)
    bot = {
        "id": 2,
        "category": ["silent"],
        "repost_probability": 0.05
    }
    
    repost_count = 0
    for _ in range(100):
        if _should_repost_post(bot, post, history):
            repost_count += 1
    
    # Silent bot should rarely repost
    assert repost_count < 20


def test_generate_bot_name():
    """Test bot name generation."""
    # Generate multiple names to ensure uniqueness
    names = [_generate_bot_name() for _ in range(10)]
    
    # Check that all names are strings
    assert all(isinstance(name, str) for name in names)
    
    # Check that all names are non-empty
    assert all(name for name in names)
    
    # Check that names are unique
    assert len(set(names)) == len(names)


def test_generate_avatar_url():
    """Test avatar URL generation using DiceBear."""
    name = "TestBot"
    avatar_url = _generate_avatar_url(name)
    
    # Check that URL is a string
    assert isinstance(avatar_url, str)
    
    # Check that URL contains DiceBear API
    assert "dicebear" in avatar_url
    
    # Check that URL contains the bot name as seed
    assert name in avatar_url


def test_calculate_behavior_probabilities():
    """Test behavior probability calculation based on bot categories."""
    # Test fan category
    probabilities = _calculate_behavior_probabilities(["fan"])
    like_prob, comment_prob, post_prob, follow_prob, unfollow_prob, repost_prob = probabilities
    
    # Fan should have high like and follow probabilities
    assert like_prob > 0.5
    assert follow_prob > 0.3
    
    # Test hater category
    probabilities = _calculate_behavior_probabilities(["hater"])
    like_prob, comment_prob, post_prob, follow_prob, unfollow_prob, repost_prob = probabilities
    
    # Hater should have low like probability but high comment probability
    assert like_prob < 0.5
    assert comment_prob > 0.2
    
    # Test silent category
    probabilities = _calculate_behavior_probabilities(["silent"])
    like_prob, comment_prob, post_prob, follow_prob, unfollow_prob, repost_prob = probabilities
    
    # Silent should have low comment and post probabilities
    assert comment_prob < 0.2
    assert post_prob < 0.1
    
    # Test multiple categories
    probabilities = _calculate_behavior_probabilities(["fan", "humorous"])
    like_prob, comment_prob, post_prob, follow_prob, unfollow_prob, repost_prob = probabilities
    
    # Fan + humorous should have high like, comment, and post probabilities
    assert like_prob > 0.5
    assert comment_prob > 0.4
    assert post_prob > 0.2


@patch('tasks.bot_tasks._create_new_bot')
def test_grow_bots(mock_create_new_bot, bot_manager):
    """Test the bot growth task."""
    # Mock dependencies
    mock_create_new_bot.return_value = Bot(
        id=3,
        name="NewBot",
        full_name="New Bot",
        age=25,
        gender="Male",
        category=["neutral"],
        description="New test bot",
        created_at=datetime.now()
    )
    
    # Mock settings
    with patch('tasks.bot_tasks.settings') as mock_settings:
        mock_settings.MAX_BOTS_COUNT = 10
        mock_settings.MAX_NEW_BOTS_PER_DAY = 5
        
        # Run the task
        with patch('tasks.bot_tasks.BotManager', return_value=bot_manager):
            result = grow_bots()
    
    # Check result
    assert result["status"] == "success"
    assert result["new_bots"] > 0
    assert mock_create_new_bot.call_count > 0


@patch('tasks.reaction_tasks._send_reactions_to_main_app')
def test_process_post_reactions(mock_send_reactions, bot_manager, llm_service, memory_service):
    """Test the post reaction processing task."""
    # Mock random to make tests deterministic
    with patch('random.random', return_value=0.1):
        # Mock dependencies
        with patch('tasks.reaction_tasks.BotManager', return_value=bot_manager):
            with patch('tasks.reaction_tasks.LLMService', return_value=llm_service):
                with patch('tasks.reaction_tasks.MemoryService', return_value=memory_service):
                    # Run the task
                    result = process_post_reactions({
                        "id": 1,
                        "user_id": "user1",
                        "content": "Test post",
                        "timestamp": datetime.now().isoformat()
                    })
    
    # Check result
    assert result["status"] == "success"
    assert "reactions_count" in result
    assert mock_send_reactions.called


def test_language_service(language_service):
    """Test the language service."""
    # Test language detection
    language = language_service.detect_language("Hello world")
    assert language == "en"
    
    # Test prompt language (always English)
    prompt_language = language_service.get_prompt_language("ru")
    assert prompt_language == "en"
    
    # Test content language adaptation
    content_language = language_service.get_content_language("ru")
    assert content_language == "ru"
    
    # Test prompt adaptation
    prompt = "Generate a comment"
    adapted_prompt = language_service.adapt_prompt_for_language(prompt, "ru")
    assert "Russian" in adapted_prompt
    
    # Test fallback content
    fallback = language_service.get_fallback_content("comment", ["fan"], "ru")
    assert isinstance(fallback, str)
    assert len(fallback) > 0


def test_llm_service_fallbacks(llm_service):
    """Test LLM service fallback mechanisms."""
    # Test fallback comment generation
    llm_service.default_llm = None
    llm_service.light_llm = None
    
    comment = llm_service._generate_fallback_comment(
        {"category": ["fan"]},
        "Test post"
    )
    assert isinstance(comment, str)
    assert len(comment) > 0
    
    # Test fallback post generation
    post = llm_service._generate_fallback_post(
        {"category": ["humorous"]},
        ["technology"]
    )
    assert isinstance(post, str)
    assert len(post) > 0
    
    # Test fallback description generation
    description = llm_service._generate_fallback_description(["neutral"])
    assert isinstance(description, str)
    assert len(description) > 0
