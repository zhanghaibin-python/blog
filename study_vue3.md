# 1. 创建项目
npm create vite@latest web -- --template vue

# 2. 进入目录
cd web

# 3. 安装核心依赖
# axios: 发请求
# vue-router: 路由跳转
# pinia: 状态管理 (Vuex 的替代者，Vue3 官方推荐)
# element-plus: 饿了么出品的 UI 库 (国内实习必备)
# sass: CSS 预处理器 (方便写样式)
npm install axios vue-router pinia element-plus sass


src/
├── api/            # 存放接口定义 (API 契约层) -> 重点！不要把 URL 散落在页面里
├── assets/         # 静态资源 (图片、css)
├── components/     # 公共组件 (Button, Card 等)
├── router/         # 路由配置
├── stores/         # 状态管理 (Pinia)
├── utils/          # 工具函数 (Axios 封装在这里)
├── views/          # 页面文件 (Login.vue, ArticleList.vue)
├── App.vue         # 根组件
└── main.js         # 入口文件