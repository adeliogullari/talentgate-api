import smtplib
from collections.abc import Sequence
from email.message import EmailMessage

from config import get_settings

settings = get_settings()


class EmailClient:
    def __init__(self, host: str, port: int, user: str, password: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def send_email(
        self,
        subject: str,
        body: str = None,
        html: str = None,
        from_addr: str | None = None,
        to_addrs: str | Sequence[str] | None = None,
    ):
        msg = EmailMessage()
        msg.add_header("Subject", subject)
        msg.add_header("From", from_addr)
        msg.add_header("To", to_addrs)
        msg.set_content(body)
        msg.add_alternative(html, subtype="html")

        try:
            with smtplib.SMTP(host=self.host, port=self.port) as server:
                server.starttls()
                server.login(user=self.user, password=self.password)
                server.send_message(msg=msg, from_addr=from_addr, to_addrs=to_addrs)
        except smtplib.SMTPException:
            raise


def get_email_client() -> EmailClient:
    return EmailClient(
        host=settings.smtp_host,
        port=settings.smtp_port,
        user=settings.smtp_user,
        password=settings.smtp_password,
    )
