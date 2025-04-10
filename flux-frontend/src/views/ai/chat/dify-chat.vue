<template>
  <div class="app-container">
    <el-container class="chat-container">
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
      
      <el-container class="chat-main">
        <el-header class="chat-header">
          <div class="provider-info" v-if="currentProvider">
            <span class="provider-name">{{ currentProvider.name }}</span>
            <span class="provider-type">({{ currentProvider.type }})</span>
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
                  <span class="message-sender">{{ message.role === 'user' ? '用户' : 'AI' }}</span>
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
    
    <!-- 重命名对话框 -->
    <el-dialog title="重命名对话" v-model="renameDialogVisible" width="30%">
      <el-input v-model="newChatTitle" placeholder="请输入新名称"></el-input>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="renameDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmRenameChat">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 选择提供商对话框 -->
    <el-dialog title="选择AI提供商" v-model="selectProviderDialogVisible" width="50%">
      <el-row :gutter="20">
        <el-col :span="8" v-for="provider in providerList" :key="provider.id">
          <el-card class="provider-card" @click="selectProvider(provider)">
            <div class="provider-card-content">
              <div class="provider-type">{{ provider.type }}</div>
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
import { ref, reactive, computed, onMounted, nextTick, watch } from 'vue';
import { listProvider } from "@/api/ai/provider";
import { listModel } from "@/api/ai/model";
import { sendChat, sendChatStream, createChat, getUserChats, sendMessageToChat, getChatMessages, deleteChat, renameChat } from "@/api/ai/dify";
import { sendChat as sendDeepSeekChat, sendChatStream as sendDeepSeekChatStream, saveChatHistory } from "@/api/ai/deepseek";
import { ElMessage, ElMessageBox } from 'element-plus';
import { marked } from 'marked';
import hljs from 'highlight.js';
import DOMPurify from 'dompurify';
import { User, ChatRound, More } from '@element-plus/icons-vue';

// 初始化marked配置
marked.setOptions({
  highlight: function(code, lang) {
    const language = hljs.getLanguage(lang) ? lang : 'plaintext';
    return hljs.highlight(code, { language }).value;
  },
  langPrefix: 'hljs language-'
});

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

// 获取提供商列表
const getProviderList = async () => {
  try {
    const response = await listProvider({ pageSize: 100 });
    providerList.value = response.rows;
  } catch (error) {
    console.error('获取提供商列表失败:', error);
    ElMessage.error('获取提供商列表失败');
  }
};

// 获取模型列表
const getModelList = async () => {
  try {
    const response = await listModel({ pageSize: 100 });
    modelList.value = response.rows;
  } catch (error) {
    console.error('获取模型列表失败:', error);
    ElMessage.error('获取模型列表失败');
  }
};

// 获取聊天列表
const getChatList = async () => {
  try {
    const response = await getUserChats({ pageSize: 100 });
    chatList.value = response.rows.sort((a, b) => {
      return new Date(b.updatedAt) - new Date(a.updatedAt);
    });
    
    // 如果有聊天，默认选中第一个
    if (chatList.value.length > 0 && !activeChatId.value) {
      activeChatId.value = chatList.value[0].id.toString();
      loadChat(activeChatId.value);
    }
  } catch (error) {
    console.error('获取聊天列表失败:', error);
    ElMessage.error('获取聊天列表失败');
  }
};

// 加载指定聊天的消息
const loadChat = async (chatId) => {
  try {
    const response = await getChatMessages(chatId, { limit: 100, offset: 0 });
    messageList.value = response.rows.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
    
    // 获取当前聊天的提供商信息
    const chat = chatList.value.find(c => c.id.toString() === chatId);
    if (chat && chat.providerId) {
      const provider = providerList.value.find(p => p.id === chat.providerId);
      if (provider) {
        currentProvider.value = provider;
      }
    }
    
    // 滚动到底部
    await nextTick();
    scrollToBottom();
  } catch (error) {
    console.error('加载聊天失败:', error);
    ElMessage.error('加载聊天失败');
  }
};

// 创建新对话
const createNewChat = () => {
  selectProviderDialogVisible.value = true;
};

// 选择提供商创建新对话
const selectProvider = async (provider) => {
  try {
    // 创建新聊天
    const newChat = {
      title: `新对话 ${new Date().toLocaleString()}`,
      providerId: provider.id
    };
    
    const response = await createChat(newChat);
    selectProviderDialogVisible.value = false;
    
    // 刷新聊天列表并选中新创建的聊天
    await getChatList();
    activeChatId.value = response.data.id.toString();
    currentProvider.value = provider;
    messageList.value = [];
  } catch (error) {
    console.error('创建新对话失败:', error);
    ElMessage.error('创建新对话失败');
  }
};

// 发送消息
const sendMessage = async () => {
  if (!userInput.value.trim() || isTyping.value) return;
  
  const userMessage = {
    role: 'user',
    content: userInput.value,
    chatId: parseInt(activeChatId.value),
    createdAt: new Date().toISOString()
  };
  
  // 添加用户消息到列表
  messageList.value.push(userMessage);
  
  // 清空输入框
  const userInputContent = userInput.value;
  userInput.value = '';
  
  // 滚动到底部
  await nextTick();
  scrollToBottom();
  
  // 发送用户消息到服务器
  try {
    await sendMessageToChat(activeChatId.value, userMessage);
    
    // 显示AI正在输入
    isTyping.value = true;
    
    // 准备AI消息请求
    const chatRequest = {
      messages: [
        ...messageList.value.map(msg => ({
          role: msg.role,
          content: msg.content
        }))
      ],
      model: modelList.value.find(m => m.id === currentModelId.value)?.code || "gpt-3.5-turbo",
      stream: false
    };
    
    // 根据提供商类型选择不同的API
    let aiResponse;
    if (currentProvider.value.type.toLowerCase() === 'dify') {
      aiResponse = await sendChat(currentProvider.value.id, chatRequest);
    } else if (currentProvider.value.type.toLowerCase() === 'deepseek') {
      aiResponse = await sendDeepSeekChat(currentProvider.value.id, chatRequest);
    } else {
      throw new Error(`不支持的提供商类型: ${currentProvider.value.type}`);
    }
    
    // 更新AI消息内容
    isTyping.value = false;
    
    // 创建AI回复消息
    const assistantMessage = {
      role: 'assistant',
      content: aiResponse.data.choices[0].message.content,
      chatId: parseInt(activeChatId.value),
      createdAt: new Date().toISOString()
    };
    
    // 添加AI消息到列表
    messageList.value.push(assistantMessage);
    
    // 保存AI消息到服务器
    await sendMessageToChat(activeChatId.value, assistantMessage);
    
    // 滚动到底部
    await nextTick();
    scrollToBottom();
    
    // 如果是第一条消息，更新聊天标题
    if (messageList.value.length <= 2) {
      // 使用用户消息的前20个字符作为聊天标题
      const newTitle = userInputContent.length > 20 
        ? userInputContent.substring(0, 20) + '...' 
        : userInputContent;
      
      await renameChat(activeChatId.value, { title: newTitle });
      
      // 刷新聊天列表
      getChatList();
    }
  } catch (error) {
    console.error('发送消息失败:', error);
    ElMessage.error('发送消息失败: ' + error.message);
    isTyping.value = false;
    
    // 移除最后一条用户消息
    messageList.value.pop();
  }
};

// 发送流式消息
const sendStreamMessage = async () => {
  if (!userInput.value.trim() || isTyping.value) return;
  
  const userMessage = {
    role: 'user',
    content: userInput.value,
    chatId: parseInt(activeChatId.value),
    createdAt: new Date().toISOString()
  };
  
  // 添加用户消息到列表
  messageList.value.push(userMessage);
  
  // 清空输入框
  const userInputContent = userInput.value;
  userInput.value = '';
  
  // 滚动到底部
  await nextTick();
  scrollToBottom();
  
  // 发送用户消息到服务器
  try {
    await sendMessageToChat(activeChatId.value, userMessage);
    
    // 显示AI正在输入
    isTyping.value = true;
    
    // 创建AI回复消息
    const assistantMessage = {
      role: 'assistant',
      content: '',
      chatId: parseInt(activeChatId.value),
      createdAt: new Date().toISOString()
    };
    
    // 添加AI消息到列表
    messageList.value.push(assistantMessage);
    
    // 准备AI消息请求
    const chatRequest = {
      messages: messageList.value.slice(0, -1).map(msg => ({
        role: msg.role,
        content: msg.content
      })),
      model: modelList.value.find(m => m.id === currentModelId.value)?.code || "gpt-3.5-turbo",
      stream: true
    };
    
    // 根据提供商类型选择不同的API
    let streamResponse;
    if (currentProvider.value.type.toLowerCase() === 'dify') {
      streamResponse = await sendChatStream(currentProvider.value.id, chatRequest);
    } else if (currentProvider.value.type.toLowerCase() === 'deepseek') {
      streamResponse = await sendDeepSeekChatStream(currentProvider.value.id, chatRequest);
    } else {
      throw new Error(`不支持的提供商类型: ${currentProvider.value.type}`);
    }
    
    // 处理流式响应
    const reader = streamResponse.data.getReader();
    const decoder = new TextDecoder();
    let done = false;
    
    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;
      
      if (done) break;
      
      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');
      
      for (const line of lines) {
        if (line.startsWith('data: ') && line.length > 6) {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.choices && data.choices[0].delta && data.choices[0].delta.content) {
              assistantMessage.content += data.choices[0].delta.content;
              // 强制更新视图
              messageList.value = [...messageList.value];
              // 滚动到底部
              scrollToBottom();
            }
          } catch (e) {
            console.error('解析流式响应失败:', e);
          }
        }
      }
    }
    
    // 更新AI消息内容
    isTyping.value = false;
    
    // 保存AI消息到服务器
    await sendMessageToChat(activeChatId.value, assistantMessage);
    
    // 如果是第一条消息，更新聊天标题
    if (messageList.value.length <= 2) {
      // 使用用户消息的前20个字符作为聊天标题
      const newTitle = userInputContent.length > 20 
        ? userInputContent.substring(0, 20) + '...' 
        : userInputContent;
      
      await renameChat(activeChatId.value, { title: newTitle });
      
      // 刷新聊天列表
      getChatList();
    }
  } catch (error) {
    console.error('发送流式消息失败:', error);
    ElMessage.error('发送流式消息失败: ' + error.message);
    isTyping.value = false;
    
    // 移除最后一条AI消息
    messageList.value.pop();
  }
};

// 复制消息内容
const copyMessage = (message) => {
  navigator.clipboard.writeText(message.content)
    .then(() => {
      ElMessage.success('已复制到剪贴板');
    })
    .catch(() => {
      ElMessage.error('复制失败');
    });
};

// 重新生成消息
const regenerateMessage = async (message) => {
  if (isTyping.value) return;
  
  try {
    // 移除最后一条AI消息
    messageList.value.pop();
    
    // 重新发送消息
    await sendMessage();
  } catch (error) {
    console.error('重新生成消息失败:', error);
    ElMessage.error('重新生成消息失败');
    isTyping.value = false;
  }
};

// 清空对话
const clearMessages = async () => {
  try {
    ElMessageBox.confirm('确定要清空当前对话吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      // 创建新聊天
      const newChat = {
        title: `新对话 ${new Date().toLocaleString()}`,
        providerId: currentProvider.value.id
      };
      
      const response = await createChat(newChat);
      
      // 刷新聊天列表并选中新创建的聊天
      await getChatList();
      activeChatId.value = response.data.id.toString();
      messageList.value = [];
    }).catch(() => {});
  } catch (error) {
    console.error('清空对话失败:', error);
    ElMessage.error('清空对话失败');
  }
};

// 处理聊天选择
const handleChatSelect = (chatId) => {
  activeChatId.value = chatId;
  loadChat(chatId);
};

// 处理聊天操作
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

// 确认重命名聊天
const confirmRenameChat = async () => {
  if (!newChatTitle.value.trim()) {
    ElMessage.warning('名称不能为空');
    return;
  }
  
  try {
    await renameChat(currentChatToRename.value.id, { title: newChatTitle.value });
    
    renameDialogVisible.value = false;
    getChatList();
    ElMessage.success('重命名成功');
  } catch (error) {
    console.error('重命名失败:', error);
    ElMessage.error('重命名失败');
  }
};

// 删除当前聊天
const deleteCurrentChat = async (chat) => {
  try {
    ElMessageBox.confirm('确定要删除该对话吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      await deleteChat(chat.id);
      
      // 如果删除的是当前选中的聊天，则选中第一个聊天
      if (activeChatId.value === chat.id.toString()) {
        activeChatId.value = '';
      }
      
      getChatList();
      ElMessage.success('删除成功');
    }).catch(() => {});
  } catch (error) {
    console.error('删除聊天失败:', error);
    ElMessage.error('删除聊天失败');
  }
};

// 格式化消息内容（支持Markdown）
const formatMessage = (content) => {
  if (!content) return '';
  
  // 使用marked解析Markdown
  const html = marked(content);
  
  // 使用DOMPurify清理HTML
  return DOMPurify.sanitize(html);
};

// 格式化时间
const formatTime = (timestamp) => {
  if (!timestamp) return '';
  
  const date = new Date(timestamp);
  return date.toLocaleString();
};

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// 监听当前模型变化
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

.message-text :deep(pre) {
  background-color: #282c34;
  border-radius: 4px;
  padding: 10px;
  overflow-x: auto;
}

.message-text :deep(code) {
  font-family: 'Courier New', Courier, monospace;
}

.message-text :deep(p) {
  margin: 8px 0;
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

.typing-indicator span:nth-child(1) {
  animation-delay: 0s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
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

.provider-card .provider-type {
  font-size: 14px;
  color: #409EFF;
  margin-bottom: 10px;
  text-transform: uppercase;
}

.provider-card .provider-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
}

.provider-card .provider-description {
  font-size: 12px;
  color: #909399;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
</style>
