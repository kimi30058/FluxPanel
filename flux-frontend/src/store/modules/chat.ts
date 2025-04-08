import { defineStore } from 'pinia'
import { 
  getChatList, 
  getChatMessages, 
  createChat, 
  sendChatMessage,
  deleteChat,
  renameChat
} from '@/api/ai'
import type { ChatMessage, ChatSession } from '@/types/chat'

export enum AIProvider {
  DIFY = 'dify',
  COZE = 'coze',
  TRADITIONAL = 'traditional'
}

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [] as ChatMessage[],
    chatHistory: [] as ChatSession[],
    currentChatId: '',
    isLoadingMessage: false,
    hasMoreMessages: false,
    currentProvider: AIProvider.DIFY,
    messageOffset: 0,
    messageLimit: 20
  }),
  
  actions: {
    setProvider(provider: AIProvider) {
      this.currentProvider = provider
    },
    
    clearMessages() {
      this.messages = []
      this.messageOffset = 0
      this.hasMoreMessages = false
    },
    
    async fetchChatHistory(params: any = {}) {
      try {
        const { data } = await getChatList(params)
        if (data && Array.isArray(data.list)) {
          this.chatHistory = data.list.map((item: any) => ({
            id: item.id.toString(),
            title: item.title,
            lastTime: item.updated_at,
            app_id: item.app_id,
            user_id: item.user_id,
            system_prompt: item.system_prompt
          }))
          return this.chatHistory
        }
        return []
      } catch (error) {
        console.error('获取聊天历史失败:', error)
        return []
      }
    },
    
    async fetchChatMessages(params: any) {
      try {
        this.isLoadingMessage = true
        const chatId = params.chat_id
        
        if (!chatId) {
          throw new Error('聊天ID不能为空')
        }
        
        this.currentChatId = chatId.toString()
        
        const { data } = await getChatMessages(chatId, {
          limit: params.limit || this.messageLimit,
          offset: params.offset || 0
        })
        
        if (data && Array.isArray(data.list)) {
          this.messages = data.list.map((item: any) => ({
            id: item.id,
            role: item.role,
            content: item.content,
            content_type: item.content_type || 'text',
            created_at: item.created_at
          }))
          
          this.hasMoreMessages = data.total > this.messages.length
          this.messageOffset = this.messages.length
          
          return this.messages
        }
        
        return []
      } catch (error) {
        console.error('获取聊天消息失败:', error)
        return []
      } finally {
        this.isLoadingMessage = false
      }
    },
    
    async fetchMoreMessages() {
      if (!this.currentChatId || !this.hasMoreMessages) return
      
      try {
        const { data } = await getChatMessages(parseInt(this.currentChatId), {
          limit: this.messageLimit,
          offset: this.messageOffset
        })
        
        if (data && Array.isArray(data.list) && data.list.length > 0) {
          const moreMessages = data.list.map((item: any) => ({
            id: item.id,
            role: item.role,
            content: item.content,
            content_type: item.content_type || 'text',
            created_at: item.created_at
          }))
          
          this.messages = [...moreMessages, ...this.messages]
          this.messageOffset += moreMessages.length
          this.hasMoreMessages = data.total > this.messageOffset
        } else {
          this.hasMoreMessages = false
        }
      } catch (error) {
        console.error('加载更多消息失败:', error)
      }
    },
    
    async createChat(params: any) {
      try {
        const { data } = await createChat(params)
        
        if (data) {
          this.currentChatId = data.id.toString()
          
          await this.fetchChatHistory()
          
          return data
        }
        
        throw new Error('创建聊天会话失败')
      } catch (error) {
        console.error('创建聊天会话失败:', error)
        throw error
      }
    },
    
    async sendMessage(params: any) {
      if (!this.currentChatId) {
        throw new Error('当前没有选中的聊天会话')
      }
      
      try {
        this.isLoadingMessage = true
        
        const userMessage: ChatMessage = {
          id: `temp-${Date.now()}`,
          role: 'user',
          content: params.content,
          content_type: params.content_type || 'text',
          file_name: params.file_name,
          created_at: new Date().toISOString()
        }
        
        this.messages.push(userMessage)
        
        const { data } = await sendChatMessage(parseInt(this.currentChatId), {
          content: params.content,
          content_type: params.content_type || 'text',
          file_name: params.file_name
        })
        
        if (data && data.user_message && data.assistant_message) {
          const userIndex = this.messages.findIndex(m => m.id === userMessage.id)
          if (userIndex !== -1) {
            this.messages[userIndex] = {
              id: data.user_message.id,
              role: 'user',
              content: data.user_message.content,
              content_type: data.user_message.content_type || 'text',
              file_name: data.user_message.file_name,
              created_at: data.user_message.created_at
            }
          }
          
          this.messages.push({
            id: data.assistant_message.id,
            role: 'assistant',
            content: data.assistant_message.content,
            content_type: data.assistant_message.content_type || 'text',
            created_at: data.assistant_message.created_at
          })
        }
        
        return data
      } catch (error) {
        console.error('发送消息失败:', error)
        throw error
      } finally {
        this.isLoadingMessage = false
      }
    },
    
    async deleteChat(chatId: number) {
      try {
        await deleteChat(chatId)
        
        if (this.currentChatId === chatId.toString()) {
          this.clearMessages()
          this.currentChatId = ''
        }
        
        await this.fetchChatHistory()
        
        return true
      } catch (error) {
        console.error('删除聊天会话失败:', error)
        throw error
      }
    },
    
    async renameChat(chatId: number, title: string) {
      try {
        await renameChat(chatId, { title })
        
        await this.fetchChatHistory()
        
        return true
      } catch (error) {
        console.error('重命名聊天会话失败:', error)
        throw error
      }
    },
    
    async sendMessageFeedback(messageId: string | number, rating: string | null) {
      try {
        console.log('发送消息反馈:', messageId, rating)
        return true
      } catch (error) {
        console.error('发送消息反馈失败:', error)
        throw error
      }
    }
  }
})
