# Environment Configuration Management for DDD
# Centralized configuration service

from typing import Dict, Any
from pydantic import BaseSettings


# Base configuration class
class Config(BaseSettings):
    """Base configuration class"""

    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./furniture_webshop.db"
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Settings:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Configuration service
class ConfigService:
    """Centralized configuration service"""

    def __init__(self):
        self.config = Config()

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return getattr(self.config, key, default)

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values"""
        return self.config.dict()

    def is_debug(self) -> bool:
        """Check if debug mode is enabled"""
        return self.config.DEBUG

    def get_database_url(self) -> str:
        """Get database URL"""
        return self.config.DATABASE_URL


# Global configuration instance
config_service = ConfigService()
