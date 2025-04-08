<template>
  <div class="app-container">
    <el-tabs v-model="activeTab" type="border-card">
      <!-- 传统模型提供商 -->
      <el-tab-pane label="传统模型提供商" name="traditional">
        <template #label>
          <span>
            <el-icon><Connection /></el-icon>
            传统模型提供商
          </span>
        </template>
        
        <div class="tab-toolbar">
          <el-button
            type="primary"
            icon="Plus"
            @click="handleCreateTraditional"
            v-hasPermi="['ai:provider:add']"
          >
            添加提供商
          </el-button>
        </div>
        
        <el-table
          v-loading="traditionalLoading"
          :data="traditionalProviders"
          style="width: 100%"
        >
          <el-table-column prop="name" label="名称" min-width="120" />
          <el-table-column prop="provider" label="提供商类型" min-width="120" />
          <el-table-column label="API密钥" min-width="180">
            <template #default="scope">
              <el-tag type="info">{{ maskApiKey(scope.row.api_key) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="base_url" label="API基础URL" min-width="180" />
          <el-table-column label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
                {{ scope.row.is_active ? '启用' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button
                link
                type="primary"
                icon="Edit"
                @click="handleEditTraditional(scope.row)"
                v-hasPermi="['ai:provider:edit']"
              >
                编辑
              </el-button>
              <el-button
                link
                type="danger"
                icon="Delete"
                @click="handleDeleteTraditional(scope.row)"
                v-hasPermi="['ai:provider:remove']"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      
      <!-- DIFY应用 -->
      <el-tab-pane label="DIFY应用" name="dify">
        <template #label>
          <span>
            <el-icon><ChatDotRound /></el-icon>
            DIFY应用
          </span>
        </template>
        
        <div class="tab-toolbar">
          <el-button
            type="primary"
            icon="Plus"
            @click="handleCreateDify"
            v-hasPermi="['ai:provider:add']"
          >
            添加DIFY应用
          </el-button>
        </div>
        
        <el-table
          v-loading="difyLoading"
          :data="difyApps"
          style="width: 100%"
        >
          <el-table-column prop="app_id" label="应用ID" min-width="180" />
          <el-table-column label="API密钥" min-width="180">
            <template #default="scope">
              <el-tag type="info">{{ maskApiKey(scope.row.api_key) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="api_base" label="API基础URL" min-width="180" />
          <el-table-column prop="conversation_mode" label="对话模式" width="120" />
          <el-table-column prop="response_mode" label="响应模式" width="120" />
          <el-table-column label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
                {{ scope.row.is_active ? '启用' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button
                link
                type="primary"
                icon="Edit"
                @click="handleEditDify(scope.row)"
                v-hasPermi="['ai:provider:edit']"
              >
                编辑
              </el-button>
              <el-button
                link
                type="danger"
                icon="Delete"
                @click="handleDeleteDify(scope.row)"
                v-hasPermi="['ai:provider:remove']"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      
      <!-- COZE应用 -->
      <el-tab-pane label="COZE应用" name="coze">
        <template #label>
          <span>
            <el-icon><ChatLineRound /></el-icon>
            COZE应用
          </span>
        </template>
        
        <div class="tab-toolbar">
          <el-button
            type="primary"
            icon="Plus"
            @click="handleCreateCoze"
            v-hasPermi="['ai:provider:add']"
          >
            添加COZE应用
          </el-button>
        </div>
        
        <el-table
          v-loading="cozeLoading"
          :data="cozeApps"
          style="width: 100%"
        >
          <el-table-column label="应用ID" min-width="180">
            <template #default="scope">
              {{ scope.row.agent_id || scope.row.workflow_id || '未设置' }}
            </template>
          </el-table-column>
          <el-table-column label="API密钥" min-width="180">
            <template #default="scope">
              <el-tag type="info">{{ maskApiKey(scope.row.api_key) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
                {{ scope.row.is_active ? '启用' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button
                link
                type="primary"
                icon="Edit"
                @click="handleEditCoze(scope.row)"
                v-hasPermi="['ai:provider:edit']"
              >
                编辑
              </el-button>
              <el-button
                link
                type="danger"
                icon="Delete"
                @click="handleDeleteCoze(scope.row)"
                v-hasPermi="['ai:provider:remove']"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 传统模型提供商对话框 -->
    <el-dialog
      v-model="traditionalDialogVisible"
      :title="traditionalForm.id ? '编辑提供商' : '添加提供商'"
      width="500px"
      append-to-body
    >
      <el-form
        ref="traditionalFormRef"
        :model="traditionalForm"
        :rules="traditionalRules"
        label-width="100px"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="traditionalForm.name" placeholder="请输入提供商名称" />
        </el-form-item>
        
        <el-form-item label="提供商类型" prop="provider">
          <el-select v-model="traditionalForm.provider" placeholder="请选择提供商类型" style="width: 100%">
            <el-option label="OpenAI" value="openai" />
            <el-option label="Azure OpenAI" value="azure_openai" />
            <el-option label="Anthropic" value="anthropic" />
            <el-option label="Google" value="google" />
            <el-option label="Hugging Face" value="huggingface" />
            <el-option label="Baidu" value="baidu" />
            <el-option label="Alibaba" value="alibaba" />
            <el-option label="Tencent" value="tencent" />
            <el-option label="Zhipu" value="zhipu" />
            <el-option label="Minimax" value="minimax" />
            <el-option label="Moonshot" value="moonshot" />
            <el-option label="Ollama" value="ollama" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="API密钥" prop="api_key">
          <el-input
            v-model="traditionalForm.api_key"
            placeholder="请输入API密钥"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="API基础URL" prop="base_url">
          <el-input
            v-model="traditionalForm.base_url"
            placeholder="请输入API基础URL（可选）"
          />
        </el-form-item>
        
        <el-form-item label="是否启用" prop="is_active">
          <el-switch v-model="traditionalForm.is_active" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="traditionalDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitTraditionalForm" :loading="submitLoading">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- DIFY应用对话框 -->
    <el-dialog
      v-model="difyDialogVisible"
      :title="difyForm.id ? '编辑DIFY应用' : '添加DIFY应用'"
      width="500px"
      append-to-body
    >
      <el-form
        ref="difyFormRef"
        :model="difyForm"
        :rules="difyRules"
        label-width="100px"
      >
        <el-form-item label="应用ID" prop="app_id">
          <el-input v-model="difyForm.app_id" placeholder="请输入DIFY应用ID" />
        </el-form-item>
        
        <el-form-item label="API密钥" prop="api_key">
          <el-input
            v-model="difyForm.api_key"
            placeholder="请输入API密钥"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="API基础URL" prop="api_base">
          <el-input
            v-model="difyForm.api_base"
            placeholder="请输入API基础URL"
          />
        </el-form-item>
        
        <el-form-item label="对话模式" prop="conversation_mode">
          <el-select v-model="difyForm.conversation_mode" placeholder="请选择对话模式" style="width: 100%">
            <el-option label="聊天模式" value="chat" />
            <el-option label="完成模式" value="completion" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="响应模式" prop="response_mode">
          <el-select v-model="difyForm.response_mode" placeholder="请选择响应模式" style="width: 100%">
            <el-option label="阻塞模式" value="blocking" />
            <el-option label="流式模式" value="streaming" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="是否启用" prop="is_active">
          <el-switch v-model="difyForm.is_active" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="difyDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitDifyForm" :loading="submitLoading">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- COZE应用对话框 -->
    <el-dialog
      v-model="cozeDialogVisible"
      :title="cozeForm.id ? '编辑COZE应用' : '添加COZE应用'"
      width="500px"
      append-to-body
    >
      <el-form
        ref="cozeFormRef"
        :model="cozeForm"
        :rules="cozeRules"
        label-width="100px"
      >
        <el-form-item label="Agent ID" prop="agent_id">
          <el-input v-model="cozeForm.agent_id" placeholder="请输入Agent ID（可选）" />
        </el-form-item>
        
        <el-form-item label="工作流ID" prop="workflow_id">
          <el-input v-model="cozeForm.workflow_id" placeholder="请输入工作流ID（可选）" />
        </el-form-item>
        
        <el-form-item label="API密钥" prop="api_key">
          <el-input
            v-model="cozeForm.api_key"
            placeholder="请输入API密钥"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="是否启用" prop="is_active">
          <el-switch v-model="cozeForm.is_active" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="cozeDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitCozeForm" :loading="submitLoading">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, FormInstance, FormRules } from 'element-plus'
import { 
  getTraditionalProviderList, 
  getTraditionalProviderById, 
  createTraditionalProvider, 
  updateTraditionalProvider, 
  deleteTraditionalProvider,
  getDifyAppList,
  getDifyAppById,
  createDifyApp,
  updateDifyApp,
  deleteDifyApp,
  getCozeAppList,
  getCozeAppById,
  createCozeApp,
  updateCozeApp,
  deleteCozeApp
} from '@/api/ai'
import { Connection, ChatDotRound, ChatLineRound } from '@element-plus/icons-vue'
import type { TraditionalProvider, DifyApplication, CozeApplication } from '@/types/chat'

defineOptions({
  name: 'AIProviders'
})

const activeTab = ref('traditional')
const traditionalLoading = ref(false)
const difyLoading = ref(false)
const cozeLoading = ref(false)
const submitLoading = ref(false)

// 传统模型提供商
const traditionalProviders = ref<TraditionalProvider[]>([])
const traditionalDialogVisible = ref(false)
const traditionalFormRef = ref<FormInstance>()
const traditionalForm = reactive({
  id: undefined as number | undefined,
  name: '',
  provider: '',
  api_key: '',
  base_url: '',
  is_active: true
})

// DIFY应用
const difyApps = ref<DifyApplication[]>([])
const difyDialogVisible = ref(false)
const difyFormRef = ref<FormInstance>()
const difyForm = reactive({
  id: undefined as number | undefined,
  app_id: '',
  api_key: '',
  api_base: 'www.ai-agent.chat/v1',
  conversation_mode: 'chat',
  response_mode: 'blocking',
  is_active: true
})

// COZE应用
const cozeApps = ref<CozeApplication[]>([])
const cozeDialogVisible = ref(false)
const cozeFormRef = ref<FormInstance>()
const cozeForm = reactive({
  id: undefined as number | undefined,
  agent_id: '',
  workflow_id: '',
  api_key: '',
  config: {},
  is_active: true
})

// 表单验证规则
const traditionalRules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入提供商名称', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  provider: [
    { required: true, message: '请选择提供商类型', trigger: 'change' }
  ],
  api_key: [
    { required: true, message: '请输入API密钥', trigger: 'blur' }
  ]
})

const difyRules = reactive<FormRules>({
  app_id: [
    { required: true, message: '请输入DIFY应用ID', trigger: 'blur' }
  ],
  api_key: [
    { required: true, message: '请输入API密钥', trigger: 'blur' }
  ],
  api_base: [
    { required: true, message: '请输入API基础URL', trigger: 'blur' }
  ]
})

const cozeRules = reactive<FormRules>({
  api_key: [
    { required: true, message: '请输入API密钥', trigger: 'blur' }
  ]
})

// 初始化
onMounted(async () => {
  await fetchTraditionalProviders()
  await fetchDifyApps()
  await fetchCozeApps()
})

// 获取传统模型提供商列表
const fetchTraditionalProviders = async () => {
  try {
    traditionalLoading.value = true
    const { data } = await getTraditionalProviderList()
    if (data && Array.isArray(data.list)) {
      traditionalProviders.value = data.list
    }
  } catch (error) {
    console.error('获取传统模型提供商列表失败:', error)
  } finally {
    traditionalLoading.value = false
  }
}

// 获取DIFY应用列表
const fetchDifyApps = async () => {
  try {
    difyLoading.value = true
    const { data } = await getDifyAppList()
    if (data && Array.isArray(data.list)) {
      difyApps.value = data.list
    }
  } catch (error) {
    console.error('获取DIFY应用列表失败:', error)
  } finally {
    difyLoading.value = false
  }
}

// 获取COZE应用列表
const fetchCozeApps = async () => {
  try {
    cozeLoading.value = true
    const { data } = await getCozeAppList()
    if (data && Array.isArray(data.list)) {
      cozeApps.value = data.list
    }
  } catch (error) {
    console.error('获取COZE应用列表失败:', error)
  } finally {
    cozeLoading.value = false
  }
}

// 掩码API密钥
const maskApiKey = (apiKey: string) => {
  if (!apiKey) return ''
  if (apiKey.length <= 8) return '*'.repeat(apiKey.length)
  return apiKey.substring(0, 4) + '*'.repeat(apiKey.length - 8) + apiKey.substring(apiKey.length - 4)
}

// 创建传统模型提供商
const handleCreateTraditional = () => {
  traditionalForm.id = undefined
  traditionalForm.name = ''
  traditionalForm.provider = ''
  traditionalForm.api_key = ''
  traditionalForm.base_url = ''
  traditionalForm.is_active = true
  
  traditionalDialogVisible.value = true
}

// 编辑传统模型提供商
const handleEditTraditional = async (row: TraditionalProvider) => {
  try {
    const { data } = await getTraditionalProviderById(row.id)
    if (data) {
      traditionalForm.id = data.id
      traditionalForm.name = data.name
      traditionalForm.provider = data.provider
      traditionalForm.api_key = data.api_key
      traditionalForm.base_url = data.base_url || ''
      traditionalForm.is_active = data.is_active
      
      traditionalDialogVisible.value = true
    }
  } catch (error) {
    console.error('获取传统模型提供商详情失败:', error)
    ElMessage.error('获取传统模型提供商详情失败')
  }
}

// 删除传统模型提供商
const handleDeleteTraditional = (row: TraditionalProvider) => {
  ElMessageBox.confirm(
    `确定要删除提供商 ${row.name} 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteTraditionalProvider(row.id)
      ElMessage.success('删除成功')
      await fetchTraditionalProviders()
    } catch (error) {
      console.error('删除传统模型提供商失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

// 提交传统模型提供商表单
const submitTraditionalForm = async () => {
  if (!traditionalFormRef.value) return
  
  await traditionalFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    submitLoading.value = true
    
    try {
      if (traditionalForm.id) {
        await updateTraditionalProvider(traditionalForm.id, traditionalForm)
        ElMessage.success('更新成功')
      } else {
        await createTraditionalProvider(traditionalForm)
        ElMessage.success('创建成功')
      }
      
      traditionalDialogVisible.value = false
      await fetchTraditionalProviders()
    } catch (error: any) {
      ElMessage.error(error.message || (traditionalForm.id ? '更新失败' : '创建失败'))
    } finally {
      submitLoading.value = false
    }
  })
}

// 创建DIFY应用
const handleCreateDify = () => {
  difyForm.id = undefined
  difyForm.app_id = ''
  difyForm.api_key = ''
  difyForm.api_base = 'www.ai-agent.chat/v1'
  difyForm.conversation_mode = 'chat'
  difyForm.response_mode = 'blocking'
  difyForm.is_active = true
  
  difyDialogVisible.value = true
}

// 编辑DIFY应用
const handleEditDify = async (row: DifyApplication) => {
  try {
    const { data } = await getDifyAppById(row.id)
    if (data) {
      difyForm.id = data.id
      difyForm.app_id = data.app_id
      difyForm.api_key = data.api_key
      difyForm.api_base = data.api_base || 'www.ai-agent.chat/v1'
      difyForm.conversation_mode = data.conversation_mode || 'chat'
      difyForm.response_mode = data.response_mode || 'blocking'
      difyForm.is_active = data.is_active
      
      difyDialogVisible.value = true
    }
  } catch (error) {
    console.error('获取DIFY应用详情失败:', error)
    ElMessage.error('获取DIFY应用详情失败')
  }
}

// 删除DIFY应用
const handleDeleteDify = (row: DifyApplication) => {
  ElMessageBox.confirm(
    `确定要删除DIFY应用 ${row.app_id} 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteDifyApp(row.id)
      ElMessage.success('删除成功')
      await fetchDifyApps()
    } catch (error) {
      console.error('删除DIFY应用失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

// 提交DIFY应用表单
const submitDifyForm = async () => {
  if (!difyFormRef.value) return
  
  await difyFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    submitLoading.value = true
    
    try {
      if (difyForm.id) {
        await updateDifyApp(difyForm.id, difyForm)
        ElMessage.success('更新成功')
      } else {
        await createDifyApp(difyForm)
        ElMessage.success('创建成功')
      }
      
      difyDialogVisible.value = false
      await fetchDifyApps()
    } catch (error: any) {
      ElMessage.error(error.message || (difyForm.id ? '更新失败' : '创建失败'))
    } finally {
      submitLoading.value = false
    }
  })
}

// 创建COZE应用
const handleCreateCoze = () => {
  cozeForm.id = undefined
  cozeForm.agent_id = ''
  cozeForm.workflow_id = ''
  cozeForm.api_key = ''
  cozeForm.config = {}
  cozeForm.is_active = true
  
  cozeDialogVisible.value = true
}

// 编辑COZE应用
const handleEditCoze = async (row: CozeApplication) => {
  try {
    const { data } = await getCozeAppById(row.id)
    if (data) {
      cozeForm.id = data.id
      cozeForm.agent_id = data.agent_id || ''
      cozeForm.workflow_id = data.workflow_id || ''
      cozeForm.api_key = data.api_key
      cozeForm.config = data.config || {}
      cozeForm.is_active = data.is_active
      
      cozeDialogVisible.value = true
    }
  } catch (error) {
    console.error('获取COZE应用详情失败:', error)
    ElMessage.error('获取COZE应用详情失败')
  }
}

// 删除COZE应用
const handleDeleteCoze = (row: CozeApplication) => {
  ElMessageBox.confirm(
    `确定要删除COZE应用 ${row.agent_id || row.workflow_id || row.id} 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteCozeApp(row.id)
      ElMessage.success('删除成功')
      await fetchCozeApps()
    } catch (error) {
      console.error('删除COZE应用失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

// 提交COZE应用表单
const submitCozeForm = async () => {
  if (!cozeFormRef.value) return
  
  await cozeFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    submitLoading.value = true
    
    try {
      if (cozeForm.id) {
        await updateCozeApp(cozeForm.id, cozeForm)
        ElMessage.success('更新成功')
      } else {
        await createCozeApp(cozeForm)
        ElMessage.success('创建成功')
      }
      
      cozeDialogVisible.value = false
      await fetchCozeApps()
    } catch (error: any) {
      ElMessage.error(error.message || (cozeForm.id ? '更新失败' : '创建失败'))
    } finally {
      submitLoading.value = false
    }
  })
}
</script>

<style lang="scss" scoped>
.tab-toolbar {
  margin-bottom: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>
