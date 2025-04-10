<template>
  <div class="app-container">
    <el-container class="chat-container">
      <el-aside width="250px" class="chat-sidebar">
        <div class="sidebar-header">
          <el-button type="primary" @click="createNewChat" plain>新建对话</el-button>
        </div>
        <el-menu
          :default-active="activeTopicId"
          class="topic-list"
          @select="handleTopicSelect"
        >
          <el-menu-item v-for="topic in topicList" :key="topic.id" :index="topic.id.toString()">
            <span class="topic-name">{{ topic.name }}</span>
            <el-dropdown trigger="click" @command="handleTopicCommand($event, topic)">
              <span class="el-dropdown-link">
                <el-icon><more /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="rename">重命名</el-dropdown-item>
                  <el-dropdown-item command="pin" v-if="!topic.pinned">置顶</el-dropdown-item>
                  <el-dropdown-item command="unpin" v-else>取消置顶</el-dropdown-item>
                  <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-container class="chat-main">
        <el-header class="chat-header">
          <div class="assistant-info" v-if="currentAssistant">
            <span class="assistant-emoji">{{ currentAssistant.emoji || '🤖' }}</span>
            <span class="assistant-name">{{ currentAssistant.name }}</span>
          </div>
          <div class="header-actions">
            <el-select v-model="currentModelId" placeholder="选择模型" size="small" v-if="currentAssistant">
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
                  {{ currentAssistant?.emoji || '🤖' }}
                </el-avatar>
              </div>
              <div class="message-content">
                <div class="message-header">
                  <span class="message-sender">{{ message.role === 'user' ? '用户' : currentAssistant?.name }}</span>
                  <span class="message-time">{{ formatTime(message.createdAt) }}</span>
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
      <el-input v-model="newTopicName" placeholder="请输入新名称"></el-input>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="renameDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmRenameTopic">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 选择助手对话框 -->
    <el-dialog title="选择助手" v-model="selectAssistantDialogVisible" width="50%">
      <el-row :gutter="20">
        <el-col :span="8" v-for="assistant in assistantList" :key="assistant.id">
          <el-card class="assistant-card" @click="selectAssistant(assistant)">
            <div class="assistant-card-content">
              <div class="assistant-emoji">{{ assistant.emoji || '🤖' }}</div>
              <div class="assistant-name">{{ assistant.name }}</div>
              <div class="assistant-description">{{ assistant.description }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick, watch } from 'vue';
import { listAssistant } from "@/api/ai/assistant";
import { listModel } from "@/api/ai/model";
import { listTopic, getTopic, addTopic, updateTopic, delTopic } from "@/api/ai/topic";
import { listMessage, addMessage } from "@/api/ai/message";
import { ElMessage, ElMessageBox } from 'element-plus';
import { marked } from 'marked';
import hljs from 'highlight.js';
import DOMPurify from 'dompurify';

// 初始化marked配置
marked.setOptions({
  highlight: function(code, lang) {
    const language = hljs.getLanguage(lang) ? lang : 'plaintext';
    return hljs.highlight(code, { language }).value;
  },
  langPrefix: 'hljs language-'
});

const topicList = ref([]);
const assistantList = ref([]);
const modelList = ref([]);
const messageList = ref([]);
const activeTopicId = ref('');
const currentAssistant = ref(null);
const currentModelId = ref(null);
const userInput = ref('');
const isTyping = ref(false);
const messagesContainer = ref(null);
const renameDialogVisible = ref(false);
const selectAssistantDialogVisible = ref(false);
const newTopicName = ref('');
const currentTopicToRename = ref(null);

// 获取助手列表
const getAssistantList = async () => {
  try {
    const response = await listAssistant({ pageSize: 100 });
    assistantList.value = response.rows;
  } catch (error) {
    console.error('获取助手列表失败:', error);
    ElMessage.error('获取助手列表失败');
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

// 获取对话主题列表
const getTopicList = async () => {
  try {
    const response = await listTopic({ pageSize: 100 });
    topicList.value = response.rows.sort((a, b) => {
      // 先按置顶排序，再按更新时间排序
      if (a.pinned && !b.pinned) return -1;
      if (!a.pinned && b.pinned) return 1;
      return new Date(b.updatedAt) - new Date(a.updatedAt);
    });
    
    // 如果有主题，默认选中第一个
    if (topicList.value.length > 0 && !activeTopicId.value) {
      activeTopicId.value = topicList.value[0].id.toString();
      loadTopic(activeTopicId.value);
    }
  } catch (error) {
    console.error('获取对话主题列表失败:', error);
    ElMessage.error('获取对话主题列表失败');
  }
};

// 加载指定主题的消息
const loadTopic = async (topicId) => {
  try {
    const response = await getTopic(topicId);
    const topic = response.data;
    
    // 设置当前助手
    const assistant = assistantList.value.find(a => a.id === topic.assistantId);
    if (assistant) {
      currentAssistant.value = assistant;
      // 如果没有设置当前模型，使用助手默认模型
      if (!currentModelId.value) {
        currentModelId.value = assistant.defaultModelId || assistant.modelId;
      }
    }
    
    // 加载消息
    loadMessages(topicId);
  } catch (error) {
    console.error('加载主题失败:', error);
    ElMessage.error('加载主题失败');
  }
};

// 加载消息列表
const loadMessages = async (topicId) => {
  try {
    const response = await listMessage({ topicId, pageSize: 100 });
    messageList.value = response.rows.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
    
    // 滚动到底部
    await nextTick();
    scrollToBottom();
  } catch (error) {
    console.error('获取消息列表失败:', error);
    ElMessage.error('获取消息列表失败');
  }
};

// 创建新对话
const createNewChat = () => {
  selectAssistantDialogVisible.value = true;
};

// 选择助手创建新对话
const selectAssistant = async (assistant) => {
  try {
    // 创建新主题
    const newTopic = {
      name: `新对话 ${new Date().toLocaleString()}`,
      assistantId: assistant.id,
      pinned: false,
      isNameManuallyEdited: false
    };
    
    const response = await addTopic(newTopic);
    selectAssistantDialogVisible.value = false;
    
    // 刷新主题列表并选中新创建的主题
    await getTopicList();
    activeTopicId.value = response.data.id.toString();
    currentAssistant.value = assistant;
    currentModelId.value = assistant.defaultModelId || assistant.modelId;
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
    topicId: parseInt(activeTopicId.value),
    assistantId: currentAssistant.value.id,
    status: 'success',
    type: 'text',
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
    await addMessage(userMessage);
    
    // 显示AI正在输入
    isTyping.value = true;
    
    // 创建AI回复消息
    const assistantMessage = {
      role: 'assistant',
      content: '',
      topicId: parseInt(activeTopicId.value),
      assistantId: currentAssistant.value.id,
      modelId: currentModelId.value,
      status: 'pending',
      type: 'text',
      createdAt: new Date().toISOString()
    };
    
    // 发送AI消息到服务器
    const response = await addMessage(assistantMessage);
    
    // 更新AI消息内容
    isTyping.value = false;
    const aiMessage = response.data;
    messageList.value.push(aiMessage);
    
    // 滚动到底部
    await nextTick();
    scrollToBottom();
    
    // 如果是第一条消息，且主题名称未手动编辑，则更新主题名称
    const topic = topicList.value.find(t => t.id.toString() === activeTopicId.value);
    if (messageList.value.length <= 2 && topic && !topic.isNameManuallyEdited) {
      // 使用用户消息的前20个字符作为主题名称
      const newName = userInputContent.length > 20 
        ? userInputContent.substring(0, 20) + '...' 
        : userInputContent;
      
      await updateTopic({
        id: parseInt(activeTopicId.value),
        name: newName,
        assistantId: currentAssistant.value.id,
        pinned: topic.pinned,
        isNameManuallyEdited: false
      });
      
      // 刷新主题列表
      getTopicList();
    }
  } catch (error) {
    console.error('发送消息失败:', error);
    ElMessage.error('发送消息失败');
    isTyping.value = false;
    
    // 移除最后一条用户消息
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
    
    // 显示AI正在输入
    isTyping.value = true;
    
    // 创建新的AI回复消息
    const assistantMessage = {
      role: 'assistant',
      content: '',
      topicId: parseInt(activeTopicId.value),
      assistantId: currentAssistant.value.id,
      modelId: currentModelId.value,
      status: 'pending',
      type: 'text',
      createdAt: new Date().toISOString()
    };
    
    // 发送AI消息到服务器
    const response = await addMessage(assistantMessage);
    
    // 更新AI消息内容
    isTyping.value = false;
    const aiMessage = response.data;
    messageList.value.push(aiMessage);
    
    // 滚动到底部
    await nextTick();
    scrollToBottom();
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
      // 创建新主题
      const newTopic = {
        name: `新对话 ${new Date().toLocaleString()}`,
        assistantId: currentAssistant.value.id,
        pinned: false,
        isNameManuallyEdited: false
      };
      
      const response = await addTopic(newTopic);
      
      // 刷新主题列表并选中新创建的主题
      await getTopicList();
      activeTopicId.value = response.data.id.toString();
      messageList.value = [];
    }).catch(() => {});
  } catch (error) {
    console.error('清空对话失败:', error);
    ElMessage.error('清空对话失败');
  }
};

// 处理主题选择
const handleTopicSelect = (topicId) => {
  activeTopicId.value = topicId;
  loadTopic(topicId);
};

// 处理主题操作
const handleTopicCommand = (command, topic) => {
  switch (command) {
    case 'rename':
      currentTopicToRename.value = topic;
      newTopicName.value = topic.name;
      renameDialogVisible.value = true;
      break;
    case 'pin':
      updateTopicPin(topic, true);
      break;
    case 'unpin':
      updateTopicPin(topic, false);
      break;
    case 'delete':
      deleteTopic(topic);
      break;
  }
};

// 确认重命名主题
const confirmRenameTopic = async () => {
  if (!newTopicName.value.trim()) {
    ElMessage.warning('名称不能为空');
    return;
  }
  
  try {
    await updateTopic({
      id: currentTopicToRename.value.id,
      name: newTopicName.value,
      assistantId: currentTopicToRename.value.assistantId,
      pinned: currentTopicToRename.value.pinned,
      isNameManuallyEdited: true
    });
    
    renameDialogVisible.value = false;
    getTopicList();
    ElMessage.success('重命名成功');
  } catch (error) {
    console.error('重命名失败:', error);
    ElMessage.error('重命名失败');
  }
};

// 更新主题置顶状态
const updateTopicPin = async (topic, pinned) => {
  try {
    await updateTopic({
      id: topic.id,
      name: topic.name,
      assistantId: topic.assistantId,
      pinned: pinned,
      isNameManuallyEdited: topic.isNameManuallyEdited
    });
    
    getTopicList();
    ElMessage.success(pinned ? '置顶成功' : '取消置顶成功');
  } catch (error) {
    console.error('更新置顶状态失败:', error);
    ElMessage.error('更新置顶状态失败');
  }
};

// 删除主题
const deleteTopic = async (topic) => {
  try {
    ElMessageBox.confirm('确定要删除该对话吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      await delTopic(topic.id);
      
      // 如果删除的是当前选中的主题，则选中第一个主题
      if (activeTopicId.value === topic.id.toString()) {
        activeTopicId.value = '';
      }
      
      getTopicList();
      ElMessage.success('删除成功');
    }).catch(() => {});
  } catch (error) {
    console.error('删除主题失败:', error);
    ElMessage.error('删除主题失败');
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
  await getAssistantList();
  await getModelList();
  await getTopicList();
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

.topic-list {
  height: calc(100% - 65px);
  overflow-y: auto;
}

.topic-name {
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

.assistant-info {
  display: flex;
  align-items: center;
}

.assistant-emoji {
  font-size: 24px;
  margin-right: 10px;
}

.assistant-name {
  font-size: 16px;
  font-weight: bold;
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

.assistant-card {
  cursor: pointer;
  transition: all 0.3s;
  height: 150px;
  margin-bottom: 20px;
}

.assistant-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.assistant-card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.assistant-card .assistant-emoji {
  font-size: 32px;
  margin-bottom: 10px;
}

.assistant-card .assistant-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
}

.assistant-card .assistant-description {
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
