import request from '@/utils/request'

export interface AIApp {
  id: number;
  app_name: string;
  app_type: string;
  description?: string;
  icon?: string;
  icon_bg_color?: string;
  tags?: string[];
  system_prompt?: string;
  max_context_turns?: number;
  max_tokens?: number;
  preserve_system_prompt?: boolean;
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface AIProvider {
  id: number;
  name: string;
  provider: string;
  api_key: string;
  base_url?: string;
  available_models?: string[];
  config?: Record<string, any>;
  is_active: boolean;
}

export interface DifyApp {
  id: number;
  api_key: string;
  app_id: string;
  api_base?: string;
  conversation_mode?: string;
  response_mode?: string;
  is_active: boolean;
}

export interface CozeApp {
  id: number;
  api_key: string;
  workflow_id?: string;
  agent_id?: string;
  config?: Record<string, any>;
  is_active: boolean;
}

export function getAIAppList(params?: any) {
  return request({
    url: '/ai/provider/application/list',
    method: 'get',
    params
  })
}

export function getAIAppById(id: number) {
  return request({
    url: `/ai/provider/application/${id}`,
    method: 'get'
  })
}

export function createAIApp(data: any) {
  return request({
    url: '/ai/provider/application/create',
    method: 'post',
    data
  })
}

export function updateAIApp(id: number, data: any) {
  return request({
    url: `/ai/provider/application/${id}`,
    method: 'put',
    data
  })
}

export function updateAppContextSettings(id: number, data: any) {
  return request({
    url: `/ai/provider/application/${id}/context`,
    method: 'put',
    data
  })
}

export function getAppContextSettings(id: number) {
  return request({
    url: `/ai/provider/application/${id}/context`,
    method: 'get'
  })
}

export function deleteAIApp(id: number) {
  return request({
    url: `/ai/provider/application/${id}`,
    method: 'delete'
  })
}

export function getTraditionalProviderList(params?: any) {
  return request({
    url: '/ai/provider/traditional/list',
    method: 'get',
    params
  })
}

export function getTraditionalProviderById(id: number) {
  return request({
    url: `/ai/provider/traditional/${id}`,
    method: 'get'
  })
}

export function createTraditionalProvider(data: any) {
  return request({
    url: '/ai/provider/traditional/create',
    method: 'post',
    data
  })
}

export function updateTraditionalProvider(id: number, data: any) {
  return request({
    url: `/ai/provider/traditional/${id}`,
    method: 'put',
    data
  })
}

export function deleteTraditionalProvider(id: number) {
  return request({
    url: `/ai/provider/traditional/${id}`,
    method: 'delete'
  })
}

export function getDifyAppList(params?: any) {
  return request({
    url: '/ai/provider/dify/list',
    method: 'get',
    params
  })
}

export function getDifyAppById(id: number) {
  return request({
    url: `/ai/provider/dify/${id}`,
    method: 'get'
  })
}

export function createDifyApp(data: any) {
  return request({
    url: '/ai/provider/dify/create',
    method: 'post',
    data
  })
}

export function updateDifyApp(id: number, data: any) {
  return request({
    url: `/ai/provider/dify/${id}`,
    method: 'put',
    data
  })
}

export function deleteDifyApp(id: number) {
  return request({
    url: `/ai/provider/dify/${id}`,
    method: 'delete'
  })
}

export function getCozeAppList(params?: any) {
  return request({
    url: '/ai/provider/coze/list',
    method: 'get',
    params
  })
}

export function getCozeAppById(id: number) {
  return request({
    url: `/ai/provider/coze/${id}`,
    method: 'get'
  })
}

export function createCozeApp(data: any) {
  return request({
    url: '/ai/provider/coze/create',
    method: 'post',
    data
  })
}

export function updateCozeApp(id: number, data: any) {
  return request({
    url: `/ai/provider/coze/${id}`,
    method: 'put',
    data
  })
}

export function deleteCozeApp(id: number) {
  return request({
    url: `/ai/provider/coze/${id}`,
    method: 'delete'
  })
}

export function getChatList(params?: any) {
  return request({
    url: '/ai/chat/list',
    method: 'get',
    params
  })
}

export function getChatById(id: number) {
  return request({
    url: `/ai/chat/${id}`,
    method: 'get'
  })
}

export function createChat(data: any) {
  return request({
    url: '/ai/chat/create',
    method: 'post',
    data
  })
}

export function renameChat(id: number, data: any) {
  return request({
    url: `/ai/chat/${id}/rename`,
    method: 'put',
    data
  })
}

export function deleteChat(id: number) {
  return request({
    url: `/ai/chat/${id}`,
    method: 'delete'
  })
}

export function getChatMessages(id: number, params?: any) {
  return request({
    url: `/ai/chat/${id}/messages`,
    method: 'get',
    params
  })
}

export function sendChatMessage(id: number, data: any) {
  return request({
    url: `/ai/chat/${id}/message`,
    method: 'post',
    data
  })
}

export function getModelProviders() {
  return request({
    url: '/ai/model-runtime/providers',
    method: 'get'
  })
}

export function getModelsByProviderAndType(provider: string, modelType: string) {
  return request({
    url: `/ai/model-runtime/models/${provider}/${modelType}`,
    method: 'get'
  })
}

export function validateProviderCredentials(data: any) {
  return request({
    url: '/ai/model-runtime/credentials/validate',
    method: 'post',
    data
  })
}

export function estimateTokenUsage(data: any) {
  return request({
    url: '/ai/token/estimate',
    method: 'post',
    data
  })
}

export function formatMessagesForModel(data: any) {
  return request({
    url: '/ai/token/format-messages',
    method: 'post',
    data
  })
}

export function invokeLLM(data: any) {
  return request({
    url: '/ai/model-invoke/llm',
    method: 'post',
    data
  })
}

export function invokeEmbedding(data: any) {
  return request({
    url: '/ai/model-invoke/embedding',
    method: 'post',
    data
  })
}

export function invokeRerank(data: any) {
  return request({
    url: '/ai/model-invoke/rerank',
    method: 'post',
    data
  })
}

export function invokeSpeechToText(data: any) {
  return request({
    url: '/ai/model-invoke/speech-to-text',
    method: 'post',
    data
  })
}

export function invokeTextToSpeech(data: any) {
  return request({
    url: '/ai/model-invoke/text-to-speech',
    method: 'post',
    data
  })
}

export function invokeModeration(data: any) {
  return request({
    url: '/ai/model-invoke/moderation',
    method: 'post',
    data
  })
}
