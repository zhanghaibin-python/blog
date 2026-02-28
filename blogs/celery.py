import os
from celery import Celery


# 设置环境变量
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'blogs.settings'
)

app = Celery('blogs')

# 使用 django 的 settings 文件配置 celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现 task
app.autodiscover_tasks()

