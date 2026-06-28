from fastapi import FastAPI
from app.api.v1.health import router as health_router
from app.api.v1.chat import router as chat_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers

app = FastAPI(
  title=settings.app_name,
  version=settings.app_version,
  description="Production-ready AI Portfolio Backend",
)

register_exception_handlers(app)

app.include_router(health_router)
app.include_router(chat_router)

@app.get("/", tags=["Root"])
async def root():
  return {
    "message": f"Welcome to {settings.app_name}"
  }