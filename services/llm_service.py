# LangChain LLM service for bot text generation
from langchain.llms import OpenAI

class LLMService:
    def __init__(self):
        self.llm = OpenAI()

    def generate_text(self, prompt: str) -> str:
        return self.llm(prompt)
