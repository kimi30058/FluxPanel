import request from '@/utils/request'

export function listModel(query) {
  return request({
    url: '/ai/model/list',
    method: 'get',
    params: query
  })
}

export function getModel(modelId) {
  return request({
    url: '/ai/model/' + modelId,
    method: 'get'
  })
}

export function addModel(data) {
  return request({
    url: '/ai/model',
    method: 'post',
    data: data
  })
}

export function updateModel(data) {
  return request({
    url: '/ai/model',
    method: 'put',
    data: data
  })
}

export function delModel(modelId) {
  return request({
    url: '/ai/model/' + modelId,
    method: 'delete'
  })
}
