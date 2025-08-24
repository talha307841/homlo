"""
Configuration settings for Homlo API
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Homlo API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str
    DATABASE_TEST_URL: Optional[str] = None
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_TEST_URL: Optional[str] = None
    
    # MinIO
    MINIO_ROOT_USER: str = "homlo"
    MINIO_ROOT_PASSWORD: str = "homlo123"
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_BUCKET_NAME: str = "homlo-assets"
    MINIO_SECURE: bool = False
    
    # SMS
    SMS_PROVIDER: str = "twilio"
    SMS_ACCOUNT_SID: Optional[str] = None
    SMS_AUTH_TOKEN: Optional[str] = None
    SMS_FROM_NUMBER: Optional[str] = None
    
    # Email
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1025
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = False
    SMTP_FROM_EMAIL: str = "noreply@homlo.pk"
    
    # Payment Gateways
    EASYPAISA_API_KEY: Optional[str] = None
    EASYPAISA_API_SECRET: Optional[str] = None
    EASYPAISA_SANDBOX: bool = True
    
    JAZZCASH_API_KEY: Optional[str] = None
    JAZZCASH_API_SECRET: Optional[str] = None
    JAZZCASH_SANDBOX: bool = True
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    ALLOWED_DOCUMENT_TYPES: List[str] = ["application/pdf", "image/jpeg", "image/png"]
    
    # Security
    SECURE_COOKIES: bool = False
    SESSION_COOKIE_SECURE: bool = False
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "lax"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Timezone
    TIMEZONE: str = "Asia/Karachi"
    
    # Celery
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    
    @validator("CELERY_BROKER_URL", pre=True, always=True)
    def set_celery_broker_url(cls, v, values):
        if v is None:
            return values.get("REDIS_URL")
        return v
    
    @validator("CELERY_RESULT_BACKEND", pre=True, always=True)
    def set_celery_result_backend(cls, v, values):
        if v is None:
            return values.get("REDIS_URL")
        return v
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("ALLOWED_IMAGE_TYPES", "ALLOWED_DOCUMENT_TYPES", pre=True)
    def parse_list_types(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create settings instance
settings = Settings()


# Development overrides
if settings.DEBUG:
    settings.CORS_ORIGINS.extend([
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ])
