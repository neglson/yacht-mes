<template>
  <div class="projects">
    <!-- 操作栏 -->
    <div class="toolbar">
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新建项目
      </el-button>
      
      <el-input
        v-model="searchQuery"
        placeholder="搜索项目名称/编号"
        style="width: 300px"
        clearable
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>
    
    <!-- 项目列表 -->
    <el-table :data="projectList" v-loading="loading">
      <el-table-column prop="project_no" label="项目编号" width="120" />
      <el-table-column prop="yacht_name" label="游艇名称" />
      
      <el-table-column prop="yacht_model" label="船型" width="150" />
      
      <el-table-column prop="client_name" label="船东" width="150" />
      
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="progress_percent" label="进度" width="180">
        <template #default="{ row }">
          <el-progress :percentage="row.progress_percent || 0" />
        </template>
      </el-table-column>
      
      <el-table-column prop="plan_start" label="计划开始" width="120" />
      
      <el-table-column prop="planned_end" label="计划结束" width="120" />
      
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleView(row)">查看</el-button>
          <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

const loading = ref(false)
const searchQuery = ref('')
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

// Mock 数据
const projectList = ref([
  {
    id: 1,
    project_no: 'YT-2024-001',
    yacht_name: '海鹰号',
    yacht_model: 'HY-65',
    client_name: '张三',
    status: 'in_progress',
    progress_percent: 65,
    plan_start: '2024-01-15',
    planned_end: '2024-06-30'
  },
  {
    id: 2,
    project_no: 'YT-2024-002',
    yacht_name: '蓝鲸号',
    yacht_model: 'LJ-80',
    client_name: '李四',
    status: 'planning',
    progress_percent: 10,
    plan_start: '2024-03-01',
    planned_end: '2024-09-30'
  }
])

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    planning: 'info',
    in_progress: 'primary',
    completed: 'success',
    cancelled: 'danger'
  }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    planning: '规划中',
    in_progress: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return map[status] || status
}

const handleCreate = () => {
  // TODO: 打开创建对话框
}

const handleView = (row: any) => {
  router.push(`/projects/${row.id}`)
}

const handleEdit = (row: any) => {
  // TODO: 打开编辑对话框
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除项目 "${row.yacht_name}" 吗？`,
      '确认删除',
      { type: 'warning' }
    )
    ElMessage.success('删除成功')
  } catch {
    // 取消删除
  }
}
</script>

<style lang="scss" scoped>
.projects {
  .toolbar {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
  }
  
  .pagination {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
  }
}
</style>
