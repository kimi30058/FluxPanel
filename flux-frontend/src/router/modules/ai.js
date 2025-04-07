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
    }
  ]
}
