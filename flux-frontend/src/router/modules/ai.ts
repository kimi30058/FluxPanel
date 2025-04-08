import Layout from '@/layout'

const aiRouter = {
  path: '/ai',
  component: Layout,
  redirect: '/ai/applications',
  name: 'AI',
  meta: {
    title: 'AI应用',
    icon: 'robot',
    roles: ['admin', 'common']
  },
  children: [
    {
      path: 'applications',
      component: () => import('@/views/ai/applications/index'),
      name: 'AIApplications',
      meta: { title: 'AI应用管理', icon: 'app', roles: ['admin'] }
    },
    {
      path: 'chat',
      component: () => import('@/views/ai/chat/index'),
      name: 'AIChat',
      meta: { title: 'AI聊天', icon: 'chat', roles: ['admin', 'common'] }
    },
    {
      path: 'providers',
      component: () => import('@/views/ai/providers/index'),
      name: 'AIProviders',
      meta: { title: '模型提供商', icon: 'cloud', roles: ['admin'] }
    }
  ]
}

export default aiRouter
