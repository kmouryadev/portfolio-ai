from unittest.mock import AsyncMock, MagicMock

import pytest

from app.schemas.chat import ChatResponse
from app.services.chat_service import ChatService


class TestChatService:
    @pytest.mark.asyncio
    async def test_send_message_success(self):

        gemini_service = MagicMock()
        gemini_service.generate = AsyncMock(
            return_value="Karun has 3.5 years of experience."
        )

        prompt_service = MagicMock()
        prompt_service.build_chat_prompt.return_value = "Generated Prompt"

        embedding_service = MagicMock()
        embedding_service.generate_query_embedding = AsyncMock(
            return_value=[0.1, 0.2, 0.3]
        )

        qdrant_service = MagicMock()
        qdrant_service.search.return_value = [
            {
                "text": "Karun has 3.5 years of experience.",
                "score": 0.95,
                "chunk_index": 0,
            }
        ]

        service = ChatService(
            gemini_service=gemini_service,
            prompt_service=prompt_service,
            embedding_service=embedding_service,
            qdrant_service=qdrant_service,
        )

        response = await service.send_message(
            "How many years of experience does Karun have?"
        )

        assert isinstance(
            response,
            ChatResponse,
        )

        assert response.answer == "Karun has 3.5 years of experience."

        embedding_service.generate_query_embedding.assert_awaited_once()

        qdrant_service.search.assert_called_once()

        prompt_service.build_chat_prompt.assert_called_once()

        gemini_service.generate.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_send_message_without_context(self):

        gemini_service = MagicMock()
        gemini_service.generate = AsyncMock(return_value="Fallback")

        prompt_service = MagicMock()
        prompt_service.build_chat_prompt.return_value = "Prompt"

        embedding_service = MagicMock()
        embedding_service.generate_query_embedding = AsyncMock(return_value=[0.1])

        qdrant_service = MagicMock()
        qdrant_service.search.return_value = []

        service = ChatService(
            gemini_service,
            prompt_service,
            embedding_service,
            qdrant_service,
        )

        response = await service.send_message("Unknown question")

        assert response.answer == "Fallback"
