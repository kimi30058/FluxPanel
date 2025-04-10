import request from '@/utils/request'

export function sendChat(providerId, data) {
  return request({
    url: `/ai/deepseek/chat?provider_id=${providerId}`,
    method: 'post',
    data: data
  })
}

export function sendChatStream(providerId, data) {
  return request({
    url: `/ai/deepseek/chat/stream?provider_id=${providerId}`,
    method: 'post',
    data: data,
    responseType: 'text',
    transformResponse: [data => data]  // 不要将响应转换为JSON
  })
}

export function useReasoner(providerId, data) {
  return request({
    url: `/ai/deepseek/reasoner?provider_id=${providerId}`,
    method: 'post',
    data: data
  })
}

export function saveChatHistory(data) {
  return request({
    url: '/ai/deepseek/save_chat',
    method: 'post',
    data: data
  })
}
