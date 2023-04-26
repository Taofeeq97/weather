from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weatherupdate.settings')

app = Celery('weatherupdate')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_weather_mail': {
        'task': 'api.tasks.send_weather_mail',
        'schedule': timedelta(days=1, hours=6),
        'args': (),
    },
}