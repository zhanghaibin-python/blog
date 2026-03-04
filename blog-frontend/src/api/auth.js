import request from '@/utils/request'

// 登录
export function login(data) {
  return request({
    url: '/auth/login/',
    method: 'post',
    data
  })
}

// 注册 (文档归类为 Users 模块，但在逻辑上属于认证)
export function register(data) {
  return request({
    url: '/users/',
    method: 'post',
    data
  })
}

// 获取当前用户信息
export function getInfo() {
  return request({
    url: '/users/me/',
    method: 'get'
  })
}

// 退出登录
export function logout(refreshToken) {
  return request({
    url: '/auth/logout/',
    method: 'post',
    data: {
      refresh: refreshToken
    }
  })
}
