<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>AI 示例</span>
            </div>
          </template>
          <div class="card-content">
            <div class="text-center mb-20">
              <h2>FluxPanel AI 示例</h2>
              <p class="text-muted">一些简单的接入AI接口的示例</p>
            </div>
            <ai-cards />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup name="AiDemo">
import AiCards from '@/components/ai/AiCards.vue';
</script>

<style scoped>
.text-center {
  text-align: center;
}
.mb-20 {
  margin-bottom: 20px;
}
.text-muted {
  color: #909399;
}
</style>
