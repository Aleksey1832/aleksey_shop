import os
from celery import Celery
from dotenv import load_dotenv


load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')

app = Celery('djangoProject1')

# Switching to Redis
app.conf.broker_url = os.getenv('CELERY_BROKER_URL')
app.conf.result_backend = os.getenv('CELERY_RESULT_BACKEND')

app.config_from_object('django.conf:settings', namespace='CELERY')
# app.conf.worker_pool = 'fork'
app.conf.worker_pool = 'solo'
app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()
