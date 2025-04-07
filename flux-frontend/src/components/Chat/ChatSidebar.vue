<template>
  <div class="chat-sidebar">
    <div class="chat-sidebar-header">
      <el-button type="primary" @click="newConversation">
        <el-icon><Plus /></el-icon> 新对话
      </el-button>
    </div>
    
    <div class="chat-sidebar-content">
      <div v-if="isLoadingHistory" class="chat-sidebar-loading">
        <el-icon class="is-loading"><Loading /></el-icon> 加载中...
      </div>
      
      <div v-else-if="conversationHistory.length === 0" class="chat-sidebar-empty">
        没有历史对话
      </div>
      
      <div v-else class="chat-sidebar-list">
        <div
          v-for="conversation in conversationHistory"
          :key="conversation.id"
          class="chat-sidebar-item"
          :class="{ 'chat-sidebar-item-active': conversation.id === currentConversationId }"
          @click="selectConversation(conversation)"
        >
          <div class="chat-sidebar-item-title">
            {{ conversation.title || '新对话' }}
          </div>
          
          <div class="chat-sidebar-item-actions">
            <el-dropdown trigger="click" @command="(command) => handleAction(command, conversation)">
              <el-button type="text" size="small">
                <el-icon><MoreFilled /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="rename">重命名</el-dropdown-item>
                  <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
        
        <div v-if="hasMoreHistory" class="chat-sidebar-load-more">
          <el-button type="text" @click="loadMoreConversations">
            加载更多
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter, useRoute } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import { Loading, Plus, MoreFilled } from '@element-plus/icons-vue'
import useDifyChatStore from '@/store/modules/dify-chat'

const difyChatStore = useDifyChatStore();
const { conversationHistory, currentConversationId, isLoadingHistory, hasMoreHistory } = storeToRefs(difyChatStore);

const router = useRouter();
const route = useRoute();

const emit = defineEmits(["onclose"]);
const renameInput = ref("");

// 选择会话
const selectConversation = (conversation) => {
  if (conversation.id === currentConversationId.value) return;
  
  router.push({
    query: { ...route.query, conversation_id: conversation.id },
  });
  
  // 关闭移动端侧边栏
  emit("onclose");
};

// 新建会话
const newConversation = () => {
  difyChatStore.startNewConversation();
  router.push({
    query: { ...route.query, conversation_id: undefined },
  });
  
  // 关闭移动端侧边栏
  emit("onclose");
};

// 加载更多会话
const loadMoreConversations = () => {
  if (!isLoadingHistory.value) {
    difyChatStore.loadConversations(true);
  }
};

// 处理会话操作
const handleAction = (action, conversation) => {
  if (action === 'delete') {
    deleteConversation(conversation);
  } else if (action === 'rename') {
    renameConversation(conversation);
  }
};

// 删除会话
const deleteConversation = (conversation) => {
  ElMessageBox.confirm(
    '确定要删除此会话吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    const success = await difyChatStore.deleteConversation(conversation.id);
    if (success) {
      ElMessage.success('删除成功');
    }
  }).catch(() => {});
};

// 重命名会话
const renameConversation = (conversation) => {
  renameInput.value = conversation.title || '';
  
  ElMessageBox.prompt(
    '请输入新的会话名称',
    '重命名会话',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputValue: renameInput.value,
    }
  ).then(async ({ value }) => {
    if (value.trim()) {
      const success = await difyChatStore.renameConversation(conversation.id, value.trim());
      if (success) {
        ElMessage.success('重命名成功');
      }
    }
  }).catch(() => {});
};
</script>

<style scoped>
.chat-sidebar {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  border-right: 1px solid var(--el-border-color);
}

.chat-sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid var(--el-border-color);
}

.chat-sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.chat-sidebar-loading,
.chat-sidebar-empty {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.chat-sidebar-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.chat-sidebar-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.chat-sidebar-item:hover {
  background-color: var(--el-fill-color-light);
}

.chat-sidebar-item-active {
  background-color: var(--el-color-primary-light-9);
}

.chat-sidebar-item-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 14px;
}

.chat-sidebar-item-actions {
  opacity: 0;
  transition: opacity 0.2s;
}

.chat-sidebar-item:hover .chat-sidebar-item-actions {
  opacity: 1;
}

.chat-sidebar-load-more {
  display: flex;
  justify-content: center;
  padding: 0.5rem 0;
}
</style>
