<template>
  <div class="message-input-container">
    <div class="input-wrapper">
      <div class="input-container">
        <el-input
          v-model="message"
          type="textarea"
          :rows="3"
          :placeholder="loading ? '正在响应中...' : '请输入消息，按 Ctrl + Enter 发送'"
          :disabled="loading"
          resize="none"
          @keydown.ctrl.enter.prevent="handleSend"
        />
        <el-button
          class="send-button"
          type="primary"
          :loading="loading"
          @click="handleSend"
        >
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['send', 'send-image', 'send-file'])

const message = ref('')

const handleSend = () => {
  if (!message.value.trim() || props.loading) return
  
  emit('send', message.value)
  message.value = ''
}
</script>

<style lang="scss" scoped>
.message-input-container {
  border-top: 1px solid #e6e6e6;
  padding: 16px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  
  .input-wrapper {
    max-width: 900px;
    width: 100%;
    
    .input-container {
      position: relative;
      
      :deep(.el-textarea__inner) {
        resize: none;
        font-size: 14px;
        padding-right: 90px;
        
        &:disabled {
          background-color: #f5f7fa;
          cursor: not-allowed;
        }
      }

      .send-button {
        position: absolute;
        right: 8px;
        bottom: 8px;
      }
    }
  }
}
</style>
