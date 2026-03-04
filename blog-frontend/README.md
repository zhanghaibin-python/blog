# Blog Frontend

基于 Vue 3 + Vite + Element Plus 构建的博客系统前端项目。

## 🛠 技术栈

- **框架**: [Vue 3](https://vuejs.org/) (Composition API)
- **构建工具**: [Vite](https://vitejs.dev/)
- **状态管理**: [Pinia](https://pinia.vuejs.org/)
- **路由**: [Vue Router 4](https://router.vuejs.org/)
- **UI 组件库**: [Element Plus](https://element-plus.org/)
- **HTTP 请求**: [Axios](https://axios-http.com/)
- **CSS 预处理**: Sass (可选)

## 📂 项目结构

```
src/
 ├─ api/           # 后端接口封装 (Auth, Articles, Users, Categories)
 ├─ assets/        # 静态资源 (CSS, Images)
 ├─ components/    # 公共组件
 ├─ layout/        # 布局组件 (MainLayout)
 ├─ router/        # 路由配置 (路由守卫)
 ├─ stores/        # Pinia 状态管理 (Auth Store)
 ├─ utils/         # 工具函数 (Axios 拦截器)
 ├─ views/         # 页面组件 (Home, Login, Register, Article...)
 ├─ App.vue        # 根组件
 └─ main.js        # 入口文件
```

## 🚀 快速开始

### 1. 安装依赖

确保已安装 Node.js (推荐 v16+)。

```bash
cd blog-frontend
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

默认运行在 `http://localhost:5173`。

### 3. 构建生产版本

```bash
npm run build
```

构建产物位于 `dist/` 目录。

## 🔌 接口对接说明

### 后端配置
本项目默认配置代理连接本地 Django 后端。
- **目标后端地址**: `http://localhost:8000`
- **API 前缀**: `/api/v1`

### 代理配置
在 `vite.config.js` 中配置了开发环境代理：

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

如果后端地址发生变化，请修改此配置。

### 认证机制
- 使用 **JWT** 认证。
- 登录成功后，Token 存储在 `localStorage` (`access_token`, `refresh_token`)。
- Axios 请求拦截器自动在 Header 中携带 `Authorization: Bearer <token>`。
- Axios 响应拦截器自动处理 `401` 状态码并跳转至登录页。

## 📝 环境变量

如需区分环境变量，可在根目录创建 `.env` 文件：

```properties
# .env
VITE_API_BASE_URL=/api/v1
```

(注：当前项目直接在 `request.js` 中硬编码了 baseURL 为 `/api/v1` 以匹配代理，如需生产环境直接访问完整 URL，请修改 `src/utils/request.js`)。

## 📦 部署

构建完成后，将 `dist/` 目录下的文件部署到 Nginx 或其他静态文件服务器。

Nginx 配置示例：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/dist;
        index index.html;
        try_files $uri $uri/ /index.html; # 支持 History 模式路由
    }

    location /api {
        proxy_pass http://localhost:8000; # 转发 API 请求到后端
    }
}
```
