# skillhub/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillhub.settings')

app = Celery('skillhub')

# read config from Django settings, using namespace 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# auto-discover tasks in installed apps' tasks.py
app.autodiscover_tasks()

# optional: set default queue, serializer
app.conf.update(
    task_track_started=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)
