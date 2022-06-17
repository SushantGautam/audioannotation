from __future__ import unicode_literals, absolute_import
import os
from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audioan.settings')

app = Celery('audioan')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))