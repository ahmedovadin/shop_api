import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')

app = Celery('shop_api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

from celery.schedules import crontab
app.conf.beat_schedule = {
    "delete unactive users": {
        "task": "users.tasks.delete_unactive_users",
        "schedule": crontab(minute="15")
    },
    'delete-old-codes-every-day': {
        'task': 'users.tasks.delete_old_confirmation_codes',
        'schedule': crontab(hour=9, minute=0),   # каждый день в 9:00
    },
}