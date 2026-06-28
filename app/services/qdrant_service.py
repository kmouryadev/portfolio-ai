from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from uuid import uuid4
from app.core.config import settings
from qdrant_client.models import Filter

class QdrantService:
  """Handles communication with Qdrant."""
  def __init__(self) -> None:
    self._client = QdrantClient(
      host=settings.qdrant_host,
      port=settings.qdrant_port,
    )
  def create_collection(
    self,
    vector_size: int,
  ) -> None:
    collections = self._client.get_collections()
    names = {
      collection.name for collection in collections.collections
    }
    if settings.collection_name in names:
      return
    self._client.create_collection(
      collection_name=settings.collection_name,
      vectors_config=VectorParams(
        size=vector_size,
        distance=Distance.COSINE,
        ),
      )
  def store_embeddings(
    self,
    chunks: list[str],
    embeddings: list[list[float]],
  ) -> None:
    points = []
    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
      points.append(
          PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={
                "text": chunk,
                "chunk_index": index,
            },
          )
      )
    self._client.upsert(
      collection_name=settings.collection_name,
      points=points,
    )
  def search(
    self,
    embedding: list[float],
    limit: int = 5,
  ) -> list[str]:
    results = self._client.query_points(
      collection_name=settings.collection_name,
      query=embedding,
      limit=limit,
    )
    matches = []
    for point in results.points:
      matches.append(
        {
          "text": point.payload["text"],
          "chunk_index": point.payload["chunk_index"],
          "score": point.score,
        }
      )
    return matches

