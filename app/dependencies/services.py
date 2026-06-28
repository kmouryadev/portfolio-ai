from app.services.chat_service import ChatService
from app.services.gemini_service import GeminiService
from app.services.prompt_service import PromptService

def get_prompt_service() -> PromptService:
  return PromptService()

def get_gemini_service() -> GeminiService:
  return GeminiService()

def get_chat_service() -> ChatService:
  return ChatService(
    gemini_service=get_gemini_service(),
    prompt_service=get_prompt_service(),
  )