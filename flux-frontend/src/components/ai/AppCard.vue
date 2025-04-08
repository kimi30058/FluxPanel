<template>
  <el-card
    class="app-card"
    :body-style="{ padding: '0px' }"
    shadow="hover"
    :class="{ 'is-disabled': !isActive }"
    @click="handleCardClick"
  >
    <div class="app-card-header">
      <div class="app-icon" :style="{ backgroundColor: app.icon_bg_color || '#e6f4ff' }">
        <div class="app-icon-fallback">
          <el-icon>
            <component :is="appType === 'coze' ? 'ChatDotRound' : 'Connection'" />
          </el-icon>
        </div>
      </div>
      <div class="app-info">
        <h3 class="app-name">{{ appName }}</h3>
        <div class="app-meta">
          <el-tag size="small" effect="plain">{{ appType }}</el-tag>
          <span v-if="createdDate" class="app-date">{{ createdDate }}</span>
        </div>
      </div>
    </div>
    <div class="app-card-body">
      <p class="app-description">{{ appDescription }}</p>
    </div>
    <div class="app-card-footer">
      <div class="app-tags" v-if="appTags.length > 0">
        <el-tag
          v-for="tag in appTags.slice(0, 3)"
          :key="tag"
          size="small"
          :type="getTagType(tag)"
          effect="light"
          class="tag-item"
        >
          {{ tag }}
        </el-tag>
        <el-tag v-if="appTags.length > 3" size="small" type="info" effect="plain">
          +{{ appTags.length - 3 }}
        </el-tag>
      </div>
      <div class="app-actions">
        <el-button
          type="primary"
          size="small"
          :disabled="!isActive"
          :loading="loading"
          class="use-app-btn"
          @click.stop="handleCardClick"
        >
          {{ isActive ? '使用' : '已禁用' }}
        </el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { AIApp } from '@/api/ai'
import { ChatDotRound, Connection } from '@element-plus/icons-vue'

defineOptions({
  name: 'AIAppCard'
})

const props = defineProps<{
  app: AIApp
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'click'): void
  (e: 'favorite', value: boolean): void
}>()

const tagColors = {
  聊天: 'success',
  文档: 'warning',
  图像: 'danger',
  办公: 'info',
  教育: 'primary'
}

const getTagType = computed(() => {
  return (tag: string) => {
    // @ts-ignore
    return tagColors[tag] || 'info'
  }
})

// 获取应用名称
const appName = computed(() => {
  return props.app.app_name || props.app.typeName || '未命名应用'
})

// 获取应用类型
const appType = computed(() => {
  return props.app.app_type || props.app.type || 'unknown'
})

// 获取应用是否可用
const isActive = computed(() => {
  return props.app.is_active !== undefined ? props.app.is_active : true
})

// 获取应用描述
const appDescription = computed(() => {
  return props.app.description || props.app.system_prompt || '暂无描述'
})

// 获取应用标签
const appTags = computed(() => {
  return Array.isArray(props.app.tags) ? props.app.tags : []
})

// 获取应用创建日期
const createdDate = computed(() => {
  if (!props.app.created_at) return ''
  return typeof props.app.created_at === 'string' && props.app.created_at.includes(' ') 
    ? props.app.created_at.split(' ')[0] 
    : props.app.created_at
})

const handleCardClick = () => {
  emit('click')
}
</script>

<style lang="scss" scoped>
.app-card {
  transition: all 0.3s;
  height: 100%;
  display: flex;
  flex-direction: column;
  cursor: pointer;

  &:hover {
    transform: translateY(-5px);
  }

  &.is-disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .app-card-header {
    padding: 15px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid var(--el-border-color-lighter);

    .app-icon {
      width: 50px;
      height: 50px;
      margin-right: 12px;
      border-radius: 10px;
      overflow: hidden;
      flex-shrink: 0;

      .el-image {
        width: 100%;
        height: 100%;
      }

      .app-icon-fallback {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--el-color-primary);
        font-size: 24px;
      }
    }

    .app-info {
      flex: 1;
      min-width: 0;

      .app-name {
        margin: 0 0 5px;
        font-size: 16px;
        font-weight: 600;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .app-meta {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 12px;
        color: var(--el-text-color-secondary);

        .app-date {
          font-size: 12px;
        }
      }
    }
  }

  .app-card-body {
    padding: 15px;
    flex: 1;

    .app-description {
      margin: 0;
      font-size: 14px;
      color: var(--el-text-color-regular);
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }

  .app-card-footer {
    padding: 10px 15px 15px;
    border-top: 1px solid var(--el-border-color-lighter);

    .app-tags {
      margin-bottom: 12px;
      display: flex;
      flex-wrap: wrap;
      gap: 5px;

      .tag-item {
        margin-right: 5px;
      }
    }

    .app-actions {
      display: flex;
      justify-content: flex-end;

      .use-app-btn {
        min-width: 80px;
      }
    }
  }
}
</style>
