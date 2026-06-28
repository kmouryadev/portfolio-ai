from fastapi import FastAPI
from app.api.v1.health import router as health_router

app = FastAPI(
  title="AI Portfolio API",
  description="Production-ready AI Portfolio Backend",
  version="1.0.0",
)

app.include_router(health_router)

@app.get("/", tags=["Root"])
async def root():
  return {
    "message": "Welcome to AI Portfolio API"
  }