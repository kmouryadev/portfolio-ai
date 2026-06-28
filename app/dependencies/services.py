from app.services.chat_service import ChatService
from app.services.gemini_service import GeminiService

def get_gemini_service() -> GeminiService:
  return GeminiService()

def get_chat_service() -> ChatService:
  return ChatService(
    gemini_service=get_gemini_service(),
  )