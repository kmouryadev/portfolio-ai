from unittest.mock import MagicMock

from app.services.qdrant_service import QdrantService


class TestQdrantService:
    def test_search_returns_chunks(self):
        service = QdrantService()
        point = MagicMock()
        point.payload = {
            "text": "Karun knows FastAPI",
            "chunk_index": 0,
        }
        point.score = 0.98
        result = MagicMock()
        result.points = [point]
        service._client = MagicMock()
        service._client.query_points.return_value = result
        response = service.search(
            embedding=[0.1, 0.2],
        )
        assert len(response) == 1
        assert response[0]["text"] == "Karun knows FastAPI"
        assert response[0]["score"] == 0.98

    def test_create_collection_existing(self):
        service = QdrantService()
        collection = MagicMock()
        collection.name = "portfolio_resume"
        collections = MagicMock()
        collections.collections = [
            collection,
        ]
        service._client = MagicMock()
        service._client.get_collections.return_value = collections
        service.create_collection(
            vector_size=3072,
        )
        service._client.create_collection.assert_not_called()
