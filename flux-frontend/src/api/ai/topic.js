import request from '@/utils/request'

export function listTopic(query) {
  return request({
    url: '/ai/topic/list',
    method: 'get',
    params: query
  })
}

export function getTopic(topicId) {
  return request({
    url: '/ai/topic/' + topicId,
    method: 'get'
  })
}

export function addTopic(data) {
  return request({
    url: '/ai/topic',
    method: 'post',
    data: data
  })
}

export function updateTopic(data) {
  return request({
    url: '/ai/topic',
    method: 'put',
    data: data
  })
}

export function delTopic(topicId) {
  return request({
    url: '/ai/topic/' + topicId,
    method: 'delete'
  })
}
