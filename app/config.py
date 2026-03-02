"""
Application configuration module.
Handles environment variables and application settings.
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # 🔹 Database configuration
    # Hardcoded for Render production deployment
    # Internal Database URL (for Render services) - no SSL needed, faster connection
    # This will be used if DATABASE_URL is not set as environment variable
    DATABASE_URL: str = "postgresql://hrms_user:AbhJkLzuoBmsUbyYd1kamVMhV00qQH6T@dpg-d6irjmsr85hc73c4tg8g-a/hrms_db_oa38"

    # 🔹 Application settings
    APP_NAME: str = "HRMS Lite API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # 🔹 CORS settings
    # For production, set this to your frontend URL
    # Example:
    # CORS_ORIGINS="https://fastapi-demo.vercel.app"
    CORS_ORIGINS: str = "*"

    # 🔹 Pydantic v2 configuration
    model_config = SettingsConfigDict(
        env_file=".env",          # Loads .env file if exists
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",           # Ignore extra environment variables
        # Priority: Environment variables > .env file > Default value
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Force use Render Internal Database URL if:
        # 1. DATABASE_URL contains "localhost" (wrong config)
        # 2. Or we're on Render (RENDER env var is set)
        # 3. Or DATABASE_URL points to localhost/127.0.0.1
        current_db_url = str(getattr(self, "DATABASE_URL", ""))
        render_db_url = "postgresql://hrms_user:AbhJkLzuoBmsUbyYd1kamVMhV00qQH6T@dpg-d6irjmsr85hc73c4tg8g-a/hrms_db_oa38"
        
        # Check if we need to override (localhost detected or on Render)
        is_localhost = ("localhost" in current_db_url.lower() or 
                       "127.0.0.1" in current_db_url or
                       "::1" in current_db_url)
        # Render sets PORT environment variable, so we can detect if we're on Render
        is_render = os.getenv("PORT") is not None or os.getenv("RENDER") is not None
        
        if is_render or is_localhost:
            # Force use Render Internal Database URL
            object.__setattr__(self, "DATABASE_URL", render_db_url)

    def get_cors_origins_list(self) -> List[str]:
        """
        Convert comma-separated CORS_ORIGINS string into a list.
        """
        if self.CORS_ORIGINS == "*":
            return ["*"]

        origins = [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]

        return origins if origins else ["*"]


# Global settings instance
settings = Settings()