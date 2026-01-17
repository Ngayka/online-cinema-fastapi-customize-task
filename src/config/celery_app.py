import os
from celery import Celery # type: ignore
from celery.schedules import crontab
from config.dependencies import get_settings


settings = get_settings()

celery_app = Celery(
    main="online_movie", broker=settings.REDIS_URL, backend=settings.REDIS_URL
)

if os.environ.get("TESTING") == "True":
    celery_app.conf.update(
        task_always_eager=True,
        task_eager_propagates=True
    )
celery_app.conf.imports = [
    "tasks.email_tasks",
    "tasks.cleanup_tasks",
]
celery_app.conf.broker_connection_retry_on_startup = True
celery_app.autodiscover_tasks(["tasks"], related_name="email_tasks")
celery_app.autodiscover_tasks(["tasks"], related_name="cleanup_tasks")

celery_app.conf.beat_schedule = {
    "cleanup_expired_tokens_every_24_hours": {
        "task": "tasks.cleanup_task.cleanup_expired_tokens",
        "schedule": crontab(minute=59, hour=23),
    }
}
