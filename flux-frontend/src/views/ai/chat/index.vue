<template>
  <div class="app-container chat-container">
    <el-row :gutter="20">
      <!-- 侧边栏 -->
      <el-col :xs="24" :sm="8" :md="6" :lg="5" :xl="4" class="chat-sidebar-col">
        <ChatSidebar @onclose="toggleSidebar" />
      </el-col>
      
      <!-- 主聊天区域 -->
      <el-col :xs="24" :sm="16" :md="18" :lg="19" :xl="20" class="chat-main-col">
        <div class="chat-main">
          <!-- 移动端侧边栏切换按钮 -->
          <div class="chat-mobile-header">
            <el-button type="text" @click="toggleSidebar">
              <el-icon><Menu /></el-icon>
            </el-button>
            <h2>AI 聊天</h2>
          </div>
          
          <!-- 聊天消息区域 -->
          <ChatMessages />
          
          <!-- 聊天输入区域 -->
          <ChatTextarea />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Menu } from '@element-plus/icons-vue'
import ChatSidebar from '@/components/Chat/ChatSidebar.vue'
import ChatMessages from '@/components/Chat/ChatMessages.vue'
import ChatTextarea from '@/components/Chat/ChatTextarea.vue'
import useDifyChatStore from '@/store/modules/dify-chat'

const route = useRoute();
const difyChatStore = useDifyChatStore();

// 移动端侧边栏显示状态
const showSidebar = ref(false);

// 切换侧边栏显示
const toggleSidebar = () => {
  showSidebar.value = !showSidebar.value;
};

// 初始化应用
onMounted(async () => {
  // 从路由获取appid
  const appid = route.params.appid || route.query.appid;
  
  if (appid) {
    difyChatStore.setAppId(appid);
    await difyChatStore.initDifyApp();
  }
});

// 监听路由变化，更新appid
watch(
  () => route.params.appid || route.query.appid,
  async (newAppId) => {
    if (newAppId && newAppId !== difyChatStore.appid) {
      difyChatStore.setAppId(newAppId);
      await difyChatStore.initDifyApp();
    }
  }
);
</script>

<style scoped>
.chat-container {
  height: calc(100vh - 120px);
  overflow: hidden;
}

.chat-sidebar-col {
  height: 100%;
}

.chat-main-col {
  height: 100%;
}

.chat-main {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: var(--el-bg-color);
  border-radius: 4px;
  box-shadow: var(--el-box-shadow-light);
}

.chat-mobile-header {
  display: none;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--el-border-color);
}

.chat-mobile-header h2 {
  margin: 0;
  font-size: 1.25rem;
}

@media (max-width: 768px) {
  .chat-sidebar-col {
    position: fixed;
    top: 0;
    left: 0;
    width: 80%;
    height: 100vh;
    z-index: 2000;
    background-color: var(--el-bg-color);
    transform: translateX(-100%);
    transition: transform 0.3s;
    box-shadow: var(--el-box-shadow);
  }
  
  .chat-sidebar-col.show {
    transform: translateX(0);
  }
  
  .chat-mobile-header {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
}
</style>
