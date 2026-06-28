from app.schemas.chat import ChatResponse

class ChatService:
  """Service responsible for chat-related business logic."""

  async def send_message(self, message: str) -> ChatResponse:
    return ChatResponse(
      answer=f"You said: {message}"
    )