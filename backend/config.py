import sys
from pathlib import Path

# Add project root to sys.path to allow absolute imports of the 'backend' package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

# Resolve .env path absolutely from the location of config.py:
# backend/config.py -> parent is backend -> parent.parent is project root (contains .env)
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

class Settings(BaseSettings):
    # Default to placeholder so server can boot and serve fallbacks without .env
    GROQ_API_KEY: str = "placeholder_key"

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Initialize settings singleton
try:
    settings = Settings()
except Exception as e:
    # Print a helpful warning for hackathon setup but allow instantiation for testing/dummy setups
    # if we run the server in a way that provides environment variables directly or we want to fallback
    print(f"Configuration Loading Warning: {e}")
    # We create a dummy settings object if we want to run tests or demo fallback,
    # but raise if not in test scenario. In actual run, Pydantic throws ValidationError.
    # We will raise it directly so it fails loudly as requested.
    raise e
