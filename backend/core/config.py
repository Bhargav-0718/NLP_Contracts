# backend/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://contract_user:contract_pass@localhost/contract_db"
    UPLOAD_DIR: str = "uploads"
    REPORT_DIR: str = "reports"

    class Config:
        env_file = ".env"

settings = Settings()
