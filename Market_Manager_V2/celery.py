import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Market_Manager_V2.settings')

app = Celery('Market_Manager_V2')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
