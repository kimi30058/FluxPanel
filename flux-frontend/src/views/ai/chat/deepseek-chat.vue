<template>
  <div class="app-container">
    <el-container class="chat-container">
      <!-- Chat sidebar with conversation history -->
      <el-aside width="250px" class="chat-sidebar">
        <div class="sidebar-header">
          <el-button type="primary" @click="createNewChat" plain>新建对话</el-button>
        </div>
        <el-menu
          :default-active="activeChatId"
          class="chat-list"
          @select="handleChatSelect"
        >
          <el-menu-item v-for="chat in chatList" :key="chat.id" :index="chat.id.toString()">
            <span class="chat-name">{{ chat.title }}</span>
            <el-dropdown trigger="click" @command="handleChatCommand($event, chat)">
              <span class="el-dropdown-link">
                <el-icon><more /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="rename">重命名</el-dropdown-item>
                  <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- Main chat area -->
      <el-container class="chat-main">
        <el-header class="chat-header">
          <div class="provider-info" v-if="currentProvider">
            <span class="provider-name">{{ currentProvider.name }}</span>
            <span class="provider-type">(DeepSeek)</span>
          </div>
          <div class="header-actions">
            <el-select v-model="currentModelId" placeholder="选择模型" size="small" v-if="currentProvider">
              <el-option
                v-for="model in modelList"
                :key="model.id"
                :label="model.name"
                :value="model.id"
              />
            </el-select>
            <el-button type="primary" size="small" @click="clearMessages" plain>清空对话</el-button>
          </div>
        </el-header>
        
        <!-- Messages display area -->
        <el-main class="chat-messages">
          <div class="messages-container" ref="messagesContainer">
            <div v-for="(message, index) in messageList" :key="index" :class="['message', message.role]">
              <div class="message-avatar">
                <el-avatar :size="40" v-if="message.role === 'user'">
                  <el-icon><user /></el-icon>
                </el-avatar>
                <el-avatar :size="40" v-else>
                  <el-icon><chat-round /></el-icon>
                </el-avatar>
              </div>
              <div class="message-content">
                <div class="message-header">
                  <span class="message-sender">{{ message.role === 'user' ? '用户' : 'DeepSeek AI' }}</span>
                  <span class="message-time">{{ formatTime(message.createdAt || new Date()) }}</span>
                </div>
                <div class="message-text" v-html="formatMessage(message.content)"></div>
                <div class="message-actions" v-if="message.role === 'assistant'">
                  <el-button type="text" size="small" @click="copyMessage(message)">复制</el-button>
                  <el-button type="text" size="small" @click="regenerateMessage(message)" v-if="index === messageList.length - 1 && message.role === 'assistant'">重新生成</el-button>
                </div>
              </div>
            </div>
            <div class="typing-indicator" v-if="isTyping">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </el-main>
        
        <!-- Input area -->
        <el-footer class="chat-input">
          <div class="input-container">
            <el-input
              v-model="userInput"
              type="textarea"
              :rows="3"
              placeholder="输入消息..."
              resize="none"
              @keydown.enter.exact.prevent="sendMessage"
            />
            <div class="input-actions">
              <el-button type="primary" @click="sendMessage" :disabled="!userInput.trim() || isTyping">发送</el-button>
            </div>
          </div>
        </el-footer>
      </el-container>
    </el-container>
    
    <!-- Dialogs -->
    <el-dialog title="重命名对话" v-model="renameDialogVisible" width="30%">
      <el-input v-model="newChatTitle" placeholder="请输入新名称"></el-input>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="renameDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmRenameChat">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <el-dialog title="选择DeepSeek提供商" v-model="selectProviderDialogVisible" width="50%">
      <el-row :gutter="20">
        <el-col :span="8" v-for="provider in deepseekProviders" :key="provider.id">
          <el-card class="provider-card" @click="selectProvider(provider)">
            <div class="provider-card-content">
              <div class="provider-type">DeepSeek</div>
              <div class="provider-name">{{ provider.name }}</div>
              <div class="provider-description">{{ provider.description || '无描述' }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue';
import { listProvider } from "@/api/ai/provider";
import { listModel } from "@/api/ai/model";
import { sendChat, sendChatStream, saveChatHistory } from "@/api/ai/deepseek";
import { ElMessage, ElMessageBox } from 'element-plus';
import { marked } from 'marked';
import hljs from 'highlight.js';
import DOMPurify from 'dompurify';

// 初始化变量
const chatList = ref([]);
const providerList = ref([]);
const modelList = ref([]);
const messageList = ref([]);
const activeChatId = ref('');
const currentProvider = ref(null);
const currentModelId = ref(null);
const userInput = ref('');
const isTyping = ref(false);
const messagesContainer = ref(null);
const renameDialogVisible = ref(false);
const selectProviderDialogVisible = ref(false);
const newChatTitle = ref('');
const currentChatToRename = ref(null);

// 计算属性：筛选DeepSeek提供商
const deepseekProviders = computed(() => {
  return providerList.value.filter(p => p.type.toLowerCase() === 'deepseek');
});

// API调用函数
const getProviderList = async () => {
  try {
    const response = await listProvider({ pageSize: 100 });
    providerList.value = response.rows;
  } catch (error) {
    console.error('获取提供商列表失败:', error);
    ElMessage.error('获取提供商列表失败');
  }
};

const getModelList = async () => {
  try {
    const response = await listModel({ pageSize: 100 });
    modelList.value = response.rows;
  } catch (error) {
    console.error('获取模型列表失败:', error);
    ElMessage.error('获取模型列表失败');
  }
};

// 本地存储管理
const getChatList = async () => {
  try {
    const savedChats = localStorage.getItem('deepseek_chats');
    if (savedChats) {
      chatList.value = JSON.parse(savedChats).sort((a, b) => {
        return new Date(b.updatedAt) - new Date(a.updatedAt);
      });
      
      if (chatList.value.length > 0 && !activeChatId.value) {
        activeChatId.value = chatList.value[0].id.toString();
        loadChat(activeChatId.value);
      }
    }
  } catch (error) {
    console.error('获取聊天列表失败:', error);
    ElMessage.error('获取聊天列表失败');
  }
};

const saveChatList = () => {
  localStorage.setItem('deepseek_chats', JSON.stringify(chatList.value));
};

const loadChat = async (chatId) => {
  try {
    const savedMessages = localStorage.getItem(`deepseek_messages_${chatId}`);
    if (savedMessages) {
      messageList.value = JSON.parse(savedMessages);
    } else {
      messageList.value = [];
    }
    
    const chat = chatList.value.find(c => c.id.toString() === chatId);
    if (chat && chat.providerId) {
      const provider = providerList.value.find(p => p.id === chat.providerId);
      if (provider) {
        currentProvider.value = provider;
      }
    }
    
    await nextTick();
    scrollToBottom();
  } catch (error) {
    console.error('加载聊天失败:', error);
    ElMessage.error('加载聊天失败');
  }
};

const saveMessageList = (chatId) => {
  localStorage.setItem(`deepseek_messages_${chatId}`, JSON.stringify(messageList.value));
};

// 用户交互函数
const createNewChat = () => {
  selectProviderDialogVisible.value = true;
};

const selectProvider = async (provider) => {
  try {
    const newChat = {
      id: Date.now(),
      title: `新对话 ${new Date().toLocaleString()}`,
      providerId: provider.id,
      updatedAt: new Date().toISOString()
    };
    
    chatList.value.unshift(newChat);
    saveChatList();
    
    selectProviderDialogVisible.value = false;
    
    activeChatId.value = newChat.id.toString();
    currentProvider.value = provider;
    messageList.value = [];
    saveMessageList(activeChatId.value);
  } catch (error) {
    console.error('创建新对话失败:', error);
    ElMessage.error('创建新对话失败');
  }
};

const sendMessage = async () => {
  if (!userInput.value.trim() || isTyping.value) return;
  
  const userMessage = {
    role: 'user',
    content: userInput.value,
    createdAt: new Date().toISOString()
  };
  
  messageList.value.push(userMessage);
  saveMessageList(activeChatId.value);
  
  const userInputContent = userInput.value;
  userInput.value = '';
  
  await nextTick();
  scrollToBottom();
  
  isTyping.value = true;
  
  try {
    const chatRequest = {
      messages: messageList.value.map(msg => ({
        role: msg.role,
        content: msg.content
      })),
      model: modelList.value.find(m => m.id === currentModelId.value)?.code || "deepseek-chat"
    };
    
    const aiResponse = await sendChat(currentProvider.value.id, chatRequest);
    
    isTyping.value = false;
    
    const assistantMessage = {
      role: 'assistant',
      content: aiResponse.data.choices[0].message.content,
      createdAt: new Date().toISOString()
    };
    
    messageList.value.push(assistantMessage);
    saveMessageList(activeChatId.value);
    
    await nextTick();
    scrollToBottom();
    
    if (messageList.value.length <= 2) {
      const newTitle = userInputContent.length > 20 
        ? userInputContent.substring(0, 20) + '...' 
        : userInputContent;
      
      const chatIndex = chatList.value.findIndex(c => c.id.toString() === activeChatId.value);
      if (chatIndex !== -1) {
        chatList.value[chatIndex].title = newTitle;
        chatList.value[chatIndex].updatedAt = new Date().toISOString();
        saveChatList();
      }
    }
    
    await saveChatHistory({
      messages: messageList.value,
      provider_id: currentProvider.value.id,
      title: chatList.value.find(c => c.id.toString() === activeChatId.value)?.title
    });
  } catch (error) {
    console.error('发送消息失败:', error);
    ElMessage.error('发送消息失败: ' + error.message);
    isTyping.value = false;
    
    messageList.value.pop();
    saveMessageList(activeChatId.value);
  }
};

// 辅助函数
const copyMessage = (message) => {
  navigator.clipboard.writeText(message.content)
    .then(() => {
      ElMessage.success('已复制到剪贴板');
    })
    .catch(() => {
      ElMessage.error('复制失败');
    });
};

const regenerateMessage = async (message) => {
  if (isTyping.value) return;
  
  try {
    messageList.value.pop();
    saveMessageList(activeChatId.value);
    
    await sendMessage();
  } catch (error) {
    console.error('重新生成消息失败:', error);
    ElMessage.error('重新生成消息失败');
    isTyping.value = false;
  }
};

const clearMessages = async () => {
  try {
    ElMessageBox.confirm('确定要清空当前对话吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      const newChat = {
        id: Date.now(),
        title: `新对话 ${new Date().toLocaleString()}`,
        providerId: currentProvider.value.id,
        updatedAt: new Date().toISOString()
      };
      
      chatList.value.unshift(newChat);
      saveChatList();
      
      activeChatId.value = newChat.id.toString();
      messageList.value = [];
      saveMessageList(activeChatId.value);
    }).catch(() => {});
  } catch (error) {
    console.error('清空对话失败:', error);
    ElMessage.error('清空对话失败');
  }
};

const handleChatSelect = (chatId) => {
  activeChatId.value = chatId;
  loadChat(chatId);
};

const handleChatCommand = (command, chat) => {
  switch (command) {
    case 'rename':
      currentChatToRename.value = chat;
      newChatTitle.value = chat.title;
      renameDialogVisible.value = true;
      break;
    case 'delete':
      deleteCurrentChat(chat);
      break;
  }
};

const confirmRenameChat = async () => {
  if (!newChatTitle.value.trim()) {
    ElMessage.warning('名称不能为空');
    return;
  }
  
  try {
    const chatIndex = chatList.value.findIndex(c => c.id === currentChatToRename.value.id);
    if (chatIndex !== -1) {
      chatList.value[chatIndex].title = newChatTitle.value;
      chatList.value[chatIndex].updatedAt = new Date().toISOString();
      saveChatList();
    }
    
    renameDialogVisible.value = false;
    ElMessage.success('重命名成功');
  } catch (error) {
    console.error('重命名失败:', error);
    ElMessage.error('重命名失败');
  }
};

const deleteCurrentChat = async (chat) => {
  try {
    ElMessageBox.confirm('确定要删除该对话吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      const chatIndex = chatList.value.findIndex(c => c.id === chat.id);
      if (chatIndex !== -1) {
        chatList.value.splice(chatIndex, 1);
        saveChatList();
      }
      
      localStorage.removeItem(`deepseek_messages_${chat.id}`);
      
      if (activeChatId.value === chat.id.toString()) {
        if (chatList.value.length > 0) {
          activeChatId.value = chatList.value[0].id.toString();
          loadChat(activeChatId.value);
        } else {
          activeChatId.value = '';
          messageList.value = [];
        }
      }
      
      ElMessage.success('删除成功');
    }).catch(() => {});
  } catch (error) {
    console.error('删除聊天失败:', error);
    ElMessage.error('删除聊天失败');
  }
};

const formatMessage = (content) => {
  if (!content) return '';
  const html = marked(content);
  return DOMPurify.sanitize(html);
};

const formatTime = (timestamp) => {
  if (!timestamp) return '';
  const date = new Date(timestamp);
  return date.toLocaleString();
};

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// 监听器
watch(currentModelId, (newVal, oldVal) => {
  if (newVal && oldVal && newVal !== oldVal) {
    ElMessage.info(`已切换到模型: ${modelList.value.find(m => m.id === newVal)?.name || '未知模型'}`);
  }
});

// 初始化
onMounted(async () => {
  await getProviderList();
  await getModelList();
  await getChatList();
});
</script>

<style scoped>
.chat-container {
  height: calc(100vh - 120px);
  border: 1px solid #e6e6e6;
  border-radius: 4px;
  overflow: hidden;
}

.chat-sidebar {
  border-right: 1px solid #e6e6e6;
  background-color: #f5f7fa;
}

.sidebar-header {
  padding: 15px;
  border-bottom: 1px solid #e6e6e6;
  text-align: center;
}

.chat-list {
  height: calc(100% - 65px);
  overflow-y: auto;
}

.chat-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chat-main {
  display: flex;
  flex-direction: column;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  border-bottom: 1px solid #e6e6e6;
  background-color: #fff;
}

.provider-info {
  display: flex;
  align-items: center;
}

.provider-name {
  font-size: 16px;
  font-weight: bold;
  margin-right: 5px;
}

.provider-type {
  font-size: 14px;
  color: #909399;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.chat-messages {
  flex: 1;
  padding: 0;
  overflow: hidden;
}

.messages-container {
  height: 100%;
  padding: 20px;
  overflow-y: auto;
}

.message {
  display: flex;
  margin-bottom: 20px;
}

.message-avatar {
  margin-right: 12px;
  flex-shrink: 0;
}

.message-content {
  flex: 1;
  background-color: #f5f7fa;
  border-radius: 8px;
  padding: 12px;
  max-width: calc(100% - 60px);
}

.message.user .message-content {
  background-color: #ecf5ff;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.message-sender {
  font-weight: bold;
}

.message-time {
  font-size: 12px;
  color: #909399;
}

.message-text {
  line-height: 1.5;
  word-break: break-word;
}

.message-actions {
  margin-top: 8px;
  text-align: right;
}

.typing-indicator {
  display: inline-flex;
  align-items: center;
  background-color: #f5f7fa;
  border-radius: 8px;
  padding: 12px;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  background-color: #606266;
  border-radius: 50%;
  display: inline-block;
  margin: 0 2px;
  animation: typing 1.4s infinite ease-in-out both;
}

@keyframes typing {
  0% { transform: scale(1); }
  50% { transform: scale(1.5); }
  100% { transform: scale(1); }
}

.chat-input {
  padding: 10px 20px;
  background-color: #fff;
  border-top: 1px solid #e6e6e6;
  height: auto;
}

.input-container {
  display: flex;
  flex-direction: column;
}

.input-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.provider-card {
  cursor: pointer;
  transition: all 0.3s;
  height: 150px;
  margin-bottom: 20px;
}

.provider-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.provider-card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>
