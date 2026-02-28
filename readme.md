# 项目环境搭建

# 一、后端环境搭建

## 1. 创建虚拟环境：
python -m venv venv

## 2. 进入虚拟环境
venv\Scripts\activate

## 3. 安装所需得软件包(requiremwnts.txt)
执行 pip install -r requirements.txt 安装requirements.txt

## 4. 执行数据库迁移
创建数据迁移\
python manage.py makemigrations\
执行数据迁移\
python manage.py migrate

## 5. 启动后端
python manage.py runserver

## 6. redis 配置

必须先安装: pip install django-redis


# 7. 配置 redis 缓存 + 配置 celery 异步任务队列 + 配置 django-celery-beat 定时任务队列

## 7.1 配置 redis 缓存
在 settings.py 中添加如下配置：
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # 1 表示使用 Redis 的数据库 1
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

## 7.2 配置 celery 异步任务队列
在 settings.py 中添加如下配置：
```python
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/2'  # 使用 Redis 数据库 2 作为消息队列
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/3'  # 使用 Redis 数据库 3 存储任务结果
```
windows 下 启动 celery 异步任务队列：
celery -A blogs worker -l info -P eventlet



# 二、前端环境搭建









