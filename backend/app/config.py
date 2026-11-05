import os
from pydantic_settings import BaseSettings

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_DB_PATH = os.path.join(PROJECT_ROOT, "data", "quickcommerce.db").replace("\\", "/")

class Settings(BaseSettings):
    PROJECT_NAME: str = "QuickCommerce Intelligence"
    API_V1_STR: str = "/api"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{DEFAULT_DB_PATH}"
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "quickcommerce-intelligence-secret-key-2026")
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
