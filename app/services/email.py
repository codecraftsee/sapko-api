import smtplib
import logging
from email.mime.text import MIMEText
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


def send_email(to: str, subject: str, body: str) -> None:
    if not settings.smtp_user or not settings.smtp_password:
        logger.info(f"[email stub] To: {to} | Subject: {subject}\n{body}")
        return

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from
    msg["To"] = to

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        server.sendmail(settings.smtp_from, [to], msg.as_string())
