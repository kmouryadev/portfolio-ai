from fastapi import APIRouter, Depends, File, UploadFile

from app.dependencies.services import get_resume_service
from app.schemas.resume import ResumeUploadResponse
from app.services.resume_service import ResumeService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

@router.post(
    "/resume/upload",
    response_model=ResumeUploadResponse,
)
async def upload_resume(
  file: UploadFile = File(...),
  service: ResumeService = Depends(get_resume_service),
):
  return await service.upload_resume(file)