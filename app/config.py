"""
Application configuration module.
Handles environment variables and application settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database configuration
    # PostgreSQL connection string (update in .env file)
    # For quick testing, using SQLite. Change to PostgreSQL in .env file
    DATABASE_URL: str = "sqlite:///./hrms.db"
    
    # Application settings
    APP_NAME: str = "HRMS Lite API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # CORS settings (can be "*" or comma-separated list)
    CORS_ORIGINS: str = "*"
    
    # Pydantic v2 configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )
    
    def get_cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into a list."""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
settings = Settings()
