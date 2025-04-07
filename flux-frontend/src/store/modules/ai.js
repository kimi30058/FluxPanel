import { defineStore } from 'pinia';
import request from '@/utils/request';

export const useAiStore = defineStore('ai', {
  state: () => ({
    appId: null,
    appInfo: null,
    appParameters: null,
    userInputs: {},
    userInputFormCache: {},
    showUserInputForm: false,
    showUserInputFormCancelBtn: false,
    messages: [],
    conversationHistory: [],
    currentConversationId: null,
    isLoadingMessage: false,
    isMessagesLoading: false,
    hasMoreHistory: false,
    lastId: null,
    firstMessageId: null,
    hasMoreMessages: false,
    isLoadingHistory: true,
    messageCache: new Map(),
    uploadingFiles: [],
    isUploading: false,
    generatedContent: null,
    currentMessageId: null,
    completionSavedList: [],
    type: 'chat'
  }),

  getters: {
    isNewConversation() {
      if (!this.currentConversationId) {
        if (this.appParameters?.openingStatement) {
          return this.messages.length <= 1;
        }
        return this.messages.length === 0;
      }
      return false;
    },
    openingStatement() {
      return this.appParameters?.openingStatement || '';
    },
    currentApp() {
      if (!this.appId) return null;
      return null; // 需要实现应用配置
    },
    enableFileUpload() {
      return this.appParameters?.fileUpload?.enabled || false;
    },
    allowedFileTypes() {
      return this.appParameters?.fileUpload?.allowedFileTypes || [];
    },
    fileInputAccept() {
      return this.getInputAccept(this.appParameters?.fileUpload?.allowedFileTypes || []);
    },
    fileInputLimit() {
      return this.appParameters?.fileUpload?.numberLimits || 1;
    },
    userInputForm() {
      return this.appParameters?.userInputForm || [];
    },
    hasConfigInputs() {
      return !!this.appParameters?.userInputForm?.length;
    },
    userInputFormList() {
      const list = [];
      
      this.userInputForm.forEach((field) => {
        Object.entries(field).forEach(([key, value]) => {
          if (value && typeof value === 'object') {
            value.type = value.type || key;
            list.push(value);
          }
        });
      });
      
      return list;
    }
  },

  actions: {
    async initAiApp() {
      this.isLoadingApp = true;
      
      try {
        if (this.type === 'chat') {
          await Promise.all([
            this.fetchAppInfo(),
            this.loadConversations(),
            this.initConversationMessages(),
            this.initParameters()
          ]);
        } else if (this.type === 'completion') {
          await Promise.all([
            this.fetchAppInfo(),
            this.initParameters()
          ]);
        }
      } catch (error) {
        console.error('Error initializing AI app:', error);
        this.isLoadingApp = false;
      } finally {
        this.isLoadingApp = false;
      }
    },

    async fetchAppInfo() {
      if (!this.appId) return;
      
      try {
        const response = await request({
          url: '/ai/info',
          method: 'get',
          params: {
            appId: this.appId
          }
        });
        
        this.appInfo = response.data;
      } catch (error) {
        console.error('Error fetching app info:', error);
        ElMessage.error('获取应用信息失败: ' + (error.message || '无法获取应用信息'));
      }
    },

    async loadConversations(loadMore = false) {
      if (this.type === 'completion') return;
      
      this.isLoadingHistory = true;
      
      try {
        const params = {
          limit: 20,
          ...(loadMore && this.lastId ? { lastId: this.lastId } : {})
        };
        
        const response = await request({
          url: '/ai/conversations',
          method: 'get',
          params,
          headers: {
            'X-App-ID': this.appId || ''
          }
        });
        
        const data = response.data;
        
        if (loadMore) {
          this.conversationHistory = [
            ...this.conversationHistory,
            ...data.data
          ];
        } else {
          this.conversationHistory = data.data;
        }
        
        this.hasMoreHistory = data.hasMore;
        this.lastId = data.data[data.data.length - 1]?.id || null;
      } catch (error) {
        console.error('Error loading conversations:', error);
      } finally {
        this.isLoadingHistory = false;
      }
    },

    async initConversationMessages() {
      if (this.type === 'completion') return;
      
      const conversationId = null; // 需要从路由获取
      if (conversationId) {
        await this.getMessages(conversationId);
      }
    },

    async initParameters() {
      if (!this.appId) return;
      
      try {
        const response = await request({
          url: '/ai/parameters',
          method: 'get',
          params: {
            appId: this.appId
          },
          headers: {
            'X-App-ID': this.appId || ''
          }
        });
        
        this.appParameters = response.data;
        
        this.showUserInputForm = this.isNewConversation && this.hasConfigInputs;
        
        if (this.isNewConversation && this.appParameters.openingStatement) {
          this.addMessage({
            id: Date.now().toString(),
            content: this.appParameters.openingStatement,
            isBot: true,
            isOpeningStatement: true
          });
        }
      } catch (error) {
        console.error('Error fetching app parameters:', error);
        ElMessage.error('获取应用参数失败: ' + (error.message || '无法获取应用参数'));
      }
    },

    addMessage(message) {
      this.messages.push(message);
    },

    clearMessages() {
      this.messages = [];
      this.currentConversationId = null;
      this.uploadingFiles = [];
      this.userInputs = {};
      this.userInputFormCache = {};
      this.showUserInputForm = false;
      this.showUserInputFormCancelBtn = false;
    },

    setAppId(appId) {
      this.appId = appId;
    },

    setType(type) {
      this.type = type;
    },

    async sendMessage(content) {
      if (!content.trim()) return;
      
      try {
        const userMessage = {
          id: Date.now().toString(),
          content,
          isBot: false,
          files: this.uploadingFiles.length > 0 ? [...this.uploadingFiles] : undefined
        };
        this.addMessage(userMessage);
        
        this.isLoadingMessage = true;
        
        const botMessageId = (Date.now() + 1).toString();
        const botMessage = {
          id: botMessageId,
          content: '',
          isBot: true
        };
        this.addMessage(botMessage);
        
        const files = this.uploadingFiles.map((file) => {
          return {
            type: file.type,
            transferMethod: file.url ? 'remoteUrl' : 'localFile',
            ...(file.url ? { url: file.url } : { uploadFileId: file.uploadFileId })
          };
        });
        
        const response = await request({
          url: '/ai/chat/messages',
          method: 'post',
          headers: {
            'X-App-ID': this.appId || ''
          },
          data: {
            query: content,
            responseMode: 'streaming',
            conversationId: this.currentConversationId || undefined,
            autoGenerateName: true,
            files: files.length > 0 ? files : undefined,
            inputs: this.userInputs || {}
          }
        });
        
        if (response.data) {
          const messageIndex = this.messages.findIndex(m => m.id === botMessageId);
          if (messageIndex !== -1) {
            this.messages[messageIndex].content = response.data.answer || '';
          }
          
          if (response.data.conversationId) {
            this.currentConversationId = response.data.conversationId;
          }
          
          if (response.data.files && messageIndex !== -1) {
            this.messages[messageIndex].files = response.data.files;
          }
        }
        
        this.clearUploadedFiles();
        
        if (this.isNewConversation) {
          this.loadConversations();
        }
      } catch (error) {
        console.error('Error sending message:', error);
        
        const lastMessage = this.messages[this.messages.length - 1];
        if (lastMessage?.isBot && lastMessage?.content === '') {
          this.messages.pop();
        }
        
        this.addMessage({
          id: Date.now().toString(),
          content: error.message || '抱歉，发生了错误，请稍后重试。',
          isBot: true,
          error: true
        });
        
        ElMessage.error('消息发送失败: ' + (error.message || '消息发送失败，请稍后重试'));
      } finally {
        this.isLoadingMessage = false;
      }
    },

    startNewConversation() {
      this.clearMessages();
      setTimeout(() => {
        this.showUserInputForm = this.hasConfigInputs;
        if (this.appParameters?.openingStatement) {
          this.addMessage({
            id: Date.now().toString(),
            content: this.appParameters.openingStatement,
            isBot: true
          });
        }
      });
    },

    async getMessages(conversationId) {
      if (!conversationId) return;
      
      this.isMessagesLoading = true;
      this.currentConversationId = conversationId;
      
      if (this.messageCache.has(conversationId)) {
        const cache = this.messageCache.get(conversationId);
        this.messages = cache.messages;
        this.firstMessageId = cache.firstMessageId;
        this.hasMoreMessages = cache.hasMoreMessages;
        this.isMessagesLoading = false;
        return;
      }
      
      try {
        const response = await request({
          url: `/ai/chat/messages/${conversationId}`,
          method: 'get',
          headers: {
            'X-App-ID': this.appId || ''
          }
        });
        
        this.messages = response.data.data || [];
        this.hasMoreMessages = response.data.hasMore;
        this.firstMessageId = this.messages[0]?.id || null;
        
        this.messageCache.set(conversationId, {
          messages: this.messages,
          firstMessageId: this.firstMessageId,
          hasMoreMessages: this.hasMoreMessages
        });
      } catch (error) {
        console.error('Error fetching messages:', error);
        ElMessage.error('获取消息失败: ' + (error.message || '无法获取消息'));
      } finally {
        this.isMessagesLoading = false;
      }
    },

    async fetchMessages(fetchMore = false) {
      if (!this.currentConversationId) return;
      
      try {
        const params = {
          conversationId: this.currentConversationId,
          ...(fetchMore && this.firstMessageId ? { firstId: this.firstMessageId } : {})
        };
        
        const response = await request({
          url: '/ai/chat/messages/history',
          method: 'get',
          params,
          headers: {
            'X-App-ID': this.appId || ''
          }
        });
        
        if (fetchMore) {
          this.messages = [...response.data.data, ...this.messages];
          this.firstMessageId = response.data.data[0]?.id || this.firstMessageId;
        } else {
          this.messages = response.data.data;
          this.firstMessageId = response.data.data[0]?.id || null;
        }
        
        this.hasMoreMessages = response.data.hasMore;
        
        this.messageCache.set(this.currentConversationId, {
          messages: this.messages,
          firstMessageId: this.firstMessageId,
          hasMoreMessages: this.hasMoreMessages
        });
        
        return response.data;
      } catch (error) {
        console.error('Error fetching more messages:', error);
        ElMessage.error('获取更多消息失败: ' + (error.message || '无法获取更多消息'));
        return null;
      }
    },

    async renameConversation(conversationId, name) {
      if (!conversationId || !name) return;
      
      try {
        await request({
          url: `/ai/conversations/${conversationId}/name`,
          method: 'post',
          data: { name },
          headers: {
            'X-App-ID': this.appId || ''
          }
        });
        
        const index = this.conversationHistory.findIndex(c => c.id === conversationId);
        if (index !== -1) {
          this.conversationHistory[index].name = name;
        }
        
        ElMessage.success('重命名成功');
      } catch (error) {
        console.error('Error renaming conversation:', error);
        ElMessage.error('重命名失败: ' + (error.message || '无法重命名会话'));
      }
    },

    async deleteConversation(conversationId) {
      if (!conversationId) return;
      
      try {
        await request({
          url: `/ai/conversations/${conversationId}`,
          method: 'delete',
          headers: {
            'X-App-ID': this.appId || ''
          }
        });
        
        this.conversationHistory = this.conversationHistory.filter(c => c.id !== conversationId);
        
        if (this.currentConversationId === conversationId) {
          this.clearMessages();
        }
        
        this.messageCache.delete(conversationId);
        
        ElMessage.success('删除成功');
      } catch (error) {
        console.error('Error deleting conversation:', error);
        ElMessage.error('删除失败: ' + (error.message || '无法删除会话'));
      }
    },

    clearCache() {
      this.messageCache.clear();
    },

    clearAll() {
      this.clearMessages();
      this.clearCache();
    },

    clearUploadedFiles() {
      this.uploadingFiles = [];
      this.isUploading = false;
    },

    getInputAccept(fileTypes) {
      if (!fileTypes || !fileTypes.length) return '';
      
      const mimeTypes = {
        image: 'image/*',
        audio: 'audio/*',
        video: 'video/*',
        document: '.pdf,.doc,.docx,.txt,.rtf,.md'
      };
      
      return fileTypes.map(type => mimeTypes[type] || '').filter(Boolean).join(',');
    }
  }
});
