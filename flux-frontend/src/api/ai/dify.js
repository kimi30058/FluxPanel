import request from '@/utils/request'

export function sendChatMessage(data) {
  return request({
    url: '/api/ai/dify/chat',
    method: 'post',
    data: data,
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

export function sendStreamChatMessage(data) {
  return request({
    url: '/api/ai/dify/chat/stream',
    method: 'post',
    data: data,
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

export function createChat(data) {
  return request({
    url: '/api/ai/dify/chats',
    method: 'post',
    data: data,
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

export function getUserChats(query) {
  return request({
    url: '/api/ai/dify/chats',
    method: 'get',
    params: query
  })
}

export function sendMessageToChat(chatId, data) {
  return request({
    url: `/api/ai/dify/chats/${chatId}/messages`,
    method: 'post',
    data: data,
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

export function getChatMessages(chatId, query) {
  return request({
    url: `/api/ai/dify/chats/${chatId}/messages`,
    method: 'get',
    params: query
  })
}

export function deleteChat(chatId) {
  return request({
    url: `/api/ai/dify/chats/${chatId}`,
    method: 'delete'
  })
}

export function renameChat(chatId, data) {
  return request({
    url: `/api/ai/dify/chats/${chatId}/title`,
    method: 'put',
    data: data
  })
}
