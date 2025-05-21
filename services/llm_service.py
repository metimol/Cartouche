# LangChain LLM service for bot text generation
from services.gemini_llm import GeminiLLM

class LLMService:
    def __init__(self, google_api_key=None):
        self.llm = GeminiLLM(google_api_key=google_api_key)

    def generate_text(self, prompt: str) -> str:
        return self.llm(prompt)
