from app.schemas.chat import ChatResponse
from app.core.logger import logger
from app.core.exceptions import AppException
from app.services.gemini_service import GeminiService
from app.services.prompt_service import PromptService
from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService

class ChatService:
  """Service responsible for chat-related business logic."""

  def __init__(
    self, 
    gemini_service: GeminiService,     
    prompt_service: PromptService,
    embedding_service: EmbeddingService,
    qdrant_service: QdrantService,
    ) -> None:
    self._gemini_service = gemini_service
    self._prompt_service = prompt_service
    self._embedding_service = embedding_service
    self._qdrant_service = qdrant_service

  async def send_message(
    self,
    message: str,
  ) -> ChatResponse:
    query_embedding = await self._embedding_service.generate_query_embedding(
      message
    )
    chunks = self._qdrant_service.search(
      embedding=query_embedding,
    )

    logger.info(
      "Retrieved %d chunks from Qdrant.",
      len(chunks),
    )
    if chunks:
      logger.info(
        "Top similarity score: %.4f",
        chunks[0]["score"],
      )
    prompt = self._prompt_service.build_chat_prompt(
      question=message,
      context=chunks,
    )
    answer = await self._gemini_service.generate(
      prompt
    )
    return ChatResponse(
      answer=answer,
    )