"""
Configuration management using Pydantic settings loader
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from .env file"""
    
    # App Config
    APP_NAME: str = "AI_Job_Matcher"
    APP_ENV: str = "production"
    DEBUG: bool = False
    PORT: int = 8000
    BASE_URL: str = "http://localhost:8000"
    
    # Database
    DATABASE_URL: str
    
    # AI/NLP Model
    HUGGINGFACE_API_TOKEN: str
    MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384
    
    # Authentication
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Cache settings instance"""
    return Settings()
