from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./aivoa.db"
    groq_api_key: str | None = None
    groq_model: str = "gemma2-9b-it"
    groq_fallback_model: str = "llama-3.1-8b-instant"
    ai_mock_mode: bool = False
    cors_origins: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
