import request from '@/utils/request'

export function listKnowledgeBase(query) {
  return request({
    url: '/ai/knowledge-base/list',
    method: 'get',
    params: query
  })
}

export function getKnowledgeBase(knowledgeBaseId) {
  return request({
    url: '/ai/knowledge-base/' + knowledgeBaseId,
    method: 'get'
  })
}

export function addKnowledgeBase(data) {
  return request({
    url: '/ai/knowledge-base',
    method: 'post',
    data: data
  })
}

export function updateKnowledgeBase(data) {
  return request({
    url: '/ai/knowledge-base',
    method: 'put',
    data: data
  })
}

export function delKnowledgeBase(knowledgeBaseId) {
  return request({
    url: '/ai/knowledge-base/' + knowledgeBaseId,
    method: 'delete'
  })
}
