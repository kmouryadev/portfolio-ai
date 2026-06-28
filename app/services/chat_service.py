from app.schemas.chat import ChatResponse
from app.core.logger import logger

class ChatService:
  """Service responsible for chat-related business logic."""

  async def send_message(self, message: str) -> ChatResponse:
    logger.info("Received chat message: %s", message)
    return ChatResponse(
      answer=f"You said: {message}"
    )