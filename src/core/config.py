"""Configuration management for the synthetic data service."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # API Provider Selection
    API_PROVIDER: str = os.getenv("API_PROVIDER", "openai").lower()  # "openai" or "anthropic"

    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "4000"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    OPENAI_REQUEST_TIMEOUT: int = int(os.getenv("OPENAI_REQUEST_TIMEOUT", "30"))

    # Anthropic Configuration
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")
    ANTHROPIC_MAX_TOKENS: int = int(os.getenv("ANTHROPIC_MAX_TOKENS", "4096"))
    ANTHROPIC_TEMPERATURE: float = float(os.getenv("ANTHROPIC_TEMPERATURE", "0.7"))

    # General API Settings
    API_REQUEST_TIMEOUT: int = int(os.getenv("API_REQUEST_TIMEOUT", "30"))
    
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

    # Demo/Test Mode (allows running without OpenAI API key)
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "false").lower() == "true"

    def validate_settings(self) -> None:
        """Validate required settings are present."""
        # Skip API key validation in demo mode
        if self.DEMO_MODE:
            return

        # Validate API provider selection
        if self.API_PROVIDER not in ["openai", "anthropic"]:
            raise ValueError(
                f"API_PROVIDER must be 'openai' or 'anthropic', got '{self.API_PROVIDER}'"
            )

        # Validate appropriate API key based on provider
        if self.API_PROVIDER == "openai":
            if not self.OPENAI_API_KEY:
                raise ValueError(
                    "OPENAI_API_KEY environment variable is required when API_PROVIDER=openai. "
                    "Please set it in your .env file or environment. "
                    "Or set DEMO_MODE=true to test without an API key."
                )

            if not self.OPENAI_API_KEY.startswith(("sk-", "sk-proj-")):
                raise ValueError(
                    "OPENAI_API_KEY appears to be invalid. "
                    "It should start with 'sk-' or 'sk-proj-'"
                )

        elif self.API_PROVIDER == "anthropic":
            if not self.ANTHROPIC_API_KEY:
                raise ValueError(
                    "ANTHROPIC_API_KEY environment variable is required when API_PROVIDER=anthropic. "
                    "Please set it in your .env file or environment. "
                    "Or set DEMO_MODE=true to test without an API key."
                )

            if not self.ANTHROPIC_API_KEY.startswith("sk-ant-"):
                raise ValueError(
                    "ANTHROPIC_API_KEY appears to be invalid. "
                    "It should start with 'sk-ant-'"
                )


# Global settings instance
settings = Settings()