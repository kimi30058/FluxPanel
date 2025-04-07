<template>
  <el-row :gutter="20">
    <el-col :xs="24" :sm="12" v-for="app in aiApps" :key="app.id">
      <el-card class="app-card" shadow="hover" @click="handleClick(app)">
        <div class="app-card-content">
          <div 
            class="app-icon" 
            :style="{ backgroundColor: app.iconBgColor }"
          >
            {{ app.icon }}
          </div>
          <div class="app-info">
            <div class="app-header">
              <h3 class="app-title">{{ app.name }}</h3>
              <el-tag size="small" type="info">{{ app.typeName }}</el-tag>
              <el-tag 
                size="small" 
                type="info" 
                v-for="tag in app.tags" 
                :key="tag" 
                class="ml-5"
              >
                {{ tag }}
              </el-tag>
            </div>
            <p class="app-description">{{ app.description }}</p>
          </div>
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>

<script setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';

const router = useRouter();

// AI应用配置
const aiApps = ref([
  {
    id: 'chat-assistant',
    name: '智能助手',
    typeName: '对话',
    icon: '💬',
    iconBgColor: '#409EFF',
    description: '一个智能的AI助手，可以回答问题、提供建议和帮助解决问题。',
    path: '/ai/chat/chat-assistant',
    tags: ['通用', '问答']
  },
  {
    id: 'code-helper',
    name: '代码助手',
    typeName: '对话',
    icon: '💻',
    iconBgColor: '#67C23A',
    description: '帮助编写、解释和优化代码的AI助手，支持多种编程语言。',
    path: '/ai/chat/code-helper',
    tags: ['编程', '开发']
  },
  {
    id: 'content-writer',
    name: '内容创作',
    typeName: '生成',
    icon: '✍️',
    iconBgColor: '#E6A23C',
    description: '帮助创作各类文本内容，包括文章、报告、广告文案等。',
    path: '/ai/completion/content-writer',
    tags: ['写作', '创作']
  },
  {
    id: 'data-analyzer',
    name: '数据分析',
    typeName: '工作流',
    icon: '📊',
    iconBgColor: '#F56C6C',
    description: '分析数据并生成见解，帮助理解数据趋势和模式。',
    path: '/ai/workflow/data-analyzer',
    tags: ['分析', '数据']
  }
]);

// 处理点击事件
const handleClick = (app) => {
  const token = localStorage.getItem('token');
  if (!token) {
    ElMessage({
      message: '请先登录',
      type: 'warning',
      duration: 2000
    });
    router.push('/login');
  } else {
    router.push(app.path);
  }
};
</script>

<style scoped>
.app-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.app-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.app-card-content {
  display: flex;
  gap: 16px;
}

.app-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
}

.app-info {
  flex: 1;
}

.app-header {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.app-title {
  margin: 0;
  margin-right: 8px;
  font-size: 18px;
  font-weight: 500;
}

.app-description {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.ml-5 {
  margin-left: 5px;
}
</style>
