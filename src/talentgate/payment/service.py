from paddle_billing import Client, Options, Environment

from config import get_settings

settings = get_settings()


def get_paddle_client() -> Client:
    return Client(
        api_key=settings.paddle_api_secret_key,
        options=Options(Environment.SANDBOX),
    )
