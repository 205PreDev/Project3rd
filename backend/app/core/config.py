"""
애플리케이션 설정
"""
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """애플리케이션 설정 클래스"""

    # ===== 앱 기본 설정 =====
    PROJECT_NAME: str = "AI 이미지 생성 플랫폼"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, production

    # ===== 데이터베이스 =====
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    # PostgreSQL (Supabase)
    SUPABASE_DB_URL: Optional[str] = None

    # ===== Supabase BaaS =====
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    SUPABASE_BUCKET: str = "images"

    # ===== Redis =====
    REDIS_URL: str = "redis://localhost:6379/0"
    # Upstash (Serverless Redis for Vercel)
    UPSTASH_REDIS_URL: Optional[str] = None

    # ===== JWT 인증 =====
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7일

    # ===== AI Services =====
    # Google Gemini
    GEMINI_API_KEY: Optional[str] = None

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_ORG_ID: Optional[str] = None

    # Unsplash
    UNSPLASH_ACCESS_KEY: Optional[str] = None

    # Rembg Service
    REMBG_API_URL: str = "http://localhost:5000"  # Docker 컨테이너 또는 Render.com

    # ===== 크레딧 시스템 =====
    WELCOME_CREDITS: int = 10  # 가입 시 무료 크레딧
    CREDIT_COSTS: dict = {
        "image_generation": 1,
        "caption_generation": 0.5,
        "prompt_edit": 1,
    }

    # ===== Rate Limiting =====
    RATE_LIMIT_DAILY: int = 10  # 프롬프트 일일 사용량
    RATE_LIMIT_HOURLY: int = 3  # 프롬프트 시간당 사용량

    # ===== 파일 업로드 =====
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png"]

    # ===== CORS =====
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
    ]

    # ===== Monitoring =====
    SENTRY_DSN: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


def get_settings() -> Settings:
    """설정 인스턴스를 반환하는 함수 (FastAPI Depends 지원)"""
    return settings
