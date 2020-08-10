
import os

from celery import Celery

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_meiduo.settings.dev")

celery_app = Celery('drf_meiduo')
celery_app.config_from_object('celery_tasks.config')
celery_app.autodiscover_tasks([
    'celery_tasks.email',       # 自动加载email文件中的任务
])