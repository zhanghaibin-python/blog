import request from '@/utils/request'

// 获取文章列表
export function getArticles(params) {
  return request({
    url: '/articles/',
    method: 'get',
    params
  })
}

// 获取文章详情
export function getArticle(id) {
  return request({
    url: `/articles/${id}/`,
    method: 'get',
    params: { _t: new Date().getTime() } // 添加时间戳参数，强制浏览器不使用缓存
  })
}

// 创建文章
export function createArticle(data) {
  return request({
    url: '/articles/',
    method: 'post',
    data
  })
}

// 删除文章
export function deleteArticle(id) {
  return request({
    url: `/articles/${id}/`,
    method: 'delete'
  })
}

// 更新文章
export function updateArticle(id, data) {
  return request({
    url: `/articles/${id}/`,
    method: 'patch',
    data
  })
}
