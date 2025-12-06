from collections.abc import Sequence

from config import get_settings
from src.talentgate.email.client import EmailClient

settings = get_settings()


def load_template(file: str) -> str:
    with open(file, encoding="utf-8") as f:
        return f.read()


def send_email(
    email_client: EmailClient,
    subject: str | None = None,
    body: str | None = None,
    html: str | None = None,
    context: dict | None = None,
    from_addr: str | None = None,
    to_addrs: str | Sequence[str] | None = None,
) -> None:
    body = body.format(**context)
    html = html.format(**context)

    email_client.send_email(subject=subject, body=body, html=html, from_addr=from_addr, to_addrs=to_addrs)
