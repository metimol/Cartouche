"""
Language utilities for the Cartouche Bot Service.
Handles language detection and translation.
"""
import logging
from typing import Dict, Any, Optional, List
import random

from config import settings

logger = logging.getLogger(__name__)

class LanguageService:
    """Service for language detection and adaptation."""
    
    def __init__(self):
        """Initialize the language service."""
        self.default_language = settings.DEFAULT_LANGUAGE
        self.supported_languages = settings.SUPPORTED_LANGUAGES
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of a text.
        
        Args:
            text: Text to detect language from
            
        Returns:
            Language code (e.g., 'en', 'ru')
        """
        # In a real implementation, this would use a language detection library
        # For now, we'll just return the default language
        return self.default_language
    
    def get_prompt_language(self, user_language: Optional[str] = None) -> str:
        """
        Get the language to use for prompts.
        
        Args:
            user_language: User's language code
            
        Returns:
            Language code for prompts (always 'en')
        """
        # Prompts are always in English
        return 'en'
    
    def get_content_language(self, user_language: Optional[str] = None) -> str:
        """
        Get the language to use for generated content.
        
        Args:
            user_language: User's language code
            
        Returns:
            Language code for content
        """
        # If user language is provided and supported, use it
        if user_language and user_language in self.supported_languages:
            return user_language
        
        # Otherwise, use default language
        return self.default_language
    
    def adapt_prompt_for_language(self, prompt: str, target_language: str) -> str:
        """
        Adapt a prompt to generate content in the target language.
        
        Args:
            prompt: Original prompt in English
            target_language: Target language code
            
        Returns:
            Adapted prompt
        """
        # Map of language codes to language names
        language_names = {
            'en': 'English',
            'ru': 'Russian',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German'
        }
        
        # Get language name
        language_name = language_names.get(target_language, 'English')
        
        # Add language instruction to the prompt
        if target_language != 'en':
            # Add instruction to generate content in the target language
            return f"{prompt}\n\nPlease generate the response in {language_name}."
        
        # For English, no adaptation needed
        return prompt
    
    def get_fallback_content(self, content_type: str, categories: List[str], language: str) -> str:
        """
        Get fallback content in the specified language.
        
        Args:
            content_type: Type of content ('comment', 'post', 'description')
            categories: Bot categories
            language: Target language code
            
        Returns:
            Fallback content in the specified language
        """
        # Fallback content in different languages
        fallback_content = {
            'en': {
                'comment': {
                    'fan': [
                        "Love this! 👍",
                        "Great post! Thanks for sharing.",
                        "This is amazing content!"
                    ],
                    'hater': [
                        "Not sure I agree with this...",
                        "Is this really necessary?",
                        "I've seen better content elsewhere."
                    ],
                    'neutral': [
                        "Interesting perspective.",
                        "Thanks for sharing this.",
                        "I see what you mean."
                    ]
                },
                'post': {
                    'fan': [
                        "Just discovered an amazing new artist! Check them out!",
                        "This new album is absolutely incredible. Can't stop listening!",
                        "Been following this project for a while and it just keeps getting better!"
                    ],
                    'hater': [
                        "Why does everyone pretend to like this trend? It's clearly overrated.",
                        "Hot take: quality has been declining lately in this industry.",
                        "Unpopular opinion: sometimes the classics are better than the new stuff."
                    ],
                    'neutral': [
                        "Interesting article I read today about technology advancements.",
                        "The weather has been quite unusual lately. Climate change effects?",
                        "Just finished a good book. Always nice to find time to read."
                    ]
                },
                'description': {
                    'fan': [
                        "Always supporting interesting ideas and projects!",
                        "I love finding new talents and supporting them."
                    ],
                    'hater': [
                        "Critical view of everything around.",
                        "Not afraid to speak the truth, even if it's unpleasant."
                    ],
                    'neutral': [
                        "Objective observer of what's happening.",
                        "I value balance and fairness in everything."
                    ]
                }
            },
            'ru': {
                'comment': {
                    'fan': [
                        "Обожаю это! 👍",
                        "Отличный пост! Спасибо, что поделились.",
                        "Это потрясающий контент!"
                    ],
                    'hater': [
                        "Не уверен, что согласен с этим...",
                        "Это действительно необходимо?",
                        "Я видел контент получше."
                    ],
                    'neutral': [
                        "Интересная точка зрения.",
                        "Спасибо, что поделились.",
                        "Понимаю, о чём вы."
                    ]
                },
                'post': {
                    'fan': [
                        "Только что открыл для себя потрясающего нового артиста! Обязательно посмотрите!",
                        "Этот новый альбом просто невероятный. Не могу перестать слушать!",
                        "Слежу за этим проектом уже некоторое время, и он становится только лучше!"
                    ],
                    'hater': [
                        "Почему все притворяются, что им нравится этот тренд? Он явно переоценен.",
                        "Горячее мнение: качество в последнее время падает в этой индустрии.",
                        "Непопулярное мнение: иногда классика лучше новинок."
                    ],
                    'neutral': [
                        "Интересная статья, которую я прочитал сегодня о технологических достижениях.",
                        "Погода в последнее время довольно необычная. Эффекты изменения климата?",
                        "Только что закончил хорошую книгу. Всегда приятно найти время для чтения."
                    ]
                },
                'description': {
                    'fan': [
                        "Всегда поддерживаю интересные идеи и проекты!",
                        "Люблю находить новые таланты и поддерживать их."
                    ],
                    'hater': [
                        "Критический взгляд на всё вокруг.",
                        "Не боюсь говорить правду, даже если она неприятна."
                    ],
                    'neutral': [
                        "Объективный наблюдатель за происходящим.",
                        "Ценю баланс и справедливость во всём."
                    ]
                }
            }
        }
        
        # If language is not supported, use English
        if language not in fallback_content:
            language = 'en'
        
        # Get content for the specified type
        content_by_type = fallback_content[language].get(content_type, {})
        
        # Find content for the specified category
        for category in categories:
            if category in content_by_type:
                return random.choice(content_by_type[category])
        
        # If no matching category, use neutral
        if 'neutral' in content_by_type:
            return random.choice(content_by_type['neutral'])
        
        # If all else fails, return a generic message
        if language == 'ru':
            return "Интересный контент!"
        else:
            return "Interesting content!"
