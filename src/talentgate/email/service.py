from collections.abc import Sequence

from config import get_settings
from src.talentgate.email.client import EmailClient

settings = get_settings()


def send_email(
    email_client: EmailClient,
    subject: str,
    body: str,
    from_addr: str | None = None,
    to_addrs: str | Sequence[str] | None = None,
):
    email_client.send_email(
        subject=subject, body=body, from_addr=from_addr, to_addrs=to_addrs
    )
