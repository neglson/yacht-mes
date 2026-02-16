<template>
  <div class="tasks">
    <!-- 操作栏 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <el-button type="primary" @click="handleCreate">
          <el-icon><Plus /></el-icon>
          新建任务
        </el-button>
        
        <el-button @click="$router.push('/tasks/gantt')">
          <el-icon><Calendar /></el-icon>
          甘特图
        </el-button>
      </div>
      
      <div class="toolbar-right">
        <el-select v-model="filter.project" placeholder="选择项目" clearable style="width: 150px">
          <el-option v-for="p in projects" :key="p.id" :label="p.yacht_name" :value="p.id" />
        </el-select>
        
        <el-select v-model="filter.status" placeholder="任务状态" clearable style="width: 120px">
          <el-option label="未开始" value="not_started" />
          <el-option label="进行中" value="in_progress" />
          <el-option label="已完成" value="completed" />
          <el-option label="延期" value="delayed" />
        </el-select>
        
        <el-input
          v-model="filter.keyword"
          placeholder="搜索任务"
          style="width: 200px"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
    </div>
    
    <!-- 任务列表 -->
    <el-table :data="taskList" v-loading="loading" row-key="id" default-expand-all
>
      <el-table-column type="index" width="50" />
      
      <el-table-column prop="task_no" label="序号" width="80" />
      
      <el-table-column prop="name" label="任务名称" min-width="200">
        <template #default="{ row }">
          <div class="task-name">
            <span class="name">{{ row.name }}</span>
            <el-tag v-if="row.priority === 'urgent'" type="danger" size="small">紧急</el-tag>
            <el-tag v-else-if="row.priority === 'high'" type="warning" size="small">高</el-tag>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column prop="task_type" label="类型" width="100">
        <template #default="{ row }">
          {{ getTaskTypeText(row.task_type) }}
        </template>
      </el-table-column>
      
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="progress_percent" label="进度" width="150">
        <template #default="{ row }">
          <el-progress :percentage="row.progress_percent || 0" :status="row.progress_percent === 100 ? 'success' : ''" />
        </template>
      </el-table-column>
      
      <el-table-column prop="manager_name" label="负责人" width="100" />
      
      <el-table-column prop="plan_start" label="计划开始" width="110" />
      
      <el-table-column prop="plan_end" label="计划结束" width="110" />
      
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleView(row)">查看</el-button>
          <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button v-if="row.status !== 'completed'" link type="success" @click="handleReport(row)">报工</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        layout="total, sizes, prev, pager, next"
        :page-sizes="[10, 20, 50, 100]"
      />
    </div>
    
    <!-- 报工对话框 -->
    <el-dialog v-model="reportDialogVisible" title="任务报工" width="500px">
      <el-form :model="reportForm" label-width="100px">
        <el-form-item label="任务">
          <span>{{ currentTask?.name }}</span>
        </el-form-item>
        
        <el-form-item label="今日工时">
          <el-input-number v-model="reportForm.work_hours" :min="1" :max="24" />
        </el-form-item>
        
        <el-form-item label="完成进度">
          <el-slider v-model="reportForm.progress_percent" show-input />
        </el-form-item>
        
        <el-form-item label="工作描述">
          <el-input v-model="reportForm.description" type="textarea" rows="3" />
        </el-form-item>
        
        <el-form-item label="上传照片">
          <el-upload
            action="/api/attachments/upload"
            list-type="picture-card"
            :on-success="handlePhotoSuccess"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="reportDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReport" :loading="submitting">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const filter = reactive({
  project: null,
  status: '',
  keyword: ''
})

const projects = ref([
  { id: 1, yacht_name: '海鹰号' },
  { id: 2, yacht_name: '蓝鲸号' }
])

const taskList = ref([
  {
    id: 1,
    task_no: '1.1',
    name: '飞桥结构设计交付',
    task_type: 'design',
    status: 'completed',
    priority: 'high',
    progress_percent: 100,
    manager_name: '张三',
    plan_start: '2024-01-15',
    plan_end: '2024-02-15'
  },
  {
    id: 2,
    task_no: '1.2',
    name: '船体结构生产放样及制作',
    task_type: 'hull_construction',
    status: 'in_progress',
    priority: 'urgent',
    progress_percent: 65,
    manager_name: '李四',
    plan_start: '2024-02-01',
    plan_end: '2024-04-30'
  },
  {
    id: 3,
    task_no: '1.3',
    name: '外板及甲板矫正',
    task_type: 'hull_construction',
    status: 'not_started',
    priority: 'medium',
    progress_percent: 0,
    manager_name: '王五',
    plan_start: '2024-03-01',
    plan_end: '2024-05-15'
  }
])

const reportDialogVisible = ref(false)
const submitting = ref(false)
const currentTask = ref<any>(null)
const reportForm = reactive({
  work_hours: 8,
  progress_percent: 0,
  description: '',
  photos: []
})

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    not_started: 'info',
    in_progress: 'primary',
    completed: 'success',
    delayed: 'danger',
    cancelled: 'info'
  }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    not_started: '未开始',
    in_progress: '进行中',
    completed: '已完成',
    delayed: '延期',
    cancelled: '已取消'
  }
  return map[status] || status
}

const getTaskTypeText = (type: string) => {
  const map: Record<string, string> = {
    design: '设计',
    hull_construction: '船体制作',
    procurement: '采购配料',
    outfitting: '舾装',
    interior: '内装',
    commissioning: '调试'
  }
  return map[type] || type
}

const handleCreate = () => {
  // TODO: 打开新建任务对话框
}

const handleView = (row: any) => {
  // TODO: 查看任务详情
}

const handleEdit = (row: any) => {
  // TODO: 编辑任务
}

const handleReport = (row: any) => {
  currentTask.value = row
  reportForm.progress_percent = row.progress_percent || 0
  reportForm.work_hours = 8
  reportForm.description = ''
  reportForm.photos = []
  reportDialogVisible.value = true
}

const handlePhotoSuccess = (response: any) => {
  reportForm.photos.push(response.url)
}

const submitReport = async () => {
  submitting.value = true
  try {
    // TODO: 调用报工 API
    await new Promise(resolve => setTimeout(resolve, 500))
    ElMessage.success('报工成功')
    reportDialogVisible.value = false
  } catch (error: any) {
    ElMessage.error(error.message || '报工失败')
  } finally {
    submitting.value = false
  }
}
</script>

<style lang="scss" scoped>
.tasks {
  .toolbar {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    gap: 16px;
    
    .toolbar-left,
    .toolbar-right {
      display: flex;
      gap: 12px;
    }
  }
  
  .task-name {
    display: flex;
    align-items: center;
    gap: 8px;
    
    .name {
      font-weight: 500;
    }
  }
  
  .pagination {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
  }
}
</style>
