from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Professional VPN Panel"
    APP_ENV: str = "production"
    DEBUG: bool = False
    
    # Security
    JWT_SECRET: str = "super-secret-change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:***@localhost:5432/vpn_db"
    REDIS_URL: str = "redis://redis.railway.internal:6379/0"
    
    # Railway / Network
    PUBLIC_DOMAIN: Optional[str] = None
    PORT: int = 8080
    CORS_ORIGINS: list[str] = ["*"]
    
    # VPN / Protocols
    DEFAULT_TRAFFIC_LIMIT: int = 100 * 1024 * 1024 * 1024 # 100 GB
    DEFAULT_EXPIRATION_DAYS: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
