from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    sentry_dsn: str
    google_api_key: str
    LOGFIRE_TOKEN: str
    model_config = SettingsConfigDict(env_file=".env")
