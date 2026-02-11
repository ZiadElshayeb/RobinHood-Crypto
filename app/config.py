from pathlib import Path
from pydantic_settings import BaseSettings

ROOT_PATH = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):

    # postgress credentials
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = ""

    # JWT Security
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Meta Custom Automation"

    # Models APIs
    OPENAI_API_KEY: str = ""  # For OpenAI GPT-4 (alternative to Gemini)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = ""
    GEMINI_BASE_URL: str = ""

    # News APIs
    NEWS_AI_API_KEY: str = ""

    # Robinhood
    ROBINHOOD_BASE_URL: str = ""

    class Config:
        env_file = str(ROOT_PATH / ".env")
        case_sensitive = True

settings = Settings()