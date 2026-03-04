import { defineStore } from 'pinia'
import { login, logout, getInfo, register } from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access_token') || '',
    refreshToken: localStorage.getItem('refresh_token') || '',
    isAuthenticated: !!localStorage.getItem('access_token')
  }),

  actions: {
    async login(username, password) {
      try {
        const res = await login({ username, password })
        // res 是 { message, refresh, access }
        // 注意：request.js 拦截器已经处理了 code !== 200 的情况，并返回了 data
        
        this.accessToken = res.access
        this.refreshToken = res.refresh
        this.isAuthenticated = true
        
        localStorage.setItem('access_token', res.access)
        localStorage.setItem('refresh_token', res.refresh)
        
        // 登录成功后获取用户信息
        await this.fetchUser()
        
        return res
      } catch (error) {
        throw error
      }
    },

    async register(username, password) {
      try {
        const res = await register({ username, password })
        return res
      } catch (error) {
        throw error
      }
    },

    async fetchUser() {
      try {
        const res = await getInfo()
        // res 是 { username: "..." }
        this.user = res
      } catch (error) {
        // 获取用户信息失败，可能 token 失效
        this.logout()
      }
    },

    async logout() {
      try {
        if (this.refreshToken) {
            await logout(this.refreshToken)
        }
      } catch (error) {
        console.error('Logout error', error)
      } finally {
        this.user = null
        this.accessToken = ''
        this.refreshToken = ''
        this.isAuthenticated = false
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      }
    }
  }
})
