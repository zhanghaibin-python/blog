import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      component: () => import('@/layout/MainLayout.vue'),
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/HomeView.vue')
        },
        {
          path: 'articles/create',
          name: 'article-create',
          component: () => import('@/views/ArticleCreateView.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: 'drafts',
          name: 'drafts',
          component: () => import('@/views/DraftsView.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: 'articles/:id',
          name: 'article-detail',
          component: () => import('@/views/ArticleDetailView.vue')
        },
        {
          path: 'articles/:id/edit',
          name: 'article-edit',
          component: () => import('@/views/ArticleEditView.vue'),
          meta: { requiresAuth: true }
        }
      ]
    }
  ]
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // 检查是否需要登录
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    // 如果已登录但用户信息为空，尝试获取用户信息
    if (authStore.isAuthenticated && !authStore.user) {
        try {
            await authStore.fetchUser()
        } catch (error) {
            // 获取失败（如 token 过期），已在 store 中处理了 logout
            next({ name: 'login' })
            return
        }
    }
    next()
  }
})

export default router
