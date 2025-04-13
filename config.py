from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgresql_schema: str
    postgresql_user: str
    postgresql_password: str
    postgresql_host: str
    postgresql_port: str
    postgresql_database: str
    minio_schema: str
    minio_host: str
    minio_port: str
    minio_root_user: str
    minio_root_password: str
    google_client_id: str
    password_hash_algorithm: str
    message_digest_algorithm: str
    access_token_expiration: float
    access_token_key: str
    access_token_algorithm: str
    access_token_type: str
    refresh_token_expiration: float
    refresh_token_key: str
    refresh_token_algorithm: str
    refresh_token_type: str

    model_config = SettingsConfigDict(
        extra="allow", env_file=".env", env_file_encoding="utf-8"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
