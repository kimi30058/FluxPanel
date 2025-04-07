<template>
  <div class="chat-textarea-container">
    <div class="chat-textarea-wrapper">
      <el-input
        ref="textareaRef"
        v-model="message"
        type="textarea"
        :rows="1"
        :disabled="isLoadingMessage"
        placeholder="输入消息..."
        resize="none"
        @keydown="handleKeyDown"
        @input="autoGrow"
      >
      </el-input>
      
      <div class="chat-textarea-actions">
        <el-button
          type="primary"
          :disabled="!message.trim() || isLoadingMessage"
          @click="handleSubmit"
        >
          <el-icon v-if="isLoadingMessage" class="is-loading"><Loading /></el-icon>
          <el-icon v-else><Position /></el-icon>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { Loading, Position } from '@element-plus/icons-vue'
import useDifyChatStore from '@/store/modules/dify-chat'

const difyChatStore = useDifyChatStore();
const { isLoadingMessage } = storeToRefs(difyChatStore);

const message = ref("");
const textareaRef = ref(null);

const handleSubmit = () => {
  if (!message.value.trim() || isLoadingMessage.value) return;
  
  difyChatStore.sendMessage(message.value);
  message.value = "";
  
  // 重置文本框高度
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.style.height = "auto";
    }
  });
};

// 处理按键事件
const handleKeyDown = (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleSubmit();
  }
};

// 文本框自动增高
const autoGrow = (e) => {
  const textarea = e.target;
  textarea.style.height = "auto";
  textarea.style.height = `${textarea.scrollHeight}px`;
};
</script>

<style scoped>
.chat-textarea-container {
  padding: 1rem;
  border-top: 1px solid var(--el-border-color);
}

.chat-textarea-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
  max-width: 780px;
  margin: 0 auto;
}

.chat-textarea-actions {
  display: flex;
  align-items: center;
}

:deep(.el-textarea__inner) {
  max-height: 150px;
  padding-right: 2.5rem;
}
</style>
