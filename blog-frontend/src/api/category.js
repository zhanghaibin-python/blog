import request from '@/utils/request'

// 获取分类列表
export function getCategories() {
  return request({
    url: '/category/',
    method: 'get'
  })
}
