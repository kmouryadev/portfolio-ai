from unittest.mock import AsyncMock, MagicMock

import pytest

@pytest.fixture
def sample_text():
  return (
    "FastAPI React Next.js Python PostgreSQL "
    * 50
  )

@pytest.fixture
def sample_chunks():
  return [
    "Karun has experience in React and Next.js.",
    "Karun has experience in FastAPI.",
    "Karun has experience in Python.",
  ]


@pytest.fixture
def sample_embeddings():
  return [
    [0.1, 0.2, 0.3],
    [0.4, 0.5, 0.6],
    [0.7, 0.8, 0.9],
  ]


@pytest.fixture
def mock_gemini():
  service = MagicMock()
  service.generate = AsyncMock(return_value="AI response")
  return service


@pytest.fixture
def mock_embedding():
  service = MagicMock()
  service.generate_query_embedding = AsyncMock(
    return_value=[0.1, 0.2, 0.3]
  )
  service.generate_embeddings = AsyncMock(
    return_value=[[0.1, 0.2, 0.3]]
  )
  return service

@pytest.fixture
def mock_qdrant():
  service = MagicMock()
  service.search.return_value = [
    {
      "text": "Karun knows FastAPI",
      "score": 0.95,
      "chunk_index": 0,
    }
  ]
  service.create_collection.return_value = None
  service.store_embeddings.return_value = None
  return service

@pytest.fixture
def prompt_service():
  return PromptService()

@pytest.fixture
def chunking_service():
  return ChunkingService()