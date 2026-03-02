"""
Application configuration module.
Handles environment variables and application settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # 🔹 Database configuration
    # Hardcoded for Render production deployment
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
        env_file=".env",          # Loads local .env file
        case_sensitive=True,
        extra="ignore"            # Ignore extra environment variables
    )

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