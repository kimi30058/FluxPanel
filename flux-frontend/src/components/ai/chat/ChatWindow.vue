<template>
  <div class="chat-window">
    <div ref="messageContainer" class="message-container" @scroll="handleMessagesScroll">
      <!-- 加载更多提示 -->
      <div v-if="hasMoreMessages && isLoadingMore" class="loading-more">
        <el-icon class="loading">
          <Loading />
        </el-icon>
        加载中...
      </div>

      <!-- 消息列表 -->
      <div v-if="messages.length === 0" class="empty-message">
        开始新的对话
      </div>

      <div v-else class="message-list">
        <div v-for="message in messages" :key="message.id" :id="`message-${message.id}`"
          :class="['message-item', message.role === 'assistant' ? 'message-ai' : 'message-user']">
          <!-- AI消息 -->
          <template v-if="message.role === 'assistant'">
            <div class="avatar">
              <el-icon>
                <Robot />
              </el-icon>
            </div>
            <div class="message-content">
              <div class="message-bubble">
                <div class="message-text" v-if="!message.content_type || message.content_type === 'text'">
                  <MessageMarkdown :content="message.content" />
                </div>
                <div v-else-if="message.content_type === 'image'" class="message-image">
                  <el-image :src="message.content" :preview-src-list="[message.content]" fit="contain"
                    style="max-width: 100%; max-height: 400px;" />
                </div>

                <!-- 操作按钮 -->
                <div class="message-actions">
                  <el-button link :class="{ 'is-active': message.copySuccess }" @click="handleCopyMessage(message)">
                    <el-icon>
                      <Document v-if="!message.copySuccess" />
                      <Select v-else />
                    </el-icon>
                  </el-button>

                  <el-button link :class="{ 'is-active': message.feedback?.rating === 'like' }"
                    @click="handleLikeMessage(message)">
                    <el-icon>
                      <ThumbsUp />
                    </el-icon>
                  </el-button>

                  <el-button link :class="{ 'is-active': message.feedback?.rating === 'dislike' }"
                    @click="handleDislikeMessage(message)">
                    <el-icon>
                      <ThumbsDown />
                    </el-icon>
                  </el-button>
                </div>
              </div>
            </div>
          </template>

          <!-- 用户消息 -->
          <template v-else>
            <div class="message-content">
              <div class="message-bubble">
                <div v-if="!message.content_type || message.content_type === 'text'" class="message-text">
                  <MessageMarkdown :content="message.content" />
                </div>
                <div v-else-if="message.content_type === 'image'" class="message-image">
                  <el-image :src="message.content" :preview-src-list="[message.content]" fit="contain"
                    style="max-width: 100%; max-height: 400px;" />
                </div>
                <div v-else-if="message.content_type === 'file'" class="message-file">
                  <div class="file-info">
                    <el-icon>
                      <Document />
                    </el-icon>
                    <span>{{ message.file_name || '文件' }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="avatar">
              <el-icon>
                <User />
              </el-icon>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- 输入框组件 -->
    <MessageInput :loading="isLoadingMessage" @send="handleSendMessage" @send-image="handleSendImage"
      @send-file="handleSendFile" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useChatStore } from '@/store/modules/chat'
import { storeToRefs } from 'pinia'
import { ElMessage } from 'element-plus'
import MessageInput from './MessageInput.vue'
import MessageMarkdown from '@/components/common/markdown/MessageMarkdown.vue'
import { debounce } from 'lodash-es'
import { Document, Loading, Robot, Select, ThumbsDown, ThumbsUp, User } from '@element-plus/icons-vue'

interface MessageWithUI extends Record<string, any> {
  copySuccess?: boolean
  feedback?: {
    rating: 'like' | 'dislike' | null
  }
  content_type?: 'text' | 'image' | 'file'
  file_name?: string
}

const props = defineProps({
  messages: {
    type: Array,
    default: () => []
  },
  provider: {
    type: String,
    default: 'dify'
  }
})

const store = useChatStore()
const { messages: storeMessages, isLoadingMessage, hasMoreMessages } = storeToRefs(store)
const messages = ref<MessageWithUI[]>([])

// 监听store中的消息变化，转换成MessageWithUI类型
watch(storeMessages, (newMessages) => {
  messages.value = newMessages as MessageWithUI[]
}, { immediate: true })

const messageContainer = ref<HTMLElement | null>(null)
const scrollInterval = ref<ReturnType<typeof setInterval> | null>(null)
const isLoadingMore = ref(false)
const lastScrollTop = ref(0)

// 滚动到底部
const scrollToBottom = () => {
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
}

// 处理加载更多消息
const handleLoadMore = debounce(async () => {
  if (hasMoreMessages.value && !isLoadingMessage.value && !isLoadingMore.value) {
    isLoadingMore.value = true

    const firstMessage = messages.value?.[0]
    const messageElement = document.getElementById(`message-${firstMessage?.id}`)

    await store.fetchMoreMessages()

    nextTick(() => {
      if (messageElement) {
        messageElement.scrollIntoView()
      }
      isLoadingMore.value = false
    })
  }
}, 200)

// 处理消息列表滚动
const handleMessagesScroll = (e: Event) => {
  const target = e.target as HTMLElement
  const { scrollTop } = target

  const isScrollingUp = scrollTop < lastScrollTop.value
  lastScrollTop.value = scrollTop

  if (isScrollingUp && scrollTop < 50) {
    handleLoadMore()
  }
}

// 复制消息内容
const handleCopyMessage = async (message: MessageWithUI) => {
  if (message.content) {
    try {
      await navigator.clipboard.writeText(message.content.trim())
      message.copySuccess = true
      setTimeout(() => {
        message.copySuccess = false
      }, 1500)
      ElMessage.success('复制成功')
    } catch (err) {
      ElMessage.error('复制失败')
    }
  }
}

// 处理点赞
const handleLikeMessage = async (message: MessageWithUI) => {
  if (!message.id) return

  const newRating = message.feedback?.rating === 'like' ? null : 'like'
  await store.sendMessageFeedback(message.id, newRating)

  if (newRating === null) {
    message.feedback = undefined
  } else {
    message.feedback = { rating: newRating }
  }
}

// 处理点踩
const handleDislikeMessage = async (message: MessageWithUI) => {
  if (!message.id) return

  const newRating = message.feedback?.rating === 'dislike' ? null : 'dislike'
  await store.sendMessageFeedback(message.id, newRating)

  if (newRating === null) {
    message.feedback = undefined
  } else {
    message.feedback = { rating: newRating }
  }
}

// 发送文本消息
const handleSendMessage = async (content: string) => {
  await store.sendMessage({
    content,
    content_type: 'text'
  })
}

// 发送图片消息
const handleSendImage = async (imageUrl: string) => {
  await store.sendMessage({
    content: imageUrl,
    content_type: 'image'
  })
}

// 发送文件消息
const handleSendFile = async (fileInfo: { url: string, name: string }) => {
  await store.sendMessage({
    content: fileInfo.url,
    content_type: 'file',
    file_name: fileInfo.name
  })
}

// 监听加载状态变化
watch(isLoadingMessage, (newValue) => {
  if (newValue) {
    if (scrollInterval.value) clearInterval(scrollInterval.value)
    scrollInterval.value = setInterval(scrollToBottom, 1000)
  } else {
    if (scrollInterval.value) {
      clearInterval(scrollInterval.value)
      scrollInterval.value = null
    }
    nextTick(scrollToBottom)
  }
})

onMounted(() => {
  scrollToBottom()
})

onUnmounted(() => {
  if (scrollInterval.value) {
    clearInterval(scrollInterval.value)
    scrollInterval.value = null
  }
})
</script>

<style lang="scss" scoped>
.chat-window {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: var(--el-bg-color);

  .message-container {
    flex: 1;
    overflow-y: auto;
    padding: 20px;

    .loading-more {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      color: var(--el-text-color-secondary);
      font-size: 14px;
      padding: 10px 0;

      .loading {
        animation: rotating 2s linear infinite;
      }
    }

    .empty-message {
      text-align: center;
      color: var(--el-text-color-secondary);
      padding: 40px 0;
    }

    .message-list {
      max-width: 900px;
      margin: 0 auto;

      .message-item {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;

        .avatar {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background-color: var(--el-color-primary-light-9);
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;

          .el-icon {
            font-size: 20px;
            color: var(--el-color-primary);
          }
        }

        .message-content {
          flex: 1;
          max-width: 80%;

          .message-bubble {
            position: relative;
            padding: 12px 16px;
            border-radius: 8px;
            background-color: var(--el-bg-color-page);

            .message-text {
              font-size: 14px;
              line-height: 1.5;
              white-space: pre-wrap;
              word-break: break-word;
            }

            .message-image {
              margin: 8px 0;
            }

            .message-file {
              .file-info {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 8px;
                border-radius: 4px;
                background-color: var(--el-fill-color-light);

                .el-icon {
                  font-size: 18px;
                  color: var(--el-color-primary);
                }
              }
            }

            .message-actions {
              display: none;
              position: absolute;
              right: 0;
              bottom: 0;
              transform: translateY(100%);
              background-color: var(--el-bg-color);
              border-radius: 4px;
              box-shadow: var(--el-box-shadow-light);

              .el-button {
                padding: 8px;

                &.is-active {
                  color: var(--el-color-primary);
                }
              }
            }

            &:hover .message-actions {
              display: flex;
            }
          }
        }

        &.message-ai {
          .message-bubble {
            background-color: var(--el-bg-color-page);
          }
        }

        &.message-user {
          flex-direction: row-reverse;

          .message-bubble {
            background-color: var(--el-color-primary-light-9);
          }

          .avatar {
            background-color: var(--el-color-primary);

            .el-icon {
              color: #fff;
            }
          }
        }
      }
    }
  }
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}
</style>
