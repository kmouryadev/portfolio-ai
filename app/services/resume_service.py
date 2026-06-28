from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from starlette import status

from app.core.exceptions import AppException

UPLOAD_DIR = Path("uploads/resumes")

class ResumeService:
  """Handles resume file uploads."""

  def __init__(self) -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

  async def upload_resume(
    self,
    file: UploadFile,
  ) -> dict:
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
    return {
      "filename": filename,
      "original_filename": file.filename,
      "content_type": file.content_type,
      "size": len(content),
    }