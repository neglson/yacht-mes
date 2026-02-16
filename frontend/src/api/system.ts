import api from './index'

// 项目 API
export const getProjects = (params?: any) => api.get('/projects', { params })
export const createProject = (data: any) => api.post('/projects', data)
export const updateProject = (id: number, data: any) => api.put(`/projects/${id}`, data)
export const deleteProject = (id: number) => api.delete(`/projects/${id}`)

// 任务 API
export const getTasks = (params?: any) => api.get('/tasks', { params })
export const createTask = (data: any) => api.post('/tasks', data)
export const updateTask = (id: number, data: any) => api.put(`/tasks/${id}`, data)
export const deleteTask = (id: number) => api.delete(`/tasks/${id}`)
export const reportWork = (id: number, data: any) => api.post(`/tasks/${id}/report`, data)

// 物料 API
export const getMaterials = (params?: any) => api.get('/materials', { params })
export const createMaterial = (data: any) => api.post('/materials', data)
export const updateMaterial = (id: number, data: any) => api.put(`/materials/${id}`, data)
export const deleteMaterial = (id: number) => api.delete(`/materials/${id}`)

// 库存 API
export const getInventory = (params?: any) => api.get('/inventory', { params })
export const inventoryTransaction = (data: any) => api.post('/inventory/transaction', data)
export const getInventoryLogs = (params?: any) => api.get('/inventory/logs', { params })
export const getInventoryAlerts = () => api.get('/inventory/alerts')

// 采购 API
export const getProcurement = (params?: any) => api.get('/procurement', { params })
export const createProcurement = (data: any) => api.post('/procurement', data)
export const approveProcurement = (id: number) => api.put(`/procurement/${id}/approve`)
export const updateProcurementStatus = (id: number, data: any) => api.put(`/procurement/${id}/status`, data)

// 用户 API
export const getUsers = (params?: any) => api.get('/users', { params })
export const createUser = (data: any) => api.post('/users', data)
export const updateUser = (id: number, data: any) => api.put(`/users/${id}`, data)
export const deleteUser = (id: number) => api.delete(`/users/${id}`)
export const resetPassword = (id: number) => api.post(`/users/${id}/reset-password`)

// 仪表盘 API
export const getDashboardStats = () => api.get('/dashboard/stats')
export const getProjectProgress = () => api.get('/dashboard/project-progress')
export const getTaskDistribution = () => api.get('/dashboard/task-distribution')
export const getRecentActivities = () => api.get('/dashboard/recent-activities')

// AI API
export const aiQuery = (query: string) => api.post('/ai/query', { query })
export const getProcurementAdvice = (projectId: number) => api.post('/ai/procurement-advice', { project_id: projectId })
export const generateDailyReport = (date?: string) => api.post('/ai/daily-report', { date })
export const queryKnowledge = (question: string) => api.post('/ai/knowledge-query', { question })

// 导入 API
export const importExcel = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/import/excel', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}
