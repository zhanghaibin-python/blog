import { createRouter, createWebHistory } from "vue-router";


// 路由表
const routes = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/Login.vue'), // 懒加载
        meta: { title: '登录' }
    },
    {
        path: '/',
        name: 'Home',
        component: () => import('@/views/Home.vue'),    // 懒加载
        meta: { title: '首页' }
    }
]

const router = createRouter({
    history: createWebHistory(), // 使用 HTML5 History 模式
    routes
})

// 路由守卫
// 作用：没有登录就不让访问首页
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    // 如果要去的地方不是登录页，且没有 Token
    if (to.path !== '/login' && !token) {
        next('/login')  // 强制跳回登录页
    } else {
        next()  // 放行
    }
})


export default router