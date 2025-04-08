<template>
  <div class="app-container">
    <el-row :gutter="20" class="chat-container">
      <!-- 聊天历史侧边栏 -->
      <el-col :span="6" class="chat-sidebar">
        <el-card class="chat-history-card">
          <ChatHistory
            :history="chatHistory"
            :current-session-id="currentChatId"
            :provider="currentProvider"
            @select-session="handleSelectSession"
            @create-new="handleCreateNew"
          />
        </el-card>
      </el-col>
      
      <!-- 聊天窗口 -->
      <el-col :span="18" class="chat-main">
        <el-card v-if="currentChatId" class="chat-window-card">
          <template #header>
            <div class="chat-header">
              <div class="chat-title">
                <span v-if="!isEditingTitle">{{ currentChatTitle }}</span>
                <el-input
                  v-else
                  v-model="editingTitle"
                  size="small"
                  @blur="handleSaveTitle"
                  @keyup.enter="handleSaveTitle"
                  ref="titleInput"
                />
                <el-button
                  v-if="!isEditingTitle"
                  type="text"
                  icon="Edit"
                  @click="handleEditTitle"
                />
              </div>
              <div class="chat-actions">
                <el-button
                  type="primary"
                  size="small"
                  @click="handleShowSettings"
                  v-hasPermi="['ai:chat:edit']"
                >
                  设置
                </el-button>
              </div>
            </div>
          </template>
          
          <ChatWindow
            :messages="messages"
            :provider="currentProvider"
          />
        </el-card>
        
        <el-empty v-else description="选择或创建一个聊天会话" />
      </el-col>
    </el-row>
    
    <!-- 创建聊天会话对话框 -->
    <el-dialog
      v-model="createDialogVisible"
      title="创建聊天会话"
      width="500px"
      append-to-body
    >
      <el-form
        ref="createFormRef"
        :model="createForm"
        :rules="createRules"
        label-width="100px"
      >
        <el-form-item label="会话标题" prop="title">
          <el-input v-model="createForm.title" placeholder="请输入会话标题" />
        </el-form-item>
        
        <el-form-item label="会话类型" prop="chat_type">
          <el-select v-model="createForm.chat_type" placeholder="请选择会话类型" style="width: 100%">
            <el-option label="AI对话" value="ai" />
            <el-option label="普通聊天" value="normal" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="AI应用" prop="ai_application_id" v-if="createForm.chat_type === 'ai'">
          <el-select
            v-model="createForm.ai_application_id"
            placeholder="请选择AI应用"
            style="width: 100%"
            @change="handleAppChange"
          >
            <el-option
              v-for="app in aiApps"
              :key="app.id"
              :label="app.name"
              :value="app.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="系统提示词" prop="system_prompt">
          <el-input
            v-model="createForm.system_prompt"
            type="textarea"
            placeholder="请输入系统提示词"
            :rows="5"
          />
        </el-form-item>
        
        <el-form-item label="会话描述" prop="description">
          <el-input
            v-model="createForm.description"
            type="textarea"
            placeholder="请输入会话描述"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="createDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitCreateForm" :loading="submitLoading">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 会话设置对话框 -->
    <el-dialog
      v-model="settingsDialogVisible"
      title="会话设置"
      width="500px"
      append-to-body
    >
      <el-form
        ref="settingsFormRef"
        :model="settingsForm"
        label-width="140px"
      >
        <el-form-item label="系统提示词" prop="system_prompt">
          <el-input
            v-model="settingsForm.system_prompt"
            type="textarea"
            placeholder="请输入系统提示词"
            :rows="5"
          />
        </el-form-item>
        
        <el-form-item label="最大上下文轮次" prop="max_context_turns">
          <el-input-number
            v-model="settingsForm.max_context_turns"
            :min="1"
            :max="100"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="最大Token数" prop="max_tokens">
          <el-input-number
            v-model="settingsForm.max_tokens"
            :min="100"
            :max="100000"
            :step="100"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="保留系统提示词" prop="preserve_system_prompt">
          <el-switch v-model="settingsForm.preserve_system_prompt" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="settingsDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitSettingsForm" :loading="submitLoading">
            保存
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { useChatStore, AIProvider } from '@/store/modules/chat'
import { storeToRefs } from 'pinia'
import ChatHistory from '@/components/ai/chat/ChatHistory.vue'
import ChatWindow from '@/components/ai/chat/ChatWindow.vue'
import { 
  getAIAppList, 
  getChatById, 
  createChat, 
  renameChat,
  getAppContextSettings,
  updateAppContextSettings
} from '@/api/ai'
import type { AIApp } from '@/api/ai'

defineOptions({
  name: 'AIChat'
})

const chatStore = useChatStore()
const { messages, chatHistory, currentChatId, isLoadingMessage } = storeToRefs(chatStore)

// 当前聊天会话标题
const currentChatTitle = ref('')
const isEditingTitle = ref(false)
const editingTitle = ref('')
const titleInput = ref<HTMLInputElement>()

// 当前提供商类型
const currentProvider = ref<AIProvider>(AIProvider.DIFY)

// AI应用列表
const aiApps = ref<AIApp[]>([])

// 创建聊天会话对话框
const createDialogVisible = ref(false)
const createFormRef = ref<FormInstance>()
const submitLoading = ref(false)

// 会话设置对话框
const settingsDialogVisible = ref(false)
const settingsFormRef = ref<FormInstance>()
const settingsForm = reactive({
  system_prompt: '',
  max_context_turns: 10,
  max_tokens: 4000,
  preserve_system_prompt: true
})

// 创建聊天会话表单
const createForm = reactive({
  title: '',
  chat_type: 'ai',
  ai_application_id: undefined as number | undefined,
  system_prompt: '',
  description: ''
})

// 表单验证规则
const createRules = reactive<FormRules>({
  title: [
    { required: true, message: '请输入会话标题', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  chat_type: [
    { required: true, message: '请选择会话类型', trigger: 'change' }
  ],
  ai_application_id: [
    { required: true, message: '请选择AI应用', trigger: 'change' }
  ]
})

// 初始化
onMounted(async () => {
  await fetchAIApps()
  await fetchChatHistory()
})

// 获取AI应用列表
const fetchAIApps = async () => {
  try {
    const { data } = await getAIAppList()
    if (data && Array.isArray(data.list)) {
      aiApps.value = data.list
    }
  } catch (error) {
    console.error('获取AI应用列表失败:', error)
  }
}

// 获取聊天历史
const fetchChatHistory = async () => {
  await chatStore.fetchChatHistory()
  
  // 如果有聊天历史，默认选择第一个
  if (chatHistory.value.length > 0 && !currentChatId.value) {
    handleSelectSession(chatHistory.value[0].id)
  }
}

// 选择聊天会话
const handleSelectSession = async (id: string) => {
  if (id === currentChatId.value) return
  
  chatStore.clearMessages()
  
  try {
    // 获取聊天会话详情
    const { data } = await getChatById(parseInt(id))
    if (data) {
      currentChatTitle.value = data.title
      
      // 设置提供商类型
      if (data.ai_application?.type === 'dify') {
        currentProvider.value = AIProvider.DIFY
      } else if (data.ai_application?.type === 'coze') {
        currentProvider.value = AIProvider.COZE
      } else {
        currentProvider.value = AIProvider.TRADITIONAL
      }
      
      // 获取聊天消息
      await chatStore.fetchChatMessages({ chat_id: id })
    }
  } catch (error) {
    console.error('获取聊天会话详情失败:', error)
    ElMessage.error('获取聊天会话详情失败')
  }
}

// 创建新聊天会话
const handleCreateNew = () => {
  createForm.title = '新的对话'
  createForm.chat_type = 'ai'
  createForm.ai_application_id = undefined
  createForm.system_prompt = ''
  createForm.description = ''
  
  createDialogVisible.value = true
}

// 提交创建表单
const submitCreateForm = async () => {
  if (!createFormRef.value) return
  
  await createFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    submitLoading.value = true
    
    try {
      const { data } = await createChat(createForm)
      
      if (data) {
        ElMessage.success('创建成功')
        createDialogVisible.value = false
        
        // 刷新聊天历史
        await fetchChatHistory()
        
        // 选择新创建的会话
        handleSelectSession(data.id.toString())
      }
    } catch (error: any) {
      ElMessage.error(error.message || '创建失败')
    } finally {
      submitLoading.value = false
    }
  })
}

// 编辑会话标题
const handleEditTitle = () => {
  isEditingTitle.value = true
  editingTitle.value = currentChatTitle.value
  
  nextTick(() => {
    titleInput.value?.focus()
  })
}

// 保存会话标题
const handleSaveTitle = async () => {
  if (!editingTitle.value.trim() || !currentChatId.value) {
    isEditingTitle.value = false
    return
  }
  
  try {
    await renameChat(parseInt(currentChatId.value), { title: editingTitle.value })
    
    currentChatTitle.value = editingTitle.value
    isEditingTitle.value = false
    
    // 刷新聊天历史
    await fetchChatHistory()
  } catch (error) {
    console.error('重命名失败:', error)
    ElMessage.error('重命名失败')
  }
}

// 显示会话设置
const handleShowSettings = async () => {
  if (!currentChatId.value) return
  
  try {
    const { data } = await getAppContextSettings(parseInt(currentChatId.value))
    
    if (data) {
      settingsForm.system_prompt = data.system_prompt || ''
      settingsForm.max_context_turns = data.max_context_turns || 10
      settingsForm.max_tokens = data.max_tokens || 4000
      settingsForm.preserve_system_prompt = data.preserve_system_prompt !== false
    }
    
    settingsDialogVisible.value = true
  } catch (error) {
    console.error('获取会话设置失败:', error)
    ElMessage.error('获取会话设置失败')
  }
}

// 提交会话设置
const submitSettingsForm = async () => {
  if (!currentChatId.value) return
  
  submitLoading.value = true
  
  try {
    await updateAppContextSettings(parseInt(currentChatId.value), settingsForm)
    
    ElMessage.success('保存成功')
    settingsDialogVisible.value = false
  } catch (error) {
    console.error('保存会话设置失败:', error)
    ElMessage.error('保存会话设置失败')
  } finally {
    submitLoading.value = false
  }
}

// 应用变更处理
const handleAppChange = async (appId: number) => {
  const app = aiApps.value.find(a => a.id === appId)
  
  if (app) {
    createForm.system_prompt = app.system_prompt || ''
  }
}
</script>

<style lang="scss" scoped>
.chat-container {
  height: calc(100vh - 180px);
  min-height: 500px;
  
  .chat-sidebar {
    height: 100%;
    
    .chat-history-card {
      height: 100%;
      
      :deep(.el-card__body) {
        height: calc(100% - 60px);
        padding: 0;
      }
    }
  }
  
  .chat-main {
    height: 100%;
    
    .chat-window-card {
      height: 100%;
      
      :deep(.el-card__body) {
        height: calc(100% - 60px);
        padding: 0;
      }
    }
    
    .chat-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .chat-title {
        display: flex;
        align-items: center;
        gap: 8px;
        
        .el-input {
          max-width: 300px;
        }
      }
    }
  }
}

.el-empty {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>
