import anyio
from fastapi import Depends
from starlette.templating import Jinja2Templates
from celery import shared_task

from notifications import EmailSenderInterface
from config.dependencies import get_settings, get_accounts_email_notificator


settings = get_settings()
email_sender: EmailSenderInterface = Depends(get_accounts_email_notificator)
templates = Jinja2Templates(directory=settings.templates_dir)


@shared_task
def send_confirmation_email(recipient_email: str, token: str) -> None:
    """Send activation email asynchronously."""
    activation_link = f"{settings.FRONTEND_URL}/auth/activate?token={token}"

    async def _send():
        await email_sender.send_activation_email(
                email=recipient_email,
                activation_link=activation_link
        )
    try:
        anyio.run(_send)
        print(f"Successfully send activation letter for {recipient_email}")

    except Exception as e:
        print(f"CELERY_TASK failed! Error sending email to {recipient_email}: {e}")
        raise
