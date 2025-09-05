"""Configuration management for the synthetic data service."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "4000"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    OPENAI_REQUEST_TIMEOUT: int = int(os.getenv("OPENAI_REQUEST_TIMEOUT", "30"))
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_REQUESTS_PER_MINUTE", "3"))
    RATE_LIMIT_REQUESTS_PER_DAY: int = int(os.getenv("RATE_LIMIT_REQUESTS_PER_DAY", "200"))
    RATE_LIMIT_TOKENS_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_TOKENS_PER_MINUTE", "10000"))
    
    # Cache Settings
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_FILE_PATH: str = os.getenv("CACHE_FILE_PATH", "data/schemas.json")
    CACHE_BACKUP_PATH: str = os.getenv("CACHE_BACKUP_PATH", "data/schemas.json.backup")
    
    # Application Settings
    MAX_DESCRIPTION_LENGTH: int = int(os.getenv("MAX_DESCRIPTION_LENGTH", "4000"))
    MIN_DESCRIPTION_LENGTH: int = int(os.getenv("MIN_DESCRIPTION_LENGTH", "10"))
    MAX_ROWS: int = int(os.getenv("MAX_ROWS", "10000"))
    MIN_ROWS: int = int(os.getenv("MIN_ROWS", "1"))
    
    def validate_settings(self) -> None:
        """Validate required settings are present."""
        if not self.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it in your .env file or environment."
            )
        
        if not self.OPENAI_API_KEY.startswith(("sk-", "sk-proj-")):
            raise ValueError(
                "OPENAI_API_KEY appears to be invalid. "
                "It should start with 'sk-' or 'sk-proj-'"
            )


# Global settings instance
settings = Settings()