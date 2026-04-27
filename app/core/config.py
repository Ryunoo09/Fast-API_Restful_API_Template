from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    """

    # Project Info
    PROJECT_NAME: str = "FastAPI Blog - Chapter 3"
    PROJECT_DESCRIPTION: str = "RESTful Blog API migrated from PHP Chapter 3 to FastAPI"
    VERSION: str = "1.0.0"

    # API
    API_V1_STR: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Database (MySQL)
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USERNAME: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "blog"

    @property
    def DATABASE_URL(self) -> str:
        """Construct MySQL connection string from individual parameters."""
        return (
            f"mysql+pymysql://{self.DB_USERNAME}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
