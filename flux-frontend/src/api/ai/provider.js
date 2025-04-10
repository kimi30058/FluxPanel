import request from '@/utils/request'

export function listProvider(query) {
  return request({
    url: '/ai/provider/list',
    method: 'get',
    params: query
  })
}

export function getProvider(providerId) {
  return request({
    url: '/ai/provider/' + providerId,
    method: 'get'
  })
}

export function addProvider(data) {
  return request({
    url: '/ai/provider',
    method: 'post',
    data: data
  })
}

export function updateProvider(data) {
  return request({
    url: '/ai/provider',
    method: 'put',
    data: data
  })
}

export function delProvider(providerId) {
  return request({
    url: '/ai/provider/' + providerId,
    method: 'delete'
  })
}
