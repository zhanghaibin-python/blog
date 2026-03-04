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
    method: 'get'
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

// 更新文章
export function updateArticle(id, data) {
  return request({
    url: `/articles/${id}/`,
    method: 'patch',
    data
  })
}
