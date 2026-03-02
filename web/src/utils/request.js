import axios from "axios";
import {ElMessage} from "element-plus";


// 1. 创建 axios 实例
const service = axios.create({
    // 这里的 '/api' 是为了后面配置代理跨域
    baseURL: '/api/v1/',
    timeout: 5000 // 请求超时时间
})

// 2. 请求拦截器 （Request Interceptor）
// 作用：每次发请求前，自动带上 Token
service.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 3. 响应器拦截器（Response Interceptor）
// 作用：解包数据，统一处理错误
service.interceptors.response.use(
    (response) => {
        const res = response.data;
        if (res.code !== 200) {
            ElMessage.error(res.msg || '系统错误');
            // 401: 未登录或 Token 过期
            if (res.code === 401) {
                // TODO: 跳转到登录页
                localStorage.removeItem('token');
                window.location.href = '/login';
            }
            return Promise.reject(new Error(res.msg || 'Error'));
        } else {
            // 核心：只返回 data 部分，页面拿到就是纯数据
            return res.data;
        }
    }, (error) => {
        // 处理 HTTP 状态码错误（如 404，500）
        console.error('Request Error: ', error);
        ElMessage.error(error.msg || '请求失败');
        return Promise.reject(error);
    }
);


export default service;