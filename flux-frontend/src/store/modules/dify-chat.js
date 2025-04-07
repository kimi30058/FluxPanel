import { getUserChats, getChatMessages, sendChatMessage, sendMessageToChat, createChat, deleteChat, renameChat } from '@/api/ai/dify'
import { getToken } from '@/utils/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import { defineStore } from 'pinia'
import { useRoute, useRouter } from 'vue-router'
import useUserStore from '@/store/modules/user'

const useDifyChatStore = defineStore(
  'dify-chat',
  {
    state: () => ({
      isLoadingApp: true,
      appid: null,
      appInfo: null,
      appParameters: null,
      userInputs: {},
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
    }),
    
    getters: {
      isNewConversation() {
        if (!this.currentConversationId) {
          if (this.appParameters?.opening_statement) {
            return this.messages.length <= 1;
          }
          return this.messages.length === 0;
        }
        return false;
      },
      
      openingStatement() {
        return this.appParameters?.opening_statement || "";
      },
    },
    
    actions: {
      setAppId(appid) {
        this.appid = appid;
      },
      
      async initDifyApp() {
        this.isLoadingApp = true;
        
        try {
          await Promise.all([
            this.loadConversations(),
            this.initConversationMessages(),
          ]);
        } catch (error) {
          console.error("Error initializing Dify app:", error);
        } finally {
          this.isLoadingApp = false;
        }
      },
      
      async loadConversations(loadMore = false) {
        this.isLoadingHistory = true;
        
        try {
          const params = {
            user_id: this.getUserId(),
            limit: 20,
            ...(loadMore && this.lastId ? { last_id: this.lastId } : {}),
          };
          
          const response = await getUserChats(params);
          const data = response.data || { data: [], has_more: false };
          
          if (loadMore) {
            this.conversationHistory = [
              ...this.conversationHistory,
              ...data.data,
            ];
          } else {
            this.conversationHistory = data.data;
          }
          
          this.hasMoreHistory = data.has_more;
          this.lastId = data.data[data.data.length - 1]?.id || null;
        } catch (error) {
          console.error("Error loading conversations:", error);
        } finally {
          this.isLoadingHistory = false;
        }
      },
      
      async initConversationMessages() {
        const route = useRoute();
        const conversationId = route.query.conversation_id;
        if (conversationId) {
          await this.getMessages(conversationId);
        }
      },
      
      async getMessages(conversation_id) {
        if (!conversation_id) return;
        
        this.currentConversationId = conversation_id;
        this.isMessagesLoading = true;
        
        try {
          if (this.messageCache.has(conversation_id)) {
            const cache = this.messageCache.get(conversation_id);
            this.messages = cache.messages;
            this.firstMessageId = cache.firstMessageId;
            this.hasMoreMessages = cache.hasMoreMessages;
            this.isMessagesLoading = false;
            return;
          }
          
          const params = {
            limit: 20,
            offset: 0
          };
          
          const response = await getChatMessages(conversation_id, params);
          const messages = response.data || [];
          
          this.messages = messages.map(msg => ({
            id: msg.id,
            content: msg.content,
            isBot: msg.role === 'assistant',
            timestamp: msg.created_at,
            files: msg.files
          }));
          
          this.messageCache.set(conversation_id, {
            messages: this.messages,
            firstMessageId: this.messages[0]?.id,
            hasMoreMessages: messages.length >= 20,
          });
          
          this.firstMessageId = this.messages[0]?.id;
          this.hasMoreMessages = messages.length >= 20;
        } catch (error) {
          console.error("Error fetching messages:", error);
          ElMessage.error('获取消息失败');
        } finally {
          this.isMessagesLoading = false;
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
        this.showUserInputForm = false;
        this.showUserInputFormCancelBtn = false;
      },
      
      async sendMessage(content) {
        if (!content.trim()) return;
        
        try {
          const userMessage = {
            id: Date.now().toString(),
            content,
            isBot: false,
            files: this.uploadingFiles.length > 0 ? [...this.uploadingFiles] : undefined,
          };
          this.addMessage(userMessage);
          
          this.isLoadingMessage = true;
          
          const botMessageId = (Date.now() + 1).toString();
          const botMessage = {
            id: botMessageId,
            content: "",
            isBot: true,
          };
          this.addMessage(botMessage);
          
          const userId = this.getUserId();
          let response;
          
          if (this.currentConversationId) {
            response = await sendMessageToChat(this.currentConversationId, {
              content: content,
              user_id: userId,
              streaming: false
            });
          } else {
            response = await sendChatMessage({
              query: content,
              user_id: userId,
              app_id: this.appid,
              conversation_id: undefined,
              streaming: false,
              inputs: this.userInputs || {},
            });
          }
          
          const messageIndex = this.messages.findIndex(m => m.id === botMessageId);
          if (messageIndex !== -1) {
            this.messages[messageIndex].content = response.data.answer || response.data.message || '';
          }
          
          if (response.data.conversation_id) {
            this.currentConversationId = response.data.conversation_id;
          }
          
          if (!this.currentConversationId) {
            this.loadConversations();
          }
          
          this.uploadingFiles = [];
        } catch (error) {
          console.error("Error sending message:", error);
          
          const lastMessage = this.messages[this.messages.length - 1];
          if (lastMessage?.isBot && lastMessage?.content === "") {
            this.messages.pop();
          }
          
          this.addMessage({
            id: Date.now().toString(),
            content: error.message || "抱歉，发生了错误，请稍后重试。",
            isBot: true,
            error: true,
          });
          
          ElMessage.error('消息发送失败');
        } finally {
          this.isLoadingMessage = false;
        }
      },
      
      startNewConversation() {
        this.clearMessages();
      },
      
      async deleteConversation(conversationId) {
        try {
          await deleteChat(conversationId);
          
          this.conversationHistory = this.conversationHistory.filter(
            (c) => c.id !== conversationId
          );
          
          if (this.currentConversationId === conversationId) {
            this.clearMessages();
          }
          
          return true;
        } catch (error) {
          console.error("Error deleting conversation:", error);
          ElMessage.error('删除会话失败');
          return false;
        }
      },
      
      async renameConversation(conversationId, title) {
        try {
          await renameChat(conversationId, { title });
          
          const index = this.conversationHistory.findIndex(
            (c) => c.id === conversationId
          );
          if (index !== -1) {
            this.conversationHistory[index].title = title;
          }
          
          return true;
        } catch (error) {
          console.error("Error renaming conversation:", error);
          ElMessage.error('重命名会话失败');
          return false;
        }
      },
      
      getUserId() {
        const userStore = useUserStore();
        return userStore.id;
      }
    }
  }
)

export default useDifyChatStore
