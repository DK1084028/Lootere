import os
from celery import Celery
from celery.schedules import crontab

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("lootere_worker", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    beat_schedule={
        "enrich-tmdb-every-15m": {
            "task": "worker.tasks.tmdb_sync.enrich_missing_tmdb_metadata_task",
            "schedule": crontab(minute="*/15"),
        }
    }
)
