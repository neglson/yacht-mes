import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '仪表盘', icon: 'Odometer' }
      },
      {
        path: 'projects',
        name: 'Projects',
        component: () => import('@/views/projects/index.vue'),
        meta: { title: '项目管理', icon: 'Ship' }
      },
      {
        path: 'projects/:id',
        name: 'ProjectDetail',
        component: () => import('@/views/projects/detail.vue'),
        meta: { title: '项目详情', hidden: true }
      },
      {
        path: 'tasks',
        name: 'Tasks',
        component: () => import('@/views/tasks/index.vue'),
        meta: { title: '任务管理', icon: 'List' }
      },
      {
        path: 'tasks/gantt',
        name: 'TaskGantt',
        component: () => import('@/views/tasks/gantt.vue'),
        meta: { title: '甘特图', icon: 'Calendar' }
      },
      {
        path: 'materials',
        name: 'Materials',
        component: () => import('@/views/materials/index.vue'),
        meta: { title: '物料管理', icon: 'Box' }
      },
      {
        path: 'procurement',
        name: 'Procurement',
        component: () => import('@/views/procurement/index.vue'),
        meta: { title: '采购管理', icon: 'ShoppingCart' }
      },
      {
        path: 'inventory',
        name: 'Inventory',
        component: () => import('@/views/inventory/index.vue'),
        meta: { title: '库存管理', icon: 'Warehouse' }
      },
      {
        path: 'quality',
        name: 'Quality',
        component: () => import('@/views/quality/index.vue'),
        meta: { title: '质量管理', icon: 'CircleCheck' }
      },
      {
        path: 'knowledge',
        name: 'Knowledge',
        component: () => import('@/views/knowledge/index.vue'),
        meta: { title: '知识库', icon: 'Reading' }
      },
      {
        path: 'ai',
        name: 'AIAssistant',
        component: () => import('@/views/ai/index.vue'),
        meta: { title: 'AI 助手', icon: 'Cpu' }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/users/index.vue'),
        meta: { title: '用户管理', icon: 'User', admin: true }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/settings/index.vue'),
        meta: { title: '系统设置', icon: 'Setting' }
      },
      {
        path: 'import',
        name: 'DataImport',
        component: () => import('@/views/import/index.vue'),
        meta: { title: '数据导入', icon: 'Upload', admin: true }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  NProgress.start()
  
  const userStore = useUserStore()
  
  // 公开页面直接放行
  if (to.meta.public) {
    next()
    return
  }
  
  // 检查登录状态
  if (!userStore.token) {
    next('/login')
    return
  }
  
  // 检查管理员权限
  if (to.meta.admin && userStore.userInfo?.role !== 'admin') {
    next('/')
    return
  }
  
  next()
})

router.afterEach(() => {
  NProgress.done()
})

export default router
