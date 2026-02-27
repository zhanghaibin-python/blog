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


# 二、前端环境搭建









