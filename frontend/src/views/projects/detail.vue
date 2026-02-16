<template>
  <div class="project-detail">
    <el-page-header :title="project?.yacht_name" @back="$router.back()">
      <template #content>
        <el-descriptions :column="4" size="small">
          <el-descriptions-item label="项目编号">{{ project?.project_no }}</el-descriptions-item>
          <el-descriptions-item label="船型">{{ project?.yacht_model }}</el-descriptions-item>
          <el-descriptions-item label="船东">{{ project?.client_name }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(project?.status)">
              {{ getStatusText(project?.status) }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </template>
      
      <template #extra>
        <el-button type="primary" @click="handleEdit">编辑</el-button>
      </template>
    </el-page-header>
    
    <!-- 进度概览 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-statistic title="总任务" :value="stats.totalTasks" />
      </el-col>
      <el-col :span="6">
        <el-statistic title="已完成" :value="stats.completedTasks" />
      </el-col>
      <el-col :span="6">
        <el-statistic title="进行中" :value="stats.inProgressTasks" />
      </el-col>
      <el-col :span="6">
        <el-statistic title="延期" :value="stats.delayedTasks" />
      </el-col>
    </el-row>
    
    <!-- 任务列表 -->
    <el-card class="tasks-card">
      <template #header>
        <div class="card-header">
          <span>任务列表</span>
          <el-button type="primary" size="small" @click="handleAddTask">添加任务</el-button>
        </div>
      </template>
      
      <el-table :data="tasks" row-key="id">
        <el-table-column prop="task_no" label="序号" width="80" />
        <el-table-column prop="name" label="任务名称" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getTaskStatusType(row.status)">
              {{ getTaskStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="progress_percent" label="进度" width="150">
          <template #default="{ row }">
            <el-progress :percentage="row.progress_percent || 0" />
          </template>
        </el-table-column>
        
        <el-table-column prop="plan_end" label="计划结束" width="120" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const projectId = route.params.id

const project = ref({
  id: 1,
  project_no: 'YT-2024-001',
  yacht_name: '海鹰号',
  yacht_model: 'HY-65',
  client_name: '张三',
  status: 'in_progress'
})

const stats = ref({
  totalTasks: 10,
  completedTasks: 3,
  inProgressTasks: 5,
  delayedTasks: 2
})

const tasks = ref([
  {
    id: 1,
    task_no: '1.1',
    name: '飞桥结构设计交付',
    status: 'completed',
    progress_percent: 100,
    plan_end: '2024-02-15'
  },
  {
    id: 2,
    task_no: '1.2',
    name: '船体结构生产放样及制作',
    status: 'in_progress',
    progress_percent: 65,
    plan_end: '2024-04-30'
  }
])

const getStatusType = (status?: string) => {
  const map: Record<string, string> = {
    planning: 'info',
    in_progress: 'primary',
    completed: 'success',
    cancelled: 'danger'
  }
  return map[status || ''] || 'info'
}

const getStatusText = (status?: string) => {
  const map: Record<string, string> = {
    planning: '规划中',
    in_progress: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return map[status || ''] || status
}

const getTaskStatusType = (status: string) => {
  const map: Record<string, string> = {
    not_started: 'info',
    in_progress: 'primary',
    completed: 'success',
    delayed: 'danger'
  }
  return map[status] || 'info'
}

const getTaskStatusText = (status: string) => {
  const map: Record<string, string> = {
    not_started: '未开始',
    in_progress: '进行中',
    completed: '已完成',
    delayed: '延期'
  }
  return map[status] || status
}

const handleEdit = () => {
  // TODO: 编辑项目
}

const handleAddTask = () => {
  // TODO: 添加任务
}

onMounted(() => {
  // TODO: 加载项目详情
  console.log('项目ID:', projectId)
})
</script>

<style lang="scss" scoped>
.project-detail {
  .stats-row {
    margin: 20px 0;
  }
  
  .tasks-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
}
</style>
