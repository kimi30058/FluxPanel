<template>
  <div class="app-container chat-container">
    <el-row :gutter="20" class="chat-layout">
      <!-- 侧边栏 -->
      <el-col :span="6" :xs="24" class="sidebar-col">
        <el-card class="sidebar-card">
          <template #header>
            <div class="card-header">
              <span>会话列表</span>
              <el-button
                type="primary"
                plain
                size="small"
                icon="Plus"
                @click="startNewConversation"
              >新对话</el-button>
            </div>
          </template>
          <div v-if="isLoadingHistory" class="loading-container">
            <el-skeleton :rows="3" animated />
          </div>
          <div v-else-if="conversationHistory.length === 0" class="empty-container">
            <el-empty description="暂无会话记录" />
          </div>
          <div v-else class="conversation-list">
            <div
              v-for="conversation in conversationHistory"
              :key="conversation.id"
              class="conversation-item"
              :class="{ active: currentConversationId === conversation.id }"
              @click="getMessages(conversation.id)"
            >
              <div class="conversation-title">{{ conversation.name || '新对话' }}</div>
              <div class="conversation-actions">
                <el-dropdown trigger="click" @command="handleCommand($event, conversation)">
                  <el-button type="text" size="small" icon="More" />
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="rename">重命名</el-dropdown-item>
                      <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
            <div v-if="hasMoreHistory" class="load-more">
              <el-button type="text" @click="loadMoreConversations">加载更多</el-button>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 聊天主区域 -->
      <el-col :span="18" :xs="24" class="chat-main-col">
        <el-card class="chat-card">
          <template #header>
            <div class="card-header">
              <span v-if="isLoadingApp || !appInfo?.name">
                <el-skeleton style="width: 150px" animated />
              </span>
              <span v-else>{{ appInfo.name }}</span>
            </div>
          </template>

          <!-- 用户输入表单 -->
          <template v-if="showUserInputForm">
            <div class="user-input-form">
              <h3>请提供以下信息</h3>
              <el-form :model="userInputs" label-position="top">
                <el-form-item
                  v-for="field in userInputFormList"
                  :key="field.variable"
                  :label="field.label"
                >
                  <el-input
                    v-if="field.type === 'text'"
                    v-model="userInputs[field.variable]"
                    :placeholder="field.placeholder || ''"
                  />
                  <el-select
                    v-else-if="field.type === 'select'"
                    v-model="userInputs[field.variable]"
                    :placeholder="field.placeholder || '请选择'"
                    style="width: 100%"
                  >
                    <el-option
                      v-for="option in field.options"
                      :key="option.value"
                      :label="option.label"
                      :value="option.value"
                    />
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="startConversationByInputs">开始对话</el-button>
                  <el-button v-if="showUserInputFormCancelBtn" @click="showUserInputForm = false">取消</el-button>
                </el-form-item>
              </el-form>
            </div>
          </template>

          <template v-else>
            <!-- 消息区域 -->
            <div class="chat-messages" ref="messagesContainer" @scroll="handleMessagesScroll">
              <div v-if="isMessagesLoading" class="loading-container">
                <el-skeleton :rows="5" animated />
              </div>

              <!-- 加载更多提示 -->
              <div v-if="hasMoreMessages && isLoadingMore" class="loading-more">
                <el-icon class="is-loading"><Loading /></el-icon> 加载中...
              </div>

              <!-- 消息列表 -->
              <div v-if="!isMessagesLoading">
                <div v-if="messages.length === 0" class="empty-messages">
                  新的对话
                </div>

                <div
                  v-for="message in messages"
                  :key="message.id"
                  :class="[
                    'message-item',
                    message.isBot ? 'bot-message' : 'user-message'
                  ]"
                  :id="`message-${message.id}`"
                >
                  <div class="message-avatar">
                    <el-avatar
                      :icon="message.isBot ? 'ChatDotRound' : 'User'"
                      :size="36"
                      :class="message.isBot ? 'bot-avatar' : 'user-avatar'"
                    />
                  </div>
                  <div class="message-content">
                    <div
                      class="message-text"
                      :class="{ 'error-message': message.error }"
                      v-html="formatMessage(message.content)"
                    ></div>
                    <!-- 文件预览 -->
                    <div v-if="message.files && message.files.length > 0" class="message-files">
                      <div v-for="file in message.files" :key="file.id" class="file-item">
                        <el-link :href="file.url" target="_blank" type="primary">
                          <el-icon><Document /></el-icon> {{ file.name }}
                        </el-link>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 输入区域 -->
            <div class="chat-input">
              <div v-if="enableFileUpload" class="file-upload">
                <el-upload
                  :action="null"
                  :auto-upload="false"
                  :multiple="fileInputLimit > 1"
                  :limit="fileInputLimit"
                  :accept="fileInputAccept"
                  :on-change="handleFileChange"
                  :on-remove="handleFileRemove"
                  :file-list="uploadedFiles"
                >
                  <el-button type="primary" plain icon="Upload">上传文件</el-button>
                </el-upload>
              </div>
              <div class="input-area">
                <el-input
                  v-model="inputMessage"
                  type="textarea"
                  :rows="3"
                  placeholder="输入消息..."
                  resize="none"
                  @keydown.enter.prevent="handleSendMessage"
                />
                <el-button
                  type="primary"
                  :disabled="!inputMessage.trim() && uploadedFiles.length === 0"
                  :loading="isLoadingMessage"
                  @click="handleSendMessage"
                >发送</el-button>
              </div>
            </div>
          </template>
        </el-card>
      </el-col>
    </el-row>

    <!-- 重命名对话框 -->
    <el-dialog
      v-model="renameDialogVisible"
      title="重命名会话"
      width="30%"
      append-to-body
    >
      <el-input v-model="renameValue" placeholder="请输入会话名称" />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="renameDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmRename">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="AiChat">
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useAiStore } from '@/store/modules/ai';
import { marked } from 'marked';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';

const route = useRoute();
const router = useRouter();
const aiStore = useAiStore();

// 初始化marked配置
marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value;
    }
    return hljs.highlightAuto(code).value;
  },
  breaks: true
});

// 状态
const appId = ref('');
const inputMessage = ref('');
const messagesContainer = ref(null);
const lastScrollTop = ref(0);
const isLoadingMore = ref(false);
const uploadedFiles = ref([]);
const renameDialogVisible = ref(false);
const renameValue = ref('');
const currentRenameId = ref('');
const scrollInterval = ref(null);

// 计算属性
const appInfo = computed(() => aiStore.appInfo);
const messages = computed(() => aiStore.messages);
const conversationHistory = computed(() => aiStore.conversationHistory);
const currentConversationId = computed(() => aiStore.currentConversationId);
const isLoadingApp = computed(() => aiStore.isLoadingApp);
const isLoadingMessage = computed(() => aiStore.isLoadingMessage);
const isMessagesLoading = computed(() => aiStore.isMessagesLoading);
const hasMoreMessages = computed(() => aiStore.hasMoreMessages);
const hasMoreHistory = computed(() => aiStore.hasMoreHistory);
const showUserInputForm = computed(() => aiStore.showUserInputForm);
const showUserInputFormCancelBtn = computed(() => aiStore.showUserInputFormCancelBtn);
const userInputs = computed(() => aiStore.userInputs);
const userInputFormList = computed(() => aiStore.userInputFormList);
const enableFileUpload = computed(() => aiStore.enableFileUpload);
const fileInputAccept = computed(() => aiStore.fileInputAccept);
const fileInputLimit = computed(() => aiStore.fileInputLimit);

// 初始化
onMounted(async () => {
  appId.value = route.params.appid;
  if (appId.value) {
    aiStore.setAppId(appId.value);
    await aiStore.initAiApp();
  }
  scrollToBottom();
});

// 清理
onUnmounted(() => {
  if (scrollInterval.value) {
    clearInterval(scrollInterval.value);
    scrollInterval.value = null;
  }
  aiStore.clearAll();
});

// 监听消息加载状态
watch(isLoadingMessage, (newValue) => {
  if (newValue) {
    setupAutoScroll();
  } else {
    if (scrollInterval.value) {
      clearInterval(scrollInterval.value);
      scrollInterval.value = null;
    }
    nextTick(() => {
      scrollToBottom();
    });
  }
});

// 监听消息列表加载状态
watch(isMessagesLoading, (newValue) => {
  if (!newValue) {
    nextTick(() => {
      scrollToBottom();
    });
  }
});

// 监听当前会话ID
watch(currentConversationId, () => {
  nextTick(() => {
    scrollToBottom();
  });
});

// 设置自动滚动
const setupAutoScroll = () => {
  if (scrollInterval.value) {
    clearInterval(scrollInterval.value);
    scrollInterval.value = null;
  }

  if (isLoadingMessage.value) {
    scrollInterval.value = setInterval(scrollToBottom, 1000);
  }
};

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// 处理消息滚动
const handleMessagesScroll = (e) => {
  const target = e.target;
  const { scrollTop } = target;

  // 判断是否是向上滚动
  const isScrollingUp = scrollTop < lastScrollTop.value;
  lastScrollTop.value = scrollTop;

  // 当向上滚动到顶部时加载更多历史消息
  if (isScrollingUp && scrollTop < 50) {
    loadMoreMessages();
  }
};

// 加载更多消息
const loadMoreMessages = async () => {
  if (hasMoreMessages.value && !isLoadingMessage.value && !isLoadingMore.value) {
    isLoadingMore.value = true;

    // 获取当前第一条消息的DOM元素
    const firstMessage = messages.value?.[0];
    const messageElement = document.getElementById(`message-${firstMessage?.id}`);

    await aiStore.fetchMessages(true);

    nextTick(() => {
      // 滚动到之前的消息位置
      if (messageElement) {
        messageElement.scrollIntoView();
      }
      isLoadingMore.value = false;
    });
  }
};

// 加载更多会话
const loadMoreConversations = () => {
  aiStore.loadConversations(true);
};

// 开始新对话
const startNewConversation = () => {
  aiStore.startNewConversation();
  router.push(`/ai/chat/${appId.value}`);
};

// 根据用户输入开始对话
const startConversationByInputs = () => {
  aiStore.showUserInputForm = false;
};

// 处理发送消息
const handleSendMessage = () => {
  if (!inputMessage.value.trim() && uploadedFiles.value.length === 0) return;
  
  aiStore.sendMessage(inputMessage.value);
  inputMessage.value = '';
};

// 处理文件变更
const handleFileChange = (file) => {
  // 这里需要实现文件上传逻辑
  console.log('File changed:', file);
};

// 处理文件移除
const handleFileRemove = (file) => {
  // 这里需要实现文件移除逻辑
  console.log('File removed:', file);
};

// 处理下拉菜单命令
const handleCommand = (command, conversation) => {
  switch (command) {
    case 'rename':
      renameValue.value = conversation.name || '';
      currentRenameId.value = conversation.id;
      renameDialogVisible.value = true;
      break;
    case 'delete':
      ElMessageBox.confirm(
        '确定要删除这个会话吗？',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        aiStore.deleteConversation(conversation.id);
      }).catch(() => {});
      break;
  }
};

// 确认重命名
const confirmRename = () => {
  if (!renameValue.value.trim()) {
    ElMessage.warning('名称不能为空');
    return;
  }
  
  aiStore.renameConversation(currentRenameId.value, renameValue.value);
  renameDialogVisible.value = false;
};

// 格式化消息内容
const formatMessage = (content) => {
  if (!content) return '';
  return marked(content);
};

// 获取会话消息
const getMessages = (conversationId) => {
  aiStore.getMessages(conversationId);
};
</script>

<style scoped>
.chat-container {
  height: calc(100vh - 120px);
}

.chat-layout {
  height: 100%;
}

.sidebar-col, .chat-main-col {
  height: 100%;
}

.sidebar-card, .chat-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.conversation-list {
  overflow-y: auto;
  max-height: calc(100vh - 200px);
}

.conversation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 5px;
  cursor: pointer;
}

.conversation-item:hover {
  background-color: #f5f7fa;
}

.conversation-item.active {
  background-color: #ecf5ff;
}

.conversation-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.load-more {
  text-align: center;
  margin-top: 10px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  max-height: calc(100vh - 280px);
}

.empty-messages {
  text-align: center;
  color: #909399;
  padding: 20px;
}

.message-item {
  display: flex;
  margin-bottom: 15px;
}

.bot-message {
  flex-direction: row;
}

.user-message {
  flex-direction: row-reverse;
}

.message-avatar {
  margin: 0 10px;
}

.bot-avatar {
  background-color: #409EFF;
}

.user-avatar {
  background-color: #67C23A;
}

.message-content {
  max-width: 70%;
}

.bot-message .message-content {
  margin-right: auto;
}

.user-message .message-content {
  margin-left: auto;
}

.message-text {
  padding: 10px 15px;
  border-radius: 8px;
  word-break: break-word;
}

.bot-message .message-text {
  background-color: #f4f4f5;
}

.user-message .message-text {
  background-color: #ecf5ff;
  color: #409EFF;
}

.error-message {
  background-color: #fef0f0 !important;
  color: #f56c6c !important;
}

.message-files {
  margin-top: 8px;
}

.file-item {
  margin-bottom: 5px;
}

.chat-input {
  margin-top: 15px;
  border-top: 1px solid #ebeef5;
  padding-top: 15px;
}

.file-upload {
  margin-bottom: 10px;
}

.input-area {
  display: flex;
  align-items: flex-end;
}

.input-area .el-textarea {
  flex: 1;
  margin-right: 10px;
}

.loading-container {
  padding: 20px;
}

.loading-more {
  text-align: center;
  color: #909399;
  padding: 5px;
  font-size: 14px;
}

.empty-container {
  padding: 20px;
  text-align: center;
}

.user-input-form {
  padding: 20px;
}

/* 代码高亮样式 */
:deep(pre) {
  background-color: #f8f8f8;
  border-radius: 4px;
  padding: 10px;
  overflow-x: auto;
}

:deep(code) {
  font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
  font-size: 14px;
}

@media (max-width: 768px) {
  .sidebar-col {
    display: none;
  }
  
  .chat-main-col {
    width: 100%;
  }
  
  .message-content {
    max-width: 85%;
  }
}
</style>
