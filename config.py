from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    frontend_base_url: str
    postgres_db: str
    postgres_schema: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    redis_host: str
    redis_port: int
    redis_username: str
    redis_password: str
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
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_email: str
    smtp_password: str
    paddle_api_secret_key: str
    paddle_api_environment: str
    paddle_standard_plan_product_id: str
    paddle_standard_plan_monthly_price_id: str
    paddle_standard_plan_annual_price_id: str
    paddle_premium_plan_product_id: str
    paddle_premium_plan_monthly_price_id: str
    paddle_premium_plan_annual_price_id: str

    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
