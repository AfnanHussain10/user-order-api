from pydantic_settings import BaseSettings
import os
import secrets
from dotenv import load_dotenv

# Get the absolute path of the .env file in the project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
ENV_PATH = os.path.join(BASE_DIR, ".env")

# Load environment variables from the root .env file
load_dotenv(ENV_PATH)

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "User Order API"

    # Database
    DATABASE_URL: str

    # JWT
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ENV_PATH 
        case_sensitive = True

settings = Settings()
