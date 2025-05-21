"""
LLM service for the Cartouche Bot Service.
Handles text generation for comments and bot descriptions.
"""
import logging
from typing import Dict, Any, Optional, List
import random

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory

from config import settings
from utils.cache_service import CacheService

logger = logging.getLogger(__name__)

class LLMService:
    """Service for generating text content using LLM."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LLM service.
        
        Args:
            api_key: Google API key. If not provided, uses the one from settings.
        """
        self.api_key = api_key or settings.GOOGLE_API_KEY
        self.default_model = settings.DEFAULT_LLM_MODEL
        self.light_model = settings.LIGHT_LLM_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
        self.cache_service = CacheService()
        
        # Initialize LLM models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize LLM models."""
        try:
            # Default model for complex tasks
            self.default_llm = ChatGoogleGenerativeAI(
                model=self.default_model,
                google_api_key=self.api_key,
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
                top_p=0.95,
                top_k=40,
                verbose=False
            )
            
            # Light model for simple tasks
            self.light_llm = ChatGoogleGenerativeAI(
                model=self.light_model,
                google_api_key=self.api_key,
                temperature=self.temperature,
                max_output_tokens=self.max_tokens // 2,
                top_p=0.95,
                top_k=40,
                verbose=False
            )
            
            logger.info("LLM models initialized successfully")
        
        except Exception as e:
            logger.error(f"Error initializing LLM models: {str(e)}")
            # Fallback to simple text generation
            self.default_llm = None
            self.light_llm = None
    
    def generate_comment(self, bot_profile: Dict[str, Any], post_content: str, history: str = "") -> str:
        """
        Generate a comment for a post.
        
        Args:
            bot_profile: Bot profile data
            post_content: Content of the post
            history: Interaction history
            
        Returns:
            Generated comment
        """
        # Check cache first
        cache_key = f"comment:{hash(str(bot_profile))}-{hash(post_content)}-{hash(history)}"
        cached_comment = self.cache_service.get(cache_key)
        if cached_comment:
            return cached_comment
        
        try:
            if self.light_llm:
                # Create prompt template
                template = """
                You are a social media bot with the following profile:
                Name: {name}
                Age: {age}
                Gender: {gender}
                Personality: {category}
                Description: {description}
                
                You need to write a comment on the following post:
                "{post_content}"
                
                Your previous interactions with this user:
                {history}
                
                Write a short, natural-sounding comment that matches your personality.
                Keep it brief (1-3 sentences) and conversational.
                Don't use hashtags unless they fit your personality.
                Don't mention that you're a bot.
                
                Your comment:
                """
                
                prompt = PromptTemplate(
                    input_variables=["name", "age", "gender", "category", "description", "post_content", "history"],
                    template=template
                )
                
                # Create chain
                chain = LLMChain(llm=self.light_llm, prompt=prompt)
                
                # Run chain
                result = chain.run(
                    name=bot_profile.get("name", "User"),
                    age=bot_profile.get("age", 30),
                    gender=bot_profile.get("gender", "Unknown"),
                    category=", ".join(bot_profile.get("category", ["neutral"])),
                    description=bot_profile.get("description", "A social media user"),
                    post_content=post_content,
                    history=history or "No previous interactions"
                )
                
                # Clean result
                comment = result.strip()
                
                # Cache result
                self.cache_service.set(cache_key, comment, ttl=86400)  # Cache for 24 hours
                
                return comment
            
            else:
                # Fallback to simple comment generation
                return self._generate_fallback_comment(bot_profile, post_content)
        
        except Exception as e:
            logger.error(f"Error generating comment: {str(e)}")
            return self._generate_fallback_comment(bot_profile, post_content)
    
    def generate_bot_description(self, name: str, age: int, gender: str, categories: List[str]) -> str:
        """
        Generate a description for a bot.
        
        Args:
            name: Bot name
            age: Bot age
            gender: Bot gender
            categories: Bot categories
            
        Returns:
            Generated description
        """
        # Check cache first
        cache_key = f"description:{name}-{age}-{gender}-{'-'.join(categories)}"
        cached_description = self.cache_service.get(cache_key)
        if cached_description:
            return cached_description
        
        try:
            if self.default_llm:
                # Create prompt template
                template = """
                Create a social media profile description for a person with the following characteristics:
                Name: {name}
                Age: {age}
                Gender: {gender}
                Personality traits: {categories}
                
                The description should be:
                1. Brief (2-4 sentences)
                2. Natural and conversational
                3. Reflect the personality traits
                4. Not mention being a bot or AI
                5. Include interests, hobbies, or profession that would fit this profile
                
                Profile description:
                """
                
                prompt = PromptTemplate(
                    input_variables=["name", "age", "gender", "categories"],
                    template=template
                )
                
                # Create chain
                chain = LLMChain(llm=self.default_llm, prompt=prompt)
                
                # Run chain
                result = chain.run(
                    name=name,
                    age=age,
                    gender=gender,
                    categories=", ".join(categories)
                )
                
                # Clean result
                description = result.strip()
                
                # Cache result
                self.cache_service.set(cache_key, description, ttl=604800)  # Cache for 7 days
                
                return description
            
            else:
                # Fallback to simple description generation
                return self._generate_fallback_description(categories)
        
        except Exception as e:
            logger.error(f"Error generating bot description: {str(e)}")
            return self._generate_fallback_description(categories)
    
    def generate_post(self, bot_profile: Dict[str, Any], interests: List[str] = None, recent_activity: str = "") -> str:
        """
        Generate a post for a bot.
        
        Args:
            bot_profile: Bot profile data
            interests: Bot interests
            recent_activity: Recent activity in the social network
            
        Returns:
            Generated post
        """
        # Check cache first
        cache_key = f"post:{hash(str(bot_profile))}-{hash(str(interests))}-{hash(recent_activity)}"
        cached_post = self.cache_service.get(cache_key)
        if cached_post:
            return cached_post
        
        try:
            if self.default_llm:
                # Create prompt template
                template = """
                You are a social media user with the following profile:
                Name: {name}
                Age: {age}
                Gender: {gender}
                Personality: {category}
                Description: {description}
                
                Your interests include: {interests}
                
                Recent activity in your social network:
                {recent_activity}
                
                Write a social media post that:
                1. Reflects your personality and interests
                2. Is natural and conversational
                3. Is appropriate for your age and background
                4. Doesn't mention being a bot or AI
                5. Is between 1-4 sentences long
                
                Your post:
                """
                
                prompt = PromptTemplate(
                    input_variables=["name", "age", "gender", "category", "description", "interests", "recent_activity"],
                    template=template
                )
                
                # Create chain
                chain = LLMChain(llm=self.default_llm, prompt=prompt)
                
                # Run chain
                result = chain.run(
                    name=bot_profile.get("name", "User"),
                    age=bot_profile.get("age", 30),
                    gender=bot_profile.get("gender", "Unknown"),
                    category=", ".join(bot_profile.get("category", ["neutral"])),
                    description=bot_profile.get("description", "A social media user"),
                    interests=", ".join(interests or ["general topics"]),
                    recent_activity=recent_activity or "Various discussions about everyday life"
                )
                
                # Clean result
                post = result.strip()
                
                # Cache result
                self.cache_service.set(cache_key, post, ttl=86400)  # Cache for 24 hours
                
                return post
            
            else:
                # Fallback to simple post generation
                return self._generate_fallback_post(bot_profile, interests)
        
        except Exception as e:
            logger.error(f"Error generating post: {str(e)}")
            return self._generate_fallback_post(bot_profile, interests)
    
    def _generate_fallback_comment(self, bot_profile: Dict[str, Any], post_content: str) -> str:
        """
        Generate a fallback comment when LLM is not available.
        
        Args:
            bot_profile: Bot profile data
            post_content: Content of the post
            
        Returns:
            Generated comment
        """
        # Simple comments based on bot category
        categories = bot_profile.get("category", ["neutral"])
        
        fan_comments = [
            "Love this! 👍",
            "Great post! Thanks for sharing.",
            "This is amazing content!",
            "I'm a big fan of this. Keep it up!",
            "Awesome! Can't wait to see more."
        ]
        
        hater_comments = [
            "Not sure I agree with this...",
            "Is this really necessary?",
            "I've seen better content elsewhere.",
            "This could use some improvement.",
            "Interesting take, but I disagree."
        ]
        
        neutral_comments = [
            "Interesting perspective.",
            "Thanks for sharing this.",
            "I see what you mean.",
            "Good point.",
            "Nice post."
        ]
        
        humorous_comments = [
            "This made my day! 😂",
            "Haha, love it!",
            "I'm laughing way too hard at this.",
            "Comedy gold right here!",
            "This is hilarious!"
        ]
        
        provocative_comments = [
            "But have you considered the opposite view?",
            "This is a controversial take...",
            "I wonder what others think about this?",
            "This will definitely start a debate.",
            "Bold statement. Care to elaborate?"
        ]
        
        # Select appropriate comment pool based on bot category
        if "fan" in categories:
            comments = fan_comments
        elif "hater" in categories:
            comments = hater_comments
        elif "humorous" in categories:
            comments = humorous_comments
        elif "provocative" in categories:
            comments = provocative_comments
        else:
            comments = neutral_comments
        
        # Return random comment
        return random.choice(comments)
    
    def _generate_fallback_description(self, categories: List[str]) -> str:
        """
        Generate a fallback description when LLM is not available.
        
        Args:
            categories: Bot categories
            
        Returns:
            Generated description
        """
        # Simple descriptions based on categories
        descriptions = {
            "fan": [
                "Always supporting interesting ideas and projects!",
                "I love finding new talents and supporting them.",
                "Your most devoted fan in everything you do!"
            ],
            "hater": [
                "Critical view of everything around.",
                "Not afraid to speak the truth, even if it's unpleasant.",
                "Skeptic by nature, I only believe facts."
            ],
            "neutral": [
                "Objective observer of what's happening.",
                "I value balance and fairness in everything.",
                "I try to see all sides of a situation."
            ],
            "humorous": [
                "Life is too short to be serious!",
                "Humor is my middle name. The first one is also good.",
                "Looking for reasons to smile every day."
            ],
            "provocative": [
                "I love asking uncomfortable questions.",
                "Sometimes you need to shake the system to see the truth.",
                "Provocation is the path to truth."
            ],
            "silent": [
                "I prefer to observe rather than speak.",
                "Silence is golden, especially on social media.",
                "I rarely comment, but I'm always aware of what's happening."
            ],
            "random": [
                "Unpredictability is my credo.",
                "Today I'm one person, tomorrow I'm completely different.",
                "Life is a kaleidoscope of randomness."
            ],
            "roleplay": [
                "I love trying on different roles and characters.",
                "I'm different in every situation, but always sincere.",
                "Life is a theater, and I'm an actor in it."
            ]
        }
        
        # Select descriptions based on categories
        selected_descriptions = []
        for category in categories:
            if category in descriptions:
                selected_descriptions.append(random.choice(descriptions[category]))
        
        # If no descriptions were selected, use a generic one
        if not selected_descriptions:
            selected_descriptions = ["I'm interested in various topics and always open to communication."]
        
        # Return combined description
        return " ".join(selected_descriptions)
    
    def _generate_fallback_post(self, bot_profile: Dict[str, Any], interests: List[str] = None) -> str:
        """
        Generate a fallback post when LLM is not available.
        
        Args:
            bot_profile: Bot profile data
            interests: Bot interests
            
        Returns:
            Generated post
        """
        # Simple posts based on bot category
        categories = bot_profile.get("category", ["neutral"])
        
        fan_posts = [
            "Just discovered an amazing new artist! Check them out!",
            "This new album is absolutely incredible. Can't stop listening!",
            "Been following this project for a while and it just keeps getting better!",
            "So impressed by the talent in this community!",
            "Supporting creative people is what makes life beautiful."
        ]
        
        hater_posts = [
            "Why does everyone pretend to like this trend? It's clearly overrated.",
            "Hot take: quality has been declining lately in this industry.",
            "Unpopular opinion: sometimes the classics are better than the new stuff.",
            "Not impressed by the latest releases. We deserve better.",
            "Am I the only one who sees the problems with this?"
        ]
        
        neutral_posts = [
            "Interesting article I read today about technology advancements.",
            "The weather has been quite unusual lately. Climate change effects?",
            "Just finished a good book. Always nice to find time to read.",
            "Thinking about the balance between work and personal life.",
            "Sometimes taking a step back helps to see the bigger picture."
        ]
        
        humorous_posts = [
            "My cooking skills are so bad, my smoke detector works as a timer!",
            "Just tried to impress my cat with my new outfit. Got completely ignored. Tough crowd!",
            "Pro tip: if you can't find something, clean your house. You won't find it, but at least your house will be clean!",
            "My fitness plan is going great! I've already completed day one, seventeen times!",
            "Why did I spend 30 minutes scrolling through social media to avoid a 5-minute task? We may never know."
        ]
        
        provocative_posts = [
            "Does anyone else think the current system is fundamentally flawed?",
            "Controversial opinion: sometimes the popular choice isn't the right one.",
            "What if everything we've been taught about success is wrong?",
            "The real problem isn't what everyone is talking about, it's what no one mentions.",
            "Sometimes the most uncomfortable questions lead to the most important answers."
        ]
        
        # Select appropriate post pool based on bot category
        if "fan" in categories:
            posts = fan_posts
        elif "hater" in categories:
            posts = hater_posts
        elif "humorous" in categories:
            posts = humorous_posts
        elif "provocative" in categories:
            posts = provocative_posts
        else:
            posts = neutral_posts
        
        # Return random post
        return random.choice(posts)
