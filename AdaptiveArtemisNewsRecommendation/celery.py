from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AdaptiveArtemisNewsRecommendation.settings')

app = Celery('your_project_name')

# Django settings config Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discovery and loading task.py
app.autodiscover_tasks()
