"""
Provide implementation of settings.
"""

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    debug: bool = False
    jwt_secret: str = 'jwt_secret'
    access_token_life_time: int = 15 * 60  # 15 minutes
    refresh_token_life_time: int = 60 * 60 * 24 * 30  # 30 days

    postgres_host: str = 'auth-service-postgres'
    postgres_db: str = 'postgres'
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'
    database_log_queries: bool = False
    database_pool_timeout: int = 30
    database_pool_max_size: int = 10

    password_min_length: int = 8

    model_config = SettingsConfigDict(
        frozen=True,
        env_file='.env',
        extra='ignore',
    )

    @property
    def database_url(self) -> str:
        return (
            f'postgresql://{self.postgres_user}:{self.postgres_password}'
            f'@{self.postgres_host}:5432/{self.postgres_db}'
        )

    @property
    def async_database_url(self) -> str:
        return self.database_url.replace('postgresql://', 'postgresql+asyncpg://')


settings = Settings()
