<template>
  <div class="chat-history-container">
    <div class="header">
      <div class="title">聊天历史</div>
      <el-button 
        type="primary" 
        size="small" 
        @click="emit('create-new')"
        :disabled="loading"
      >
        新建对话
      </el-button>
    </div>
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="3" animated />
    </div>
    
    <el-empty v-else-if="!history.length" description="暂无聊天记录" />
    
    <div v-else class="history-list">
      <div
        v-for="item in history"
        :key="item.id"
        class="history-item"
        :class="{ active: item.id === currentSessionId }"
        @click="selectSession(item.id)"
      >
        <el-icon><ChatDotSquare /></el-icon>
        <div class="content">
          <div class="title">{{ item.title }}</div>
          <div class="time">{{ formatTime(item.lastTime) }}</div>
        </div>
        <div class="actions">
          <el-popconfirm
            title="确定要删除这个对话吗？"
            @confirm="handleDelete(item.id)"
            width="200"
            confirm-button-text="确定"
            cancel-button-text="取消"
          >
            <template #reference>
              <el-icon @click.stop><Delete /></el-icon>
            </template>
          </el-popconfirm>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { ChatDotSquare, Delete } from '@element-plus/icons-vue'
import { AIProvider } from '@/store/modules/chat'
import { deleteChat } from '@/api/ai'
import type { ChatSession } from '@/types/chat'

defineOptions({
  name: 'ChatHistory'
})

const props = defineProps<{
  history: ChatSession[]
  currentSessionId: string
  provider?: AIProvider
}>()

const emit = defineEmits<{
  (e: 'select-session', id: string): void
  (e: 'create-new'): void
}>()

const loading = ref(false)

// 选择会话
const selectSession = (id: string) => {
  emit('select-session', id)
}

// 删除会话
const handleDelete = async (id: string) => {
  try {
    loading.value = true
    await deleteChat(parseInt(id))
    ElMessage.success('删除成功')
    emit('create-new') // 触发刷新
  } catch (error: any) {
    ElMessage.error(error.message || '删除失败')
  } finally {
    loading.value = false
  }
}

// 格式化时间
const formatTime = (timeStr: string) => {
  if (!timeStr) return ''
  
  const date = new Date(timeStr)
  const now = new Date()
  
  // 如果是今天，只显示时间
  if (date.toDateString() === now.toDateString()) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }
  
  // 如果是今年，显示月日和时间
  if (date.getFullYear() === now.getFullYear()) {
    return date.toLocaleDateString([], { month: 'numeric', day: 'numeric' }) + ' ' + 
           date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }
  
  // 显示完整日期
  return date.toLocaleDateString()
}
</script>

<style lang="scss" scoped>
.chat-history-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 15px;
    border-bottom: 1px solid #eee;
    
    .title {
      font-weight: bold;
      font-size: 16px;
    }
  }
  
  .loading-container {
    padding: 20px 15px;
  }
  
  .history-list {
    flex: 1;
    overflow-y: auto;
    padding: 10px 0;
    
    .history-item {
      display: flex;
      align-items: center;
      padding: 10px 15px;
      cursor: pointer;
      transition: background-color 0.2s ease;
      
      &:hover {
        background-color: #f0f2f5;
      }
      
      &.active {
        background-color: #e6f4ff;
      }
      
      .el-icon {
        color: var(--el-color-primary);
        margin-right: 10px;
        font-size: 18px;
      }
      
      .content {
        flex: 1;
        min-width: 0;
        
        .title {
          font-size: 14px;
          margin-bottom: 4px;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        
        .time {
          font-size: 12px;
          color: var(--el-text-color-secondary);
        }
      }
      
      .actions {
        opacity: 0;
        transition: opacity 0.2s ease;
        
        .el-icon {
          color: var(--el-color-danger);
          cursor: pointer;
          font-size: 16px;
        }
      }
      
      &:hover .actions {
        opacity: 1;
      }
    }
  }
}
</style>
