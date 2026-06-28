from app.schemas.chat import ChatResponse
from app.core.logger import logger
from app.core.exceptions import AppException
from app.services.gemini_service import GeminiService
from app.services.prompt_service import PromptService

class ChatService:
  """Service responsible for chat-related business logic."""

  def __init__(
    self, 
    gemini_service: GeminiService,     
    prompt_service: PromptService,
    ) -> None:
    self._gemini_service = gemini_service
    self._prompt_service = prompt_service

  async def send_message(self, message: str) -> ChatResponse:
    prompt = self._prompt_service.build_chat_prompt(
        message=message,
    )
    answer = await self._gemini_service.generate(prompt)

    return ChatResponse(
      answer=answer,
    )