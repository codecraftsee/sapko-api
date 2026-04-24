import secrets
import logging
import resend
from datetime import datetime, timedelta
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

VERIFICATION_TOKEN_EXPIRE_HOURS = 24


def send_email(to: str, subject: str, body: str) -> None:
    if not settings.resend_api_key:
        logger.info(f"[email stub] To: {to} | Subject: {subject}\n{body}")
        return

    resend.api_key = settings.resend_api_key
    resend.Emails.send({
        "from": settings.email_from,
        "to": [to],
        "subject": subject,
        "text": body,
    })


def generate_verification_token() -> tuple[str, datetime]:
    token = secrets.token_urlsafe(64)
    expires_at = datetime.utcnow() + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)
    return token, expires_at


def send_verification_email(to: str, token: str) -> None:
    link = f"{settings.frontend_url}/verify-email?token={token}"
    subject = "Potvrdite vašu email adresu — Šapko"
    body = (
        f"Zdravo,\n\n"
        f"Hvala što ste se registrovali na Šapko platformi.\n\n"
        f"Molimo vas da potvrdite vašu email adresu klikom na link ispod:\n\n"
        f"{link}\n\n"
        f"Link važi 24 sata.\n\n"
        f"Ako se niste registrovali na Šapko, ignorišite ovu poruku.\n\n"
        f"— Tim Šapko"
    )
    send_email(to=to, subject=subject, body=body)
