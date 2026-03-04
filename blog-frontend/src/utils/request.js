import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const service = axios.create({
  baseURL: '/api/v1', // 使用代理，指向 /api/v1
  timeout: 5000 // 请求超时时间
})

// request 拦截器
service.interceptors.request.use(
  config => {
    // 从 localStorage 获取 token
    const token = localStorage.getItem('access_token')
    if (token) {
      // 如果存在 token，则添加到请求头
      // 格式：Authorization: Bearer <token>
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    // 请求错误处理
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response 拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    
    // 根据后端约定，code === 200 代表成功
    if (res.code !== 200) {
      ElMessage({
        message: res.msg || 'Error',
        type: 'error',
        duration: 5 * 1000
      })

      // 401: 未登录或 Token 过期
      if (res.code === 401) {
        // 清除 token 并跳转登录页
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        // 这里可以使用 router 跳转，或者直接 reload
        window.location.reload()
      }
      return Promise.reject(new Error(res.msg || 'Error'))
    } else {
      // 如果 code === 200，直接返回 data 字段（业务数据）
      // 注意：有些接口可能没有 data 字段，或者 data 是 null
      return res.data
    }
  },
  error => {
    console.log('err' + error) // for debug
    let message = error.message
    if (error.response) {
       // 处理 HTTP 状态码错误
       if (error.response.status === 401) {
         message = '未授权，请重新登录'
         localStorage.removeItem('access_token')
         localStorage.removeItem('refresh_token')
         window.location.href = '/login' // 强制跳转
       } else if (error.response.status === 403) {
         message = '拒绝访问'
       } else if (error.response.status === 404) {
         message = '请求资源不存在'
       } else if (error.response.status === 500) {
         message = '服务器内部错误'
       }
       // 如果后端返回了错误信息结构，优先使用
       if (error.response.data && error.response.data.msg) {
         message = error.response.data.msg
       }
    }
    
    ElMessage({
      message: message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
