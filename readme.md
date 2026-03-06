# 个人博客系统 (后端)

基于 **Django + DRF + Redis + Celery** 构建的高性能博客后端系统。

## 🛠 技术栈
- **核心框架**: Python 3.10+, Django 4.2+, Django REST Framework
- **数据库**: MySQL 8.0
- **缓存与消息队列**: Redis 6.0+
- **异步任务**: Celery + Eventlet (Windows适配)
- **认证**: SimpleJWT

## 🚀 快速开始

### 1. 环境准备
确保本地已安装 Python 3.10+、MySQL 8.0+ 和 Redis 服务。

### 2. 创建虚拟环境
```bash
python -m venv venv
# Windows 激活
venv\Scripts\activate
# Linux/Mac 激活
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```
> **注意**: Windows 下运行 Celery 需要安装 `eventlet`。

### 4. 环境变量配置
在项目根目录新建 `.env` 文件，填入以下配置：
```ini
SECRET_KEY=你的DjangoSecretKey
NAME=blog_db
USER=root
PASSWORD=你的数据库密码
HOST=127.0.0.1
```

### 5. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 创建超级用户
```bash
python manage.py createsuperuser
```

### 7. 启动服务

#### 7.1 启动 Django 后端
```bash
python manage.py runserver
```

#### 7.2 启动 Celery Worker (异步任务)
用于处理阅读量异步落库等后台任务。
```bash
# Windows (必须加 -P eventlet) 
# 先执行
celery -A blogs worker -l info -P eventlet  # 添加一个工人负责执行redis中的任务
# 在执行
celery -A blogs beat -l info    # 启动模式：发送一个指令告诉 worker 该干活了

```

#### 7.3 启动 Celery Beat (定时任务)
用于定时触发 Redis 数据同步到 MySQL。
```bash
celery -A blogs beat -l info
```

---

## 🔧 核心配置说明

### Redis 缓存配置 (settings.py)
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Celery 配置 (settings.py)
```python
# Broker (消息中间件)
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/2'
# Result Backend (结果存储)
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/3'
```

---

## 🧪 测试
运行单元测试以确保功能正常：
```bash
python manage.py test articles
```

## 📝 接口文档
启动服务后，访问 `http://127.0.0.1:8000/api/v1/` 查看接口列表。
