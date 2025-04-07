import request from '@/utils/request';

export function getAiAppInfo(appId) {
  return request({
    url: '/ai/info',
    method: 'get',
    params: { appId }
  });
}

export function getAiAppParameters(appId) {
  return request({
    url: '/ai/parameters',
    method: 'get',
    params: { appId },
    headers: {
      'X-App-ID': appId || ''
    }
  });
}

export function getConversations(appId, params) {
  return request({
    url: '/ai/conversations',
    method: 'get',
    params,
    headers: {
      'X-App-ID': appId || ''
    }
  });
}

export function getConversationMessages(appId, conversationId) {
  return request({
    url: `/ai/chat/messages/${conversationId}`,
    method: 'get',
    headers: {
      'X-App-ID': appId || ''
    }
  });
}

export function getMoreMessages(appId, params) {
  return request({
    url: '/ai/chat/messages/history',
    method: 'get',
    params,
    headers: {
      'X-App-ID': appId || ''
    }
  });
}

export function sendChatMessage(appId, data) {
  return request({
    url: '/ai/chat/messages',
    method: 'post',
    data,
    headers: {
      'X-App-ID': appId || ''
    }
  });
}

export function renameConversation(appId, conversationId, name) {
  return request({
    url: `/ai/conversations/${conversationId}/name`,
    method: 'post',
    data: { name },
    headers: {
      'X-App-ID': appId || ''
    }
  });
}

export function deleteConversation(appId, conversationId) {
  return request({
    url: `/ai/conversations/${conversationId}`,
    method: 'delete',
    headers: {
      'X-App-ID': appId || ''
    }
  });
}

export function uploadFile(appId, file) {
  const formData = new FormData();
  formData.append('file', file);
  
  return request({
    url: '/ai/files/upload',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data',
      'X-App-ID': appId || ''
    }
  });
}
