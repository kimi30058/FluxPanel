<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>AI应用</span>
          <el-button
            type="primary"
            icon="Plus"
            @click="handleCreateApp"
            v-hasPermi="['ai:application:add']"
          >
            创建应用
          </el-button>
        </div>
      </template>
      
      <el-row :gutter="16">
        <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="app in aiApps" :key="app.id">
          <div class="app-card-wrapper">
            <AppCard :app="app" @click="handleOpenApp(app)" />
          </div>
        </el-col>
      </el-row>
      
      <el-empty v-if="!aiApps.length" description="暂无应用" />
    </el-card>
    
    <!-- 创建应用对话框 -->
    <el-dialog
      v-model="createDialogVisible"
      title="创建AI应用"
      width="500px"
      append-to-body
    >
      <el-form
        ref="createFormRef"
        :model="createForm"
        :rules="createRules"
        label-width="100px"
      >
        <el-form-item label="应用名称" prop="name">
          <el-input v-model="createForm.name" placeholder="请输入应用名称" />
        </el-form-item>
        
        <el-form-item label="应用类型" prop="type">
          <el-select v-model="createForm.type" placeholder="请选择应用类型" style="width: 100%">
            <el-option label="传统模型" value="traditional" />
            <el-option label="DIFY应用" value="dify" />
            <el-option label="COZE应用" value="coze" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="应用描述" prop="description">
          <el-input
            v-model="createForm.description"
            type="textarea"
            placeholder="请输入应用描述"
            :rows="3"
          />
        </el-form-item>
        
        <el-form-item label="系统提示词" prop="system_prompt">
          <el-input
            v-model="createForm.system_prompt"
            type="textarea"
            placeholder="请输入系统提示词"
            :rows="5"
          />
        </el-form-item>
        
        <el-form-item label="标签" prop="tags">
          <el-select
            v-model="createForm.tags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="请选择或创建标签"
            style="width: 100%"
          >
            <el-option
              v-for="tag in defaultTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="图标背景色" prop="icon_bg_color">
          <el-color-picker v-model="createForm.icon_bg_color" />
        </el-form-item>
        
        <el-form-item label="是否启用" prop="is_enabled">
          <el-switch v-model="createForm.is_enabled" />
        </el-form-item>
        
        <!-- 传统模型特有配置 -->
        <template v-if="createForm.type === 'traditional'">
          <el-form-item label="提供商" prop="id_traditional_provider">
            <el-select
              v-model="createForm.id_traditional_provider"
              placeholder="请选择提供商"
              style="width: 100%"
              @change="handleProviderChange"
            >
              <el-option
                v-for="provider in providers"
                :key="provider.id"
                :label="provider.name"
                :value="provider.id"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="模型" prop="model">
            <el-select
              v-model="createForm.model"
              placeholder="请选择模型"
              style="width: 100%"
              :disabled="!createForm.id_traditional_provider"
            >
              <el-option
                v-for="model in availableModels"
                :key="model.id"
                :label="model.name"
                :value="model.id"
              />
            </el-select>
          </el-form-item>
        </template>
        
        <!-- DIFY应用特有配置 -->
        <template v-if="createForm.type === 'dify'">
          <el-form-item label="DIFY应用" prop="id_dify_app">
            <el-select
              v-model="createForm.id_dify_app"
              placeholder="请选择DIFY应用"
              style="width: 100%"
            >
              <el-option
                v-for="app in difyApps"
                :key="app.id"
                :label="app.app_id"
                :value="app.id"
              />
            </el-select>
          </el-form-item>
        </template>
        
        <!-- COZE应用特有配置 -->
        <template v-if="createForm.type === 'coze'">
          <el-form-item label="COZE应用" prop="id_coze_app">
            <el-select
              v-model="createForm.id_coze_app"
              placeholder="请选择COZE应用"
              style="width: 100%"
            >
              <el-option
                v-for="app in cozeApps"
                :key="app.id"
                :label="app.agent_id || app.workflow_id || '未命名'"
                :value="app.id"
              />
            </el-select>
          </el-form-item>
        </template>
        
        <!-- 上下文设置 -->
        <el-divider>上下文设置</el-divider>
        
        <el-form-item label="最大轮次" prop="max_context_turns">
          <el-input-number
            v-model="createForm.max_context_turns"
            :min="1"
            :max="100"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="最大Token" prop="max_tokens">
          <el-input-number
            v-model="createForm.max_tokens"
            :min="100"
            :max="100000"
            :step="100"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="保留系统提示词" prop="preserve_system_prompt">
          <el-switch v-model="createForm.preserve_system_prompt" />
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { useRouter } from 'vue-router'
import AppCard from '@/components/ai/AppCard.vue'
import { 
  getAIAppList, 
  createAIApp, 
  getTraditionalProviderList,
  getDifyAppList,
  getCozeAppList,
  getModelsByProviderAndType
} from '@/api/ai'
import type { AIApplication, TraditionalProvider, DifyApplication, CozeApplication } from '@/types/chat'

defineOptions({
  name: 'AIApplications'
})

const router = useRouter()
const aiApps = ref<AIApplication[]>([])
const providers = ref<TraditionalProvider[]>([])
const difyApps = ref<DifyApplication[]>([])
const cozeApps = ref<CozeApplication[]>([])
const availableModels = ref<any[]>([])
const createDialogVisible = ref(false)
const submitLoading = ref(false)
const createFormRef = ref<FormInstance>()

const defaultTags = ['聊天', '文档', '图像', '办公', '教育']

// 创建表单
const createForm = reactive({
  name: '',
  type: 'traditional',
  description: '',
  system_prompt: '',
  tags: [] as string[],
  icon_bg_color: '#e6f4ff',
  icon: 'default-icon.png',
  is_enabled: true,
  id_traditional_provider: undefined as number | undefined,
  id_dify_app: undefined as number | undefined,
  id_coze_app: undefined as number | undefined,
  model: '',
  max_context_turns: 10,
  max_tokens: 4000,
  preserve_system_prompt: true
})

// 表单验证规则
const createRules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入应用名称', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择应用类型', trigger: 'change' }
  ],
  id_traditional_provider: [
    { required: true, message: '请选择提供商', trigger: 'change' }
  ],
  id_dify_app: [
    { required: true, message: '请选择DIFY应用', trigger: 'change' }
  ],
  id_coze_app: [
    { required: true, message: '请选择COZE应用', trigger: 'change' }
  ]
})

// 初始化
onMounted(async () => {
  await fetchAIApps()
  await fetchProviders()
  await fetchDifyApps()
  await fetchCozeApps()
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

// 获取传统模型提供商列表
const fetchProviders = async () => {
  try {
    const { data } = await getTraditionalProviderList()
    if (data && Array.isArray(data.list)) {
      providers.value = data.list
    }
  } catch (error) {
    console.error('获取传统模型提供商列表失败:', error)
  }
}

// 获取DIFY应用列表
const fetchDifyApps = async () => {
  try {
    const { data } = await getDifyAppList()
    if (data && Array.isArray(data.list)) {
      difyApps.value = data.list
    }
  } catch (error) {
    console.error('获取DIFY应用列表失败:', error)
  }
}

// 获取COZE应用列表
const fetchCozeApps = async () => {
  try {
    const { data } = await getCozeAppList()
    if (data && Array.isArray(data.list)) {
      cozeApps.value = data.list
    }
  } catch (error) {
    console.error('获取COZE应用列表失败:', error)
  }
}

// 处理提供商变更
const handleProviderChange = async (providerId: number) => {
  if (!providerId) {
    availableModels.value = []
    return
  }
  
  const provider = providers.value.find(p => p.id === providerId)
  
  if (!provider) {
    availableModels.value = []
    return
  }
  
  try {
    const { data } = await getModelsByProviderAndType(provider.provider, 'llm')
    if (data && Array.isArray(data.models)) {
      availableModels.value = data.models
    }
  } catch (error) {
    console.error('获取模型列表失败:', error)
    availableModels.value = []
  }
}

// 创建应用
const handleCreateApp = () => {
  createForm.name = ''
  createForm.type = 'traditional'
  createForm.description = ''
  createForm.system_prompt = ''
  createForm.tags = []
  createForm.icon_bg_color = '#e6f4ff'
  createForm.icon = 'default-icon.png'
  createForm.is_enabled = true
  createForm.id_traditional_provider = undefined
  createForm.id_dify_app = undefined
  createForm.id_coze_app = undefined
  createForm.model = ''
  createForm.max_context_turns = 10
  createForm.max_tokens = 4000
  createForm.preserve_system_prompt = true
  
  createDialogVisible.value = true
}

// 提交创建表单
const submitCreateForm = async () => {
  if (!createFormRef.value) return
  
  await createFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    submitLoading.value = true
    
    try {
      const formData = { ...createForm }
      
      // 根据应用类型设置必要字段
      if (formData.type === 'traditional') {
        formData.id_dify_app = undefined
        formData.id_coze_app = undefined
      } else if (formData.type === 'dify') {
        formData.id_traditional_provider = undefined
        formData.id_coze_app = undefined
        formData.model = ''
      } else if (formData.type === 'coze') {
        formData.id_traditional_provider = undefined
        formData.id_dify_app = undefined
        formData.model = ''
      }
      
      const { data } = await createAIApp(formData)
      
      if (data) {
        ElMessage.success('创建成功')
        createDialogVisible.value = false
        
        // 刷新应用列表
        await fetchAIApps()
      }
    } catch (error: any) {
      ElMessage.error(error.message || '创建失败')
    } finally {
      submitLoading.value = false
    }
  })
}

// 打开应用
const handleOpenApp = (app: AIApplication) => {
  if (!app.is_enabled) {
    ElMessage.warning('该应用已禁用')
    return
  }
  
  router.push({
    path: '/ai/chat',
    query: {
      app_id: app.id.toString()
    }
  })
}
</script>

<style lang="scss" scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-card-wrapper {
  margin-bottom: 20px;
  height: 100%;
}

.el-empty {
  margin: 40px 0;
}
</style>
