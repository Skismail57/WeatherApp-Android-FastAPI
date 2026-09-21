from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="Weather Platform API", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=True, description="Debug mode")

    database_url: str = Field(default="", description="Database connection URL")

    cors_origins_str: str = Field(
        default="http://localhost:5173", description="Comma-separated list of allowed CORS origins"
    )

    @property
    def cors_origins(self) -> list[str]:
        """Parse CORS origins string into a list."""
        return [origin.strip() for origin in self.cors_origins_str.split(",") if origin.strip()]

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str, info) -> str:
        """Validate database URL is present in non-debug mode."""
        if not v and not info.data.get("debug", True):
            raise ValueError("DATABASE_URL is required in production mode")
        return v

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


settings = Settings()
