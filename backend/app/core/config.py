from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    debug: bool = True

    database_url: str
    sync_database_url: str

    frontend_url: str = "http://localhost:5173"

    api_prefix: str = "/api"


settings = Settings()  # pyright: ignore[reportCallIssue]
