import { defineStore } from 'pinia'
import {ref} from "vue";
import { login, getUserInfo } from '@/api/auth'



// 'user' 是 store 的唯一 ID
export const useUserStore =
    defineStore('user', () => {
        // 1. State(状态) - 相当于 data
        // 从 localStorage 初始化 token, 实现刷新不丢失
        const token = ref(localStorage.getItem('token') || '')
        const user = ref({})

         // 2. Actions (动作) - 相当于methods
        // 登录动作
        const loginAction =
            async (loginForm) => {
            try {
                const res = await login(loginForm)
                token.value = res.access
                // 持久化保存 Token
                localStorage.setItem('token', res.access)
                return true
            } catch (error) {
                return false
            }
        }

        // 获取用户信息
        const getUserInfoAction = async () => {
            try {
                const res = await getUserInfo()
                user.value = res
            } catch (error) {
                console.error('获取用户信息失败', error)
            }
        }


        // 退出登录
        const logout = () => {
            token.value = ''
            user.value = {}
            localStorage.removeItem('token')
        }

        // 3. 导出给组件使用
        return { token, user, loginAction,
        getUserInfoAction, logout}
    })

