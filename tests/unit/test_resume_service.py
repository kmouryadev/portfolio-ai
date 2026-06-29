from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core.exceptions import AppException
from app.services.resume_service import ResumeService


class TestResumeService:
    @pytest.mark.asyncio
    @patch("app.services.resume_service.extract_text_from_pdf")
    @patch("pathlib.Path.write_bytes")
    async def test_upload_resume_success(
        self,
        mock_write_bytes,
        mock_extract_text,
    ):
        upload_file = MagicMock()
        upload_file.filename = "resume.pdf"
        upload_file.content_type = "application/pdf"
        upload_file.read = AsyncMock(return_value=b"dummy pdf")
        chunking_service = MagicMock()
        chunking_service.split_text.return_value = [
            "chunk one",
            "chunk two",
        ]
        embedding_service = MagicMock()
        embedding_service.generate_embeddings = AsyncMock(
            return_value=[
                [0.1, 0.2],
                [0.3, 0.4],
            ]
        )
        qdrant_service = MagicMock()

        mock_extract_text.return_value = "Resume text extracted"
        service = ResumeService(
            chunking_service=chunking_service,
            embedding_service=embedding_service,
            qdrant_service=qdrant_service,
        )
        response = await service.upload_resume(upload_file)

        assert response.original_filename == "resume.pdf"
        upload_file.read.assert_awaited_once()

        mock_write_bytes.assert_called_once()

        mock_extract_text.assert_called_once()

        chunking_service.split_text.assert_called_once()

        embedding_service.generate_embeddings.assert_awaited_once()

        qdrant_service.create_collection.assert_called_once()

        qdrant_service.store_embeddings.assert_called_once()

    @pytest.mark.asyncio
    async def test_upload_resume_invalid_file_type(self):
        upload_file = MagicMock()
        upload_file.filename = "resume.txt"
        upload_file.content_type = "text/plain"
        chunking_service = MagicMock()
        embedding_service = MagicMock()
        qdrant_service = MagicMock()
        service = ResumeService(
            chunking_service,
            embedding_service,
            qdrant_service,
        )

        with pytest.raises(AppException):
            await service.upload_resume(upload_file)
