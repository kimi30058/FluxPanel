<template>
  <div
    ref="messageContainer"
    class="chat-messages-container"
    @scroll="handleMessagesScroll"
  >
    <div class="chat-messages-content">
      <div
        v-if="isMessagesLoading"
        class="chat-loading"
      >
        <el-icon class="is-loading"><Loading /></el-icon>
        <p class="chat-loading-text">加载对话内容...</p>
      </div>

      <!-- 加载更多提示 -->
      <div
        v-if="hasMoreMessages && isLoadingMore"
        class="chat-loading-more"
      >
        <el-icon class="is-loading"><Loading /></el-icon> 加载中...
      </div>

      <!-- 消息列表 -->
      <div v-if="!isMessagesLoading">
        <div
          v-if="messages.length === 0"
          class="chat-new-conversation"
        >
          新的对话
        </div>

        <div
          v-for="message in messages"
          :key="message.id"
          :id="`message-${message.id}`"
          :class="[
            'chat-message',
            message.isBot ? 'chat-message-bot' : 'chat-message-user',
          ]"
        >
          <!-- AI消息 -->
          <template v-if="message.isBot">
            <div class="chat-avatar chat-avatar-bot">
              <el-icon><Service /></el-icon>
            </div>
            <div class="chat-message-content">
              <div
                class="chat-message-bubble"
                :class="{ 'chat-message-error': message.error }"
              >
                <div v-html="message.content"></div>
                <!-- 文件预览（如有需要可添加） -->
              </div>
            </div>
          </template>

          <!-- 用户消息 -->
          <template v-else>
            <div class="chat-message-content">
              <div class="chat-message-bubble chat-message-bubble-user">
                <div v-html="message.content"></div>
                <!-- 文件预览（如有需要可添加） -->
              </div>
            </div>
            <div class="chat-avatar chat-avatar-user">
              <el-icon><User /></el-icon>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useRoute } from 'vue-router'
import { Loading, Service, User } from '@element-plus/icons-vue'
import useDifyChatStore from '@/store/modules/dify-chat'
import lodash from 'lodash'

const difyChatStore = useDifyChatStore();

const {
  messages,
  isLoadingMessage,
  isMessagesLoading,
  hasMoreMessages,
  currentConversationId,
} = storeToRefs(difyChatStore);

// 消息容器的引用
const messageContainer = ref(null);
const scrollInterval = ref(null);
const isLoadingMore = ref(false);

// 记录上一次的滚动位置
const lastScrollTop = ref(0);

// 滚动到底部
const scrollToBottom = () => {
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
  }
};

// 处理加载更多消息
const handleLoadMore = lodash.debounce(async () => {
  if (
    hasMoreMessages.value &&
    !isLoadingMessage.value &&
    !isLoadingMore.value
  ) {
    isLoadingMore.value = true;

    // 获取当前第一条消息的DOM元素
    const firstMessage = messages.value?.[0];
    const messageElement = document.getElementById(
      `message-${firstMessage?.id}`
    );

    await difyChatStore.fetchMessages(true);

    nextTick(() => {
      // 滚动到之前的消息位置
      if (messageElement) {
        messageElement.scrollIntoView();
      }
      isLoadingMore.value = false;
    });
  }
}, 200);

// 处理消息列表滚动
const handleMessagesScroll = (e) => {
  const target = e.target;
  const { scrollTop } = target;

  // 判断是否是向上滚动
  const isScrollingUp = scrollTop < lastScrollTop.value;
  lastScrollTop.value = scrollTop;

  // 当向上滚动到顶部时加载更多历史消息
  if (isScrollingUp && scrollTop < 50) {
    handleLoadMore();
  }
};

// 设置自动滚动
const setupAutoScroll = () => {
  // 清除已存在的定时器
  if (scrollInterval.value) {
    clearInterval(scrollInterval.value);
    scrollInterval.value = null;
  }

  // 如果正在加载，设置定时滚动
  if (isLoadingMessage.value) {
    scrollInterval.value = setInterval(scrollToBottom, 1000);
  }
};

watch(isLoadingMessage, (newValue) => {
  if (newValue) {
    setupAutoScroll();
  } else {
    // 停止加载时清除定时器
    if (scrollInterval.value) {
      clearInterval(scrollInterval.value);
      scrollInterval.value = null;
    }
    // 最后再滚动一次确保显示最新消息
    nextTick(() => {
      scrollToBottom();
    });
  }
});

watch(isMessagesLoading, (newValue) => {
  if (!newValue) {
    nextTick(() => {
      scrollToBottom();
    });
  }
});

watch(currentConversationId, () => {
  nextTick(() => {
    scrollToBottom();
  });
});

// 组件卸载时清理定时器
onUnmounted(() => {
  if (scrollInterval.value) {
    clearInterval(scrollInterval.value);
    scrollInterval.value = null;
  }
});

// 初始化时滚动到底部
onMounted(() => {
  scrollToBottom();
});
</script>

<style scoped>
.chat-messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.chat-messages-content {
  max-width: 780px;
  margin: 0 auto;
  padding: 1rem;
}

.chat-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 2rem 0;
}

.chat-loading-text {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.chat-loading-more {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem 0;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.chat-new-conversation {
  text-align: center;
  padding: 2rem 0;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.chat-message {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.chat-message-bot {
  justify-content: flex-start;
}

.chat-message-user {
  justify-content: flex-end;
}

.chat-avatar {
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  flex-shrink: 0;
}

.chat-avatar-bot {
  background-color: var(--el-fill-color-darker);
  color: var(--el-text-color-primary);
}

.chat-avatar-user {
  background-color: var(--el-color-primary);
  color: white;
}

.chat-message-content {
  display: flex;
  flex-direction: column;
  max-width: 80%;
  width: 100%;
}

.chat-message-bubble {
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-size: 14px;
  word-break: break-word;
  background-color: var(--el-fill-color);
}

.chat-message-bubble-user {
  background-color: var(--el-color-primary);
  color: white;
}

.chat-message-error {
  background-color: var(--el-color-danger-light-9);
  color: var(--el-color-danger);
}
</style>
