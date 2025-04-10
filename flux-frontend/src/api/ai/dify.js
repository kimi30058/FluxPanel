import request from '@/utils/request'

export function sendChat(providerId, data) {
  return request({
    url: `/ai/dify/chat?provider_id=${providerId}`,
    method: 'post',
    data: data
  })
}

export function sendChatStream(providerId, data) {
  return request({
    url: `/ai/dify/chat/stream?provider_id=${providerId}`,
    method: 'post',
    data: data,
    responseType: 'text',
    transformResponse: [data => data]  // 不要将响应转换为JSON
  })
}

export function createChat(data) {
  return request({
    url: '/ai/dify/chats',
    method: 'post',
    data: data
  })
}

export function getUserChats(query) {
  return request({
    url: '/ai/dify/chats',
    method: 'get',
    params: query
  })
}

export function sendMessageToChat(chatId, data) {
  return request({
    url: `/ai/dify/chats/${chatId}/messages`,
    method: 'post',
    data: data
  })
}

export function getChatMessages(chatId, query) {
  return request({
    url: `/ai/dify/chats/${chatId}/messages`,
    method: 'get',
    params: query
  })
}

export function deleteChat(chatId) {
  return request({
    url: `/ai/dify/chats/${chatId}`,
    method: 'delete'
  })
}

export function renameChat(chatId, data) {
  return request({
    url: `/ai/dify/chats/${chatId}/title`,
    method: 'put',
    data: data
  })
}
