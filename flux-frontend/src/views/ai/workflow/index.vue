<template>
  <div class="app-container workflow-container">
    <el-row :gutter="20" class="workflow-layout">
      <!-- 左侧输入区域 -->
      <el-col :span="12" :xs="24" class="input-col">
        <el-card class="input-card">
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
                  <el-button type="primary" @click="startWorkflowByInputs">开始工作流</el-button>
                </el-form-item>
              </el-form>
            </div>
          </template>

          <template v-else>
            <!-- 输入区域 -->
            <div class="workflow-input">
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
                  :rows="8"
                  placeholder="输入工作流指令..."
                  resize="none"
                />
                <div class="action-buttons">
                  <el-button
                    type="primary"
                    :disabled="!inputMessage.trim() && uploadedFiles.length === 0"
                    :loading="isLoadingMessage"
                    @click="handleExecute"
                  >执行</el-button>
                  <el-button
                    v-if="workflowContent"
                    type="default"
                    @click="handleClear"
                  >清除</el-button>
                </div>
              </div>
            </div>
          </template>
        </el-card>
      </el-col>

      <!-- 右侧生成内容区域 -->
      <el-col :span="12" :xs="24" class="output-col">
        <el-card class="output-card">
          <template #header>
            <div class="card-header">
              <span>工作流结果</span>
              <div class="header-actions" v-if="workflowContent">
                <el-badge v-if="workflowContent" :value="workflowContent.length" type="primary">
                  <el-button
                    type="primary"
                    plain
                    size="small"
                    icon="CopyDocument"
                    @click="copyContent"
                  >复制</el-button>
                </el-badge>
                <el-button
                  type="primary"
                  plain
                  size="small"
                  icon="Download"
                  @click="downloadContent"
                >下载</el-button>
              </div>
            </div>
          </template>

          <div class="workflow-output">
            <div v-if="isLoadingMessage" class="loading-container">
              <el-skeleton :rows="10" animated />
            </div>
            <div v-else-if="!workflowContent" class="empty-output">
              <el-empty description="暂无工作流结果" />
            </div>
            <div v-else class="output-content" v-html="formatContent(workflowContent)"></div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup name="AiWorkflow">
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
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
const uploadedFiles = ref([]);
const isDrawerOpen = ref(false);

// 计算属性
const appInfo = computed(() => aiStore.appInfo);
const isLoadingApp = computed(() => aiStore.isLoadingApp);
const isLoadingMessage = computed(() => aiStore.isLoadingMessage);
const showUserInputForm = computed(() => aiStore.showUserInputForm);
const userInputs = computed(() => aiStore.userInputs);
const userInputFormList = computed(() => aiStore.userInputFormList);
const enableFileUpload = computed(() => aiStore.enableFileUpload);
const fileInputAccept = computed(() => aiStore.fileInputAccept);
const fileInputLimit = computed(() => aiStore.fileInputLimit);
const workflowContent = computed(() => aiStore.workflowContent);

// 初始化
onMounted(async () => {
  appId.value = route.params.appid;
  if (appId.value) {
    aiStore.setAppId(appId.value);
    aiStore.setType('workflow');
    await aiStore.initAiApp();
    aiStore.getCompletionSaved();
  }
});

// 清理
onUnmounted(() => {
  aiStore.clearAll();
});

// 监听工作流内容变化，自动打开抽屉（移动端）
watch(workflowContent, (newValue) => {
  if (newValue && window.innerWidth < 768) {
    isDrawerOpen.value = true;
  }
});

// 开始工作流
const startWorkflowByInputs = () => {
  aiStore.showUserInputForm = false;
};

// 处理执行
const handleExecute = () => {
  if (!inputMessage.value.trim() && uploadedFiles.value.length === 0) return;
  
  aiStore.executeWorkflow(inputMessage.value);
  // 不清空输入，方便用户修改后重新执行
};

// 处理清除
const handleClear = () => {
  aiStore.clearWorkflowContent();
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

// 复制内容
const copyContent = () => {
  if (!workflowContent.value) return;
  
  navigator.clipboard.writeText(workflowContent.value)
    .then(() => {
      ElMessage({
        message: '内容已复制到剪贴板',
        type: 'success',
        duration: 2000
      });
    })
    .catch(() => {
      ElMessage({
        message: '复制失败，请手动复制',
        type: 'error',
        duration: 2000
      });
    });
};

// 下载内容
const downloadContent = () => {
  if (!workflowContent.value) return;
  
  const blob = new Blob([workflowContent.value], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${appInfo.value?.name || 'workflow-result'}-${new Date().toISOString().slice(0, 10)}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};

// 格式化内容
const formatContent = (content) => {
  if (!content) return '';
  return marked(content);
};
</script>

<style scoped>
.workflow-container {
  height: calc(100vh - 120px);
}

.workflow-layout {
  height: 100%;
}

.input-col, .output-col {
  height: 100%;
}

.input-card, .output-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.workflow-input {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.file-upload {
  margin-bottom: 16px;
}

.input-area {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 16px;
}

.workflow-output {
  height: 100%;
  overflow-y: auto;
  padding: 16px;
}

.empty-output {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.output-content {
  white-space: pre-wrap;
  word-break: break-word;
}

.loading-container {
  padding: 20px;
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
  .input-col, .output-col {
    width: 100%;
  }
  
  .output-col {
    margin-top: 20px;
  }
}
</style>
