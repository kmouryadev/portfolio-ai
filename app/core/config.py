from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="AI Portfolio API")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=True)

    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000)

    google_api_key: str = Field(default="")
    gemini_model: str = Field(default="gemini-2.5-flash")
    embedding_model: str = Field(default="gemini-embedding-001")

    qdrant_url: str | None = Field(default=None)
    qdrant_api_key: str | None = Field(default=None)
    qdrant_host: str = Field(default="localhost")
    qdrant_port: int = Field(default=6333)
    collection_name: str = Field(default="portfolio_resume")

    jwt_secret_key: str = Field(default="change-this-in-production")
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60)

    admin_username: str = Field(default="admin")
    admin_password_hash: str = Field(default="")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
