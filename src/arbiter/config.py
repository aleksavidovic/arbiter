from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    pg_dsn: PostgresDsn = PostgresDsn(
            "postgresql+asyncpg://arbiter:arbiter_dev_password@localhost:5432/arbiter_db"
    )
    redis_dsn: RedisDsn = RedisDsn(
            "redis://localhost:6379/0"
    )

settings = Settings()
