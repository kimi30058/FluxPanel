<template>
  <div class="markdown-content" v-html="renderedContent"></div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

const props = defineProps({
  content: {
    type: String,
    default: ''
  }
})

// 配置marked
marked.setOptions({
  highlight: function(code, lang) {
    const language = hljs.getLanguage(lang) ? lang : 'plaintext';
    return hljs.highlight(code, { language }).value;
  },
  langPrefix: 'hljs language-',
  gfm: true,
  breaks: true
})

// 渲染Markdown内容
const renderedContent = computed(() => {
  if (!props.content) return ''
  
  try {
    return marked(props.content)
  } catch (error) {
    console.error('Markdown渲染失败:', error)
    return props.content
  }
})

onMounted(() => {
  // 确保代码高亮应用到动态内容
  document.querySelectorAll('pre code').forEach((block) => {
    hljs.highlightElement(block as HTMLElement)
  })
})
</script>

<style lang="scss" scoped>
.markdown-content {
  :deep(pre) {
    background-color: #f6f8fa;
    border-radius: 6px;
    padding: 16px;
    overflow: auto;
    
    code {
      font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
      font-size: 14px;
      line-height: 1.5;
    }
  }
  
  :deep(code) {
    background-color: rgba(175, 184, 193, 0.2);
    border-radius: 6px;
    padding: 0.2em 0.4em;
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  }
  
  :deep(p) {
    margin: 0.5em 0;
  }
  
  :deep(ul), :deep(ol) {
    padding-left: 2em;
  }
  
  :deep(blockquote) {
    border-left: 4px solid #dfe2e5;
    padding-left: 1em;
    color: #6a737d;
    margin: 0.5em 0;
  }
  
  :deep(table) {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    
    th, td {
      border: 1px solid #dfe2e5;
      padding: 6px 13px;
    }
    
    th {
      background-color: #f6f8fa;
    }
  }
  
  :deep(img) {
    max-width: 100%;
  }
  
  :deep(a) {
    color: var(--el-color-primary);
    text-decoration: none;
    
    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
