from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from starlette import status

from app.core.exceptions import AppException
from app.core.logger import logger
from app.schemas.resume import ResumeUploadResponse
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService
from app.utils.pdf import extract_text_from_pdf

UPLOAD_DIR = Path("uploads/resumes")


class ResumeService:
    """Handles resume file uploads."""

    def __init__(
        self,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
        qdrant_service: QdrantService,
    ) -> None:
        self._chunking_service = chunking_service
        self._embedding_service = embedding_service
        self._qdrant_service = qdrant_service
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    async def upload_resume(
        self,
        file: UploadFile,
    ) -> ResumeUploadResponse:
        if file.content_type != "application/pdf":
            raise AppException(
                message="Only PDF files are allowed.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        extension = Path(file.filename).suffix
        filename = f"{uuid4()}{extension}"
        destination = UPLOAD_DIR / filename
        content = await file.read()
        destination.write_bytes(content)
        extracted_text = extract_text_from_pdf(destination)
        chunks = self._chunking_service.split_text(extracted_text)
        logger.info(
            "Generated %d chunks.",
            len(chunks),
        )
        embeddings = await self._embedding_service.generate_embeddings(chunks)
        self._qdrant_service.create_collection(vector_size=len(embeddings[0]))
        self._qdrant_service.store_embeddings(
            chunks,
            embeddings,
        )
        logger.info(
            "Stored %d vectors in Qdrant.",
            len(chunks),
        )
        logger.info(
            "Generated %d embeddings.",
            len(embeddings),
        )
        logger.info(
            "Embedding dimension: %d",
            len(embeddings[0]) if embeddings else 0,
        )
        return ResumeUploadResponse(
            filename=filename,
            original_filename=file.filename,
            content_type=file.content_type,
            size=len(content),
            pages=extracted_text.count("\f") + 1,
        )
