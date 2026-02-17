
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','Blog.settings')
celery_app = Celery('celery')
celery_app.config_from_object('django.conf:settings' , namespace = 'CELERY')

celery_app.autodiscover_tasks()
