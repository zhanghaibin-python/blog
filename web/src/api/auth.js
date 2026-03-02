import request from '@/utils/request'


// 登录接口
export function login(data) {
    return request({
        url: '/auth/login/',
        method: 'post',
        data
    })
}


// 获取用户信息
export function getUserInfo() {
    return request({
        url: '/users/me/',
        method: 'get'
    })
}


// 注册接口
export function register(data) {
    return request({
        url: '/users/',
        method: 'post',
        data
    })
}

