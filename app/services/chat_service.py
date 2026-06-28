from app.schemas.chat import ChatResponse
from app.core.logger import logger
from app.core.exceptions import AppException
from app.services.gemini_service import GeminiService

class ChatService:
  """Service responsible for chat-related business logic."""

  def __init__(self, gemini_service: GeminiService) -> None:
    self._gemini_service = gemini_service

  async def send_message(self, message: str) -> ChatResponse:
    answer = await self._gemini_service.generate(message)

    return ChatResponse(
      answer=answer,
    )