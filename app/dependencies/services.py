from app.services.auth_service import AuthService
from app.services.chat_service import ChatService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.gemini_service import GeminiService
from app.services.prompt_service import PromptService
from app.services.qdrant_service import QdrantService
from app.services.resume_service import ResumeService


def get_auth_service() -> AuthService:
    return AuthService()


def get_qdrant_service() -> QdrantService:
    return QdrantService()


def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()


def get_chunking_service() -> ChunkingService:
    return ChunkingService()


def get_resume_service() -> ResumeService:
    return ResumeService(
        chunking_service=get_chunking_service(),
        embedding_service=get_embedding_service(),
        qdrant_service=get_qdrant_service(),
    )


def get_prompt_service() -> PromptService:
    return PromptService()


def get_gemini_service() -> GeminiService:
    return GeminiService()


def get_chat_service() -> ChatService:
    return ChatService(
        gemini_service=get_gemini_service(),
        prompt_service=get_prompt_service(),
        embedding_service=get_embedding_service(),
        qdrant_service=get_qdrant_service(),
    )
