import request from '@/utils/request'

export function listKnowledgeItem(query) {
  return request({
    url: '/ai/knowledge-item/list',
    method: 'get',
    params: query
  })
}

export function getKnowledgeItem(knowledgeItemId) {
  return request({
    url: '/ai/knowledge-item/' + knowledgeItemId,
    method: 'get'
  })
}

export function addKnowledgeItem(data) {
  return request({
    url: '/ai/knowledge-item',
    method: 'post',
    data: data
  })
}

export function updateKnowledgeItem(data) {
  return request({
    url: '/ai/knowledge-item',
    method: 'put',
    data: data
  })
}

export function delKnowledgeItem(knowledgeItemId) {
  return request({
    url: '/ai/knowledge-item/' + knowledgeItemId,
    method: 'delete'
  })
}
