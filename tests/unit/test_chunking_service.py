from app.services.chunking_service import ChunkingService


class TestChunkingService:
    def test_split_text_returns_list(self):
        service = ChunkingService(
            chunk_size=50,
            chunk_overlap=10,
        )
        text = "FastAPI React Next.js " * 30
        chunks = service.split_text(text)
        assert isinstance(chunks, list)
        assert len(chunks) > 1
        assert all(isinstance(chunk, str) for chunk in chunks)

    def test_split_text_preserves_content(self):
        service = ChunkingService()
        text = "Karun Mourya"
        chunks = service.split_text(text)
        assert "Karun" in chunks[0]
        assert "Mourya" in chunks[0]
