from unittest.mock import MagicMock

import pytest

from app.services.embedding_service import EmbeddingService


class TestEmbeddingService:
    @pytest.mark.asyncio
    async def test_generate_query_embedding(self):
        service = EmbeddingService()
        embedding = MagicMock()
        embedding.values = [0.1, 0.2, 0.3]
        response = MagicMock()
        response.embeddings = [embedding]
        service._client = MagicMock()
        service._client.models.embed_content.return_value = response
        result = await service.generate_query_embedding(
            "What technologies does Karun know?"
        )
        assert result == [0.1, 0.2, 0.3]
        service._client.models.embed_content.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_embeddings(self):
        service = EmbeddingService()
        embedding1 = MagicMock()
        embedding1.values = [1, 2]
        embedding2 = MagicMock()
        embedding2.values = [3, 4]
        response1 = MagicMock()
        response1.embeddings = [embedding1]

        response2 = MagicMock()
        response2.embeddings = [embedding2]

        service._client = MagicMock()
        service._client.models.embed_content.side_effect = [
            response1,
            response2,
        ]
        result = await service.generate_embeddings(
            [
                "chunk one",
                "chunk two",
            ]
        )
        assert len(result) == 2
        assert result[0] == [1, 2]
        assert result[1] == [3, 4]
