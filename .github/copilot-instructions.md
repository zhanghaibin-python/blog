# Copilot Instructions for blog_project

## 项目架构概览
- 后端采用 Django + Django REST Framework，分为 `users`（用户）、`articles`（文章）、`util`（工具/渲染/异常）等模块，主配置在 `blogs/`。
- 前端为 Vue3 + Vite，代码在 `frontent/`，与后端通过 API 通信。
- Redis 用于缓存和 Celery 异步任务队列，相关配置见 `blogs/settings.py`。
- MySQL 为主数据库，连接参数通过环境变量和 `.env` 文件管理。

## 关键开发流程
- 后端开发：
  - 启动开发服务器：`python manage.py runserver`
  - 数据库迁移：`python manage.py makemigrations` + `python manage.py migrate`
  - 启动 Celery worker：`celery -A blogs worker -l info -P eventlet`
  - Redis 必须本地运行，端口 6379。
- 前端开发：
  - 进入 `frontent/`，使用 Vite 相关命令（如 `npm run dev`）。

## 重要约定与模式
- 文章相关 API 使用分离的读写序列化器（见 `articles/serializers.py`），并通过自定义权限（`IsAuthorOrReadOnly`）和分页器控制访问。
- 文章详情接口结合 Redis 实现高效阅读量统计与缓存（见 `articles/views.py`），定期通过 Celery 任务同步到数据库（见 `articles/tasks.py`）。
- 所有 API 响应统一采用 `{code, msg, data}` 格式（见 `util/renderers.py`），异常处理自定义（见 `util/exceptions.py`）。
- 分类 slug 自动转拼音并唯一（见 `articles/models.py`）。
- 采集脚本通过 Playwright 自动化采集 StackOverflow 内容（见 `articles/management/BlogCrawly.py`）。

## 目录与文件参考
- 后端主入口：`manage.py`，配置：`blogs/settings.py`
- 文章业务：`articles/`（models、views、serializers、tasks、permissions）
- 用户业务：`users/`（models、views、serializers）
- 工具/通用：`util/`（renderers、exceptions）
- 前端入口：`frontent/`

## 其他说明
- 环境变量通过 `.env` 文件管理，需包含数据库和 SECRET_KEY。
- 依赖包统一在 `requirements.txt`（后端）和 `package.json`（前端）管理。
- 代码风格以简洁、分层、可扩展为主，优先使用 Django/DRF 推荐模式。

---
如需补充特殊约定或遇到不明确的流程，请在此文档下方补充说明。
