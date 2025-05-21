# Google Gemini LLM setup for LangChain
from langchain.chat_models import init_chat_model
import os
import getpass

class GeminiLLM:
    def __init__(self, model="gemini-2.0-flash", google_api_key=None):
        if google_api_key:
            os.environ["GOOGLE_API_KEY"] = google_api_key
        
        if not os.environ.get("GOOGLE_API_KEY"):
            os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")
        self.llm = init_chat_model(model, model_provider="google_genai")

    def __call__(self, prompt: str) -> str:
        return self.llm(prompt)
