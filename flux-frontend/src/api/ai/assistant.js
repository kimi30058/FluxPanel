import request from '@/utils/request'

export function listAssistant(query) {
  return request({
    url: '/ai/assistant/list',
    method: 'get',
    params: query
  })
}

export function getAssistant(assistantId) {
  return request({
    url: '/ai/assistant/' + assistantId,
    method: 'get'
  })
}

export function addAssistant(data) {
  return request({
    url: '/ai/assistant',
    method: 'post',
    data: data
  })
}

export function updateAssistant(data) {
  return request({
    url: '/ai/assistant',
    method: 'put',
    data: data
  })
}

export function delAssistant(assistantId) {
  return request({
    url: '/ai/assistant/' + assistantId,
    method: 'delete'
  })
}
