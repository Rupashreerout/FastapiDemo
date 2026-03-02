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
    DATABASE_URL: str = "postgresql://postgres:admin123@localhost:5432/hrms_db"
    
    # Application settings
    APP_NAME: str = "HRMS Lite API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # CORS settings (comma-separated list of origins, or "*" for all)
    # In production, set this to your frontend URL(s)
    # Example: "https://your-app.vercel.app,https://www.yourdomain.com"
    CORS_ORIGINS: str = "*"
    
    # Pydantic v2 configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # Ignore extra environment variables
    )
    
    def get_cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into a list."""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        # Split by comma and clean up whitespace
        origins = [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        return origins if origins else ["*"]


# Global settings instance
settings = Settings()
