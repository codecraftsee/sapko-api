from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "sqlite:///./sapko.db"
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    allowed_origins: str = "http://localhost:4200,https://sapko.vercel.app"
    frontend_url: str = "http://localhost:4200"

    resend_api_key: str = ""
    email_from: str = "noreply@sapko.rs"

    upload_dir: str = "./uploads"

    supabase_url: str = ""
    supabase_key: str = ""
    supabase_bucket: str = "sapko"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
