from google import genai

from app.core.config import settings
from app.core.exceptions import AppException
from app.core.logger import logger

class GeminiService:
  """Handles communication with Google Gemini."""
  
  def __init__(self) -> None:
    self.client = genai.Client(
      api_key=settings.google_api_key
    )
    self._model = settings.gemini_model

    async def generate(self, prompt: str) -> str:
      try:
        response = self.client.models.generate_content(
          model=settings.gemini_model,
          contents=prompt,
          )
        return response.text
      except Exception as e:
        logger.exception("Gemini request failed")
        raise AppException(
          message="Unable to generate AI response.",
          status_code=500,
        )
