from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])
chat_service = ChatService()

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
  return await chat_service.send_message(request.message)