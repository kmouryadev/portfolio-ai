from google import genai

from app.core.config import settings


class EmbeddingService:
    """Service responsible for generating text embeddings."""

    def __init__(self) -> None:
        self._client = genai.Client(
            api_key=settings.google_api_key,
        )
        self._model = settings.embedding_model

    async def generate_embeddings(
        self,
        chunks: list[str],
    ) -> list[list[float]]:
        embeddings: list[list[float]] = []
        for chunk in chunks:
            response = self._client.models.embed_content(
                model=self._model,
                contents=chunk,
            )
            embeddings.append(response.embeddings[0].values)
        return embeddings

    async def generate_query_embedding(
        self,
        query: str,
    ) -> list[float]:
        response = self._client.models.embed_content(
            model=self._model,
            contents=query,
        )
        return response.embeddings[0].values
