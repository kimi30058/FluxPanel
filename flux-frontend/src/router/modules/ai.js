import Layout from '@/layout'

export default {
  path: '/ai',
  component: Layout,
  name: 'Ai',
  meta: {
    title: 'AI 示例',
    icon: 'chat-dot-round'
  },
  children: [
    {
      path: 'index',
      component: () => import('@/views/ai/index'),
      name: 'AiDemo',
      meta: { title: 'AI 示例', icon: 'chat-dot-round' }
    },
    {
      path: 'chat/:appid',
      component: () => import('@/views/ai/chat/index'),
      name: 'AiChat',
      meta: { title: 'AI 对话', activeMenu: '/ai/index' },
      hidden: true
    },
    {
      path: 'completion/:appid',
      component: () => import('@/views/ai/completion/index'),
      name: 'AiCompletion',
      meta: { title: 'AI 生成', activeMenu: '/ai/index' },
      hidden: true
    },
    {
      path: 'workflow/:appid',
      component: () => import('@/views/ai/workflow/index'),
      name: 'AiWorkflow',
      meta: { title: 'AI 工作流', activeMenu: '/ai/index' },
      hidden: true
    }
  ]
}
