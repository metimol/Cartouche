"""
Content generator for the Cartouche Autonomous Service.
Handles text generation for posts, comments, and bot descriptions.
"""
import logging
import random
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from config import GOOGLE_API_KEY, DEFAULT_LLM_MODEL, LIGHT_LLM_MODEL, MAX_TOKENS, TEMPERATURE

logger = logging.getLogger(__name__)

class ContentGenerator:
    """Generator for text content using LLM."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the content generator.
        
        Args:
            api_key: Google API key. If not provided, uses the one from config.
        """
        self.api_key = api_key or GOOGLE_API_KEY
        self.default_model = DEFAULT_LLM_MODEL
        self.light_model = LIGHT_LLM_MODEL
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
        
        # Initialize LLM models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize LLM models."""
        try:
            # Configure Google Generative AI
            genai.configure(api_key=self.api_key)
            
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
    
    async def generate_comment(self, bot_profile: Dict[str, Any], post_content: str, history: str = "") -> str:
        """
        Generate a comment for a post.
        
        Args:
            bot_profile: Bot profile data
            post_content: Content of the post
            history: Interaction history
            
        Returns:
            Generated comment
        """
        try:
            if self.light_llm:
                # Create prompt template
                template = """
                Ты бот в социальной сети со следующим профилем:
                Имя: {name}
                Возраст: {age}
                Пол: {gender}
                Личность: {categories}
                Описание: {description}
                
                Тебе нужно написать комментарий к следующему посту:
                "{post_content}"
                
                Твои предыдущие взаимодействия с этим пользователем:
                {history}
                
                Напиши короткий, естественно звучащий комментарий, соответствующий твоей личности.
                Комментарий должен быть кратким (1-3 предложения) и разговорным.
                Не используй хэштеги, если они не соответствуют твоей личности.
                Не упоминай, что ты бот.
                
                Твой комментарий:
                """
                
                prompt = PromptTemplate(
                    input_variables=["name", "age", "gender", "categories", "description", "post_content", "history"],
                    template=template
                )
                
                # Create chain
                chain = LLMChain(llm=self.light_llm, prompt=prompt)
                
                # Run chain
                result = await chain.arun(
                    name=bot_profile.get("name", "User"),
                    age=bot_profile.get("age", 30),
                    gender=bot_profile.get("gender", "Unknown"),
                    categories=", ".join(bot_profile.get("categories", ["neutral"])),
                    description=bot_profile.get("description", "Пользователь социальной сети"),
                    post_content=post_content,
                    history=history or "Нет предыдущих взаимодействий"
                )
                
                # Clean result
                comment = result.strip()
                
                return comment
            
            else:
                # Fallback to simple comment generation
                return self._generate_fallback_comment(bot_profile, post_content)
        
        except Exception as e:
            logger.error(f"Error generating comment: {str(e)}")
            return self._generate_fallback_comment(bot_profile, post_content)
    
    async def generate_bot_description(self, name: str, age: int, gender: str, categories: List[str]) -> str:
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
        try:
            if self.default_llm:
                # Create prompt template
                template = """
                Создай описание профиля в социальной сети для человека со следующими характеристиками:
                Имя: {name}
                Возраст: {age}
                Пол: {gender}
                Черты личности: {categories}
                
                Описание должно быть:
                1. Кратким (2-4 предложения)
                2. Естественным и разговорным
                3. Отражать черты личности
                4. Не упоминать о том, что это бот или ИИ
                5. Включать интересы, хобби или профессию, которые подходят этому профилю
                
                Описание профиля:
                """
                
                prompt = PromptTemplate(
                    input_variables=["name", "age", "gender", "categories"],
                    template=template
                )
                
                # Create chain
                chain = LLMChain(llm=self.default_llm, prompt=prompt)
                
                # Run chain
                result = await chain.arun(
                    name=name,
                    age=age,
                    gender=gender,
                    categories=", ".join(categories)
                )
                
                # Clean result
                description = result.strip()
                
                return description
            
            else:
                # Fallback to simple description generation
                return self._generate_fallback_description(categories)
        
        except Exception as e:
            logger.error(f"Error generating bot description: {str(e)}")
            return self._generate_fallback_description(categories)
    
    async def generate_post(self, bot_profile: Dict[str, Any], interests: List[str] = None, recent_activity: str = "") -> str:
        """
        Generate a post for a bot.
        
        Args:
            bot_profile: Bot profile data
            interests: Bot interests
            recent_activity: Recent activity in the social network
            
        Returns:
            Generated post
        """
        try:
            if self.default_llm:
                # Create prompt template
                template = """
                Ты пользователь социальной сети со следующим профилем:
                Имя: {name}
                Возраст: {age}
                Пол: {gender}
                Личность: {categories}
                Описание: {description}
                
                Твои интересы включают: {interests}
                
                Недавняя активность в твоей социальной сети:
                {recent_activity}
                
                Напиши пост в социальной сети, который:
                1. Отражает твою личность и интересы
                2. Звучит естественно и разговорно
                3. Соответствует твоему возрасту и происхождению
                4. Не упоминает о том, что ты бот или ИИ
                5. Состоит из 1-4 предложений
                
                Твой пост:
                """
                
                prompt = PromptTemplate(
                    input_variables=["name", "age", "gender", "categories", "description", "interests", "recent_activity"],
                    template=template
                )
                
                # Create chain
                chain = LLMChain(llm=self.default_llm, prompt=prompt)
                
                # Run chain
                result = await chain.arun(
                    name=bot_profile.get("name", "User"),
                    age=bot_profile.get("age", 30),
                    gender=bot_profile.get("gender", "Unknown"),
                    categories=", ".join(bot_profile.get("categories", ["neutral"])),
                    description=bot_profile.get("description", "Пользователь социальной сети"),
                    interests=", ".join(interests or ["общие темы"]),
                    recent_activity=recent_activity or "Различные обсуждения о повседневной жизни"
                )
                
                # Clean result
                post = result.strip()
                
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
        categories = bot_profile.get("categories", ["neutral"])
        
        fan_comments = [
            "Обожаю это! 👍",
            "Отличный пост! Спасибо, что поделились.",
            "Это потрясающий контент!",
            "Я большой поклонник этого. Так держать!",
            "Круто! Жду с нетерпением новых постов."
        ]
        
        hater_comments = [
            "Не уверен, что согласен с этим...",
            "Это действительно необходимо?",
            "Я видел контент и получше.",
            "Это можно было бы улучшить.",
            "Интересная точка зрения, но я не согласен."
        ]
        
        neutral_comments = [
            "Интересная перспектива.",
            "Спасибо, что поделились этим.",
            "Понимаю, о чем вы.",
            "Хороший аргумент.",
            "Неплохой пост."
        ]
        
        humorous_comments = [
            "Это сделало мой день! 😂",
            "Ха-ха, обожаю!",
            "Я слишком сильно смеюсь над этим.",
            "Комедия высшего сорта!",
            "Это уморительно!"
        ]
        
        provocative_comments = [
            "А вы рассматривали противоположную точку зрения?",
            "Это довольно спорное утверждение...",
            "Интересно, что другие думают об этом?",
            "Это определенно вызовет дискуссию.",
            "Смелое заявление. Не могли бы вы пояснить?"
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
                "Всегда поддерживаю интересные идеи и проекты!",
                "Люблю находить новые таланты и поддерживать их.",
                "Ваш самый преданный поклонник во всем, что вы делаете!"
            ],
            "hater": [
                "Критический взгляд на все вокруг.",
                "Не боюсь говорить правду, даже если она неприятна.",
                "Скептик по натуре, верю только фактам."
            ],
            "neutral": [
                "Объективный наблюдатель происходящего.",
                "Ценю баланс и справедливость во всем.",
                "Стараюсь видеть все стороны ситуации."
            ],
            "humorous": [
                "Жизнь слишком коротка, чтобы быть серьезным!",
                "Юмор - мое второе имя. Первое тоже неплохое.",
                "Ищу поводы для улыбки каждый день."
            ],
            "provocative": [
                "Люблю задавать неудобные вопросы.",
                "Иногда нужно встряхнуть систему, чтобы увидеть правду.",
                "Провокация - путь к истине."
            ],
            "silent": [
                "Предпочитаю наблюдать, а не говорить.",
                "Молчание - золото, особенно в социальных сетях.",
                "Редко комментирую, но всегда в курсе происходящего."
            ],
            "random": [
                "Непредсказуемость - мое кредо.",
                "Сегодня я один человек, завтра - совершенно другой.",
                "Жизнь - калейдоскоп случайностей."
            ],
            "roleplay": [
                "Люблю примерять на себя разные роли и характеры.",
                "В каждой ситуации я разный, но всегда искренний.",
                "Жизнь - театр, а я в нем актер."
            ]
        }
        
        # Select descriptions based on categories
        selected_descriptions = []
        for category in categories:
            if category in descriptions:
                selected_descriptions.append(random.choice(descriptions[category]))
        
        # If no descriptions were selected, use a generic one
        if not selected_descriptions:
            selected_descriptions = ["Интересуюсь разными темами и люблю общаться с людьми."]
        
        # Combine descriptions
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
        categories = bot_profile.get("categories", ["neutral"])
        
        fan_posts = [
            "Сегодня отличный день для новых открытий! Что нового у всех?",
            "Только что нашел потрясающий контент, который стоит посмотреть!",
            "Так благодарен за эту платформу и всех замечательных людей здесь!",
            "Кто еще в восторге от последних трендов? Я точно да!",
            "Поддерживаю всех творческих людей! Продолжайте вдохновлять нас!"
        ]
        
        hater_posts = [
            "Почему никто не говорит о реальных проблемах? Все слишком поверхностно.",
            "Не понимаю, почему все так восхищаются последними трендами. Ничего особенного.",
            "Качество контента в последнее время сильно упало. Кто-нибудь еще это замечает?",
            "Иногда мне кажется, что я единственный, кто видит недостатки во всем этом.",
            "Критическое мышление сегодня в дефиците. Слишком много слепого восхищения."
        ]
        
        neutral_posts = [
            "Интересно наблюдать за развитием дискуссий на разные темы.",
            "Сегодня прочитал интересную статью о последних событиях. Много пищи для размышлений.",
            "Баланс разных точек зрения - ключ к пониманию сложных вопросов.",
            "Наблюдаю за трендами с интересом, хотя не всегда с ними согласен.",
            "Важно сохранять объективность при оценке информации."
        ]
        
        humorous_posts = [
            "Если бы мои мысли были озвучены, я бы уже давно был в комедийном шоу! 😂",
            "Только что пытался приготовить ужин. Пожарная служба оценила мои старания!",
            "Моя кошка смотрит на меня так, будто я задолжал ей деньги. Много денег.",
            "Жизненный совет дня: никогда не говорите 'что может пойти не так?' вслух.",
            "Мой уровень сарказма сегодня зашкаливает. Извините заранее!"
        ]
        
        provocative_posts = [
            "А что, если все, во что мы верим, основано на ложных предпосылках?",
            "Почему никто не задает неудобные вопросы о том, что происходит?",
            "Общество слишком быстро принимает новые идеи без критического анализа.",
            "Интересно, сколько людей действительно формируют собственное мнение, а не следуют за большинством?",
            "Самые важные истины часто скрываются за комфортными иллюзиями."
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
