import os

from django.conf import settings
from django.core.cache import cache
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery("backend")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task
def set_cache(key, value):
    try:
        cache.set(key, value, timeout=settings.TOKEN_EXPIRED_TIME * 60)
    except Exception as ex:
        raise ex


@app.task
def delete_local_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)