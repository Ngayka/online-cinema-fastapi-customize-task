import asyncio
from celery import shared_task
from config.dependencies import get_settings
from notifications.emails import EmailSender


@shared_task(name="tasks.send_activation_email_task")
def send_activation_email_task(email: str, activation_link: str) -> None:
    """
    Celery task (SYNC entrypoint).
    Celery cannot run async directly, so we bootstrap an event loop
    and call the real async email sender.
    """
    async def _send():
        settings = get_settings()

        sender = EmailSender(
            hostname=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            email=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            template_dir=settings.PATH_TO_EMAIL_TEMPLATES_DIR,
            activation_email_template_name=settings.ACTIVATION_EMAIL_TEMPLATE_NAME,
            activation_complete_email_template_name=settings.ACTIVATION_COMPLETE_EMAIL_TEMPLATE_NAME,
            password_email_template_name=settings.PASSWORD_RESET_TEMPLATE_NAME,
            password_complete_email_template_name=settings.PASSWORD_RESET_COMPLETE_TEMPLATE_NAME,
            payment_confirmation_template_name=settings.PAYMENT_CONFIRMATION_TEMPLATE_NAME,
        )
        await sender.send_activation_email(email, activation_link)
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        loop.create_task(_send())
    else:
        asyncio.run(_send())
