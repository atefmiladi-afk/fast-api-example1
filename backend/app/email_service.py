import logging
import smtplib
from email.message import EmailMessage

from app.config import settings

logger = logging.getLogger("deutsch.email")


def send_email(to_email: str, subject: str, text_body: str) -> None:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.smtp_from
    message["To"] = to_email
    message.set_content(text_body)

    if not settings.smtp_host:
        logger.warning("SMTP not configured. Email to %s:\n%s\n%s", to_email, subject, text_body)
        print(f"[EMAIL DEV] to={to_email} subject={subject}\n{text_body}")
        return

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=20) as smtp:
        if settings.smtp_tls:
            smtp.starttls()
        if settings.smtp_user:
            smtp.login(settings.smtp_user, settings.smtp_password)
        smtp.send_message(message)


def send_verification_email(to_email: str, token: str) -> None:
    link = f"{settings.frontend_url.rstrip('/')}/verify-email?token={token}"
    send_email(
        to_email,
        "Verify your Deutsch Lernen account",
        f"Willkommen!\n\nPlease confirm your email by opening this link:\n{link}\n\nThis link expires in 24 hours.",
    )


def send_reset_email(to_email: str, token: str) -> None:
    link = f"{settings.frontend_url.rstrip('/')}/reset-password?token={token}"
    send_email(
        to_email,
        "Reset your Deutsch Lernen password",
        f"We received a request to reset your password.\n\nOpen this link to choose a new password:\n{link}\n\nThis link expires in 1 hour. If you did not request this, ignore the email.",
    )
