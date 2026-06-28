from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from starlette import status

from app.core.exceptions import AppException
from app.core.logger import logger
from app.schemas.resume import ResumeUploadResponse
from app.utils.pdf import extract_text_from_pdf

UPLOAD_DIR = Path("uploads/resumes")

class ResumeService:
  """Handles resume file uploads."""

  def __init__(self) -> None:
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
    logger.info(
      "Resume uploaded successfully. Extracted %d characters.",
      len(extracted_text),
      )

    return ResumeUploadResponse(
      filename=filename,
      original_filename=file.filename,
      content_type=file.content_type,
      size=len(content),
      pages=extracted_text.count("\f") + 1,
    )