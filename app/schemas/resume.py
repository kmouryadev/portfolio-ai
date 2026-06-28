from pydantic import BaseModel

class ResumeUploadResponse(BaseModel):
  filename: str
  original_filename: str
  content_type: str
  size: int
  pages: int
  