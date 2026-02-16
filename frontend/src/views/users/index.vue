<template>
  <div class="users">
    <!-- 操作栏 -->
    <div class="toolbar">
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新建用户
      </el-button>
      
      <div class="filter-group">
        <el-select v-model="filter.dept" placeholder="部门" clearable style="width: 150px">
          <el-option v-for="d in departments" :key="d.id" :label="d.name" :value="d.id" />
        </el-select>
        
        <el-select v-model="filter.role" placeholder="角色" clearable style="width: 120px">
          <el-option label="管理员" value="admin" />
          <el-option label="部门领导" value="dept_manager" />
          <el-option label="班组长" value="team_leader" />
          <el-option label="工人" value="worker" />
        </el-select>
        
        <el-input
          v-model="filter.keyword"
          placeholder="搜索用户名/姓名"
          style="width: 200px"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
    </div>
    
    <!-- 用户列表 -->
    <el-table :data="userList" v-loading="loading">
      <el-table-column label="用户" min-width="200">
        <template #default="{ row }">
          <div class="user-info">
            <el-avatar :size="40" :src="row.avatar_url">
              {{ row.real_name?.[0] || row.username?.[0] }}
            </el-avatar>
            <div class="user-detail">
              <div class="name">{{ row.real_name || row.username }}</div>
              <div class="username">{{ row.username }}</div>
            </div>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column prop="dept_name" label="部门" width="120" />
      
      <el-table-column prop="team_name" label="班组" width="120" />
      
      <el-table-column prop="role" label="角色" width="100">
        <template #default="{ row }">
          <el-tag :type="getRoleType(row.role)">
            {{ getRoleText(row.role) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="phone" label="电话" width="130" />
      
      <el-table-column prop="email" label="邮箱" min-width="180" />
      
      <el-table-column prop="last_login_at" label="最后登录" width="160">
        <template #default="{ row }">
          {{ row.last_login_at || '-' }}
        </template>
      </el-table-column>
      
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-switch
            v-model="row.is_active"
            @change="(val) => handleStatusChange(row, val)"
          />
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button link type="primary" @click="handleResetPassword(row)">重置密码</el-button>
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
    
    <!-- 用户编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑用户' : '新建用户'" width="500px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" :disabled="isEdit" />
        </el-form-item>
        
        <el-form-item label="姓名" prop="real_name">
          <el-input v-model="form.real_name" />
        </el-form-item>
        
        <el-form-item label="密码" prop="password" v-if="!isEdit">
          <el-input v-model="form.password" type="password" show-password />
        </el-form-item>
        
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" placeholder="选择角色">
            <el-option label="管理员" value="admin" />
            <el-option label="部门领导" value="dept_manager" />
            <el-option label="班组长" value="team_leader" />
            <el-option label="工人" value="worker" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="部门">
          <el-select v-model="form.dept_id" placeholder="选择部门" clearable @change="handleDeptChange">
            <el-option v-for="d in departments" :key="d.id" :label="d.name" :value="d.id" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="班组">
          <el-select v-model="form.team_id" placeholder="选择班组" clearable :disabled="!form.dept_id">
            <el-option v-for="t in filteredTeams" :key="t.id" :label="t.name" :value="t.id" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="电话">
          <el-input v-model="form.phone" />
        </el-form-item>
        
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm" :loading="submitting">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const formRef = ref()

const filter = reactive({
  dept: null,
  role: '',
  keyword: ''
})

const departments = ref([
  { id: 1, name: '设计部' },
  { id: 2, name: '生产部' },
  { id: 3, name: '采购部' },
  { id: 4, name: '质检部' }
])

const teams = ref([
  { id: 1, name: '结构设计组', dept_id: 1 },
  { id: 2, name: '铝合金班组', dept_id: 2 },
  { id: 3, name: '焊接班组', dept_id: 2 },
  { id: 4, name: '采购组', dept_id: 3 }
])

const filteredTeams = computed(() => {
  if (!form.dept_id) return []
  return teams.value.filter(t => t.dept_id === form.dept_id)
})

const userList = ref([
  {
    id: 1,
    username: 'admin',
    real_name: '管理员',
    role: 'admin',
    dept_name: '综合部',
    team_name: '',
    phone: '13800138000',
    email: 'admin@yacht.com',
    is_active: true,
    last_login_at: '2024-02-15 10:30:00'
  },
  {
    id: 2,
    username: 'zhangsan',
    real_name: '张三',
    role: 'dept_manager',
    dept_name: '设计部',
    team_name: '',
    phone: '13900139000',
    email: 'zs@yacht.com',
    is_active: true,
    last_login_at: '2024-02-14 16:45:00'
  },
  {
    id: 3,
    username: 'lisi',
    real_name: '李四',
    role: 'team_leader',
    dept_name: '生产部',
    team_name: '铝合金班组',
    phone: '13700137000',
    email: 'ls@yacht.com',
    is_active: true,
    last_login_at: null
  }
])

const form = reactive({
  id: null,
  username: '',
  real_name: '',
  password: '',
  role: 'worker',
  dept_id: null,
  team_id: null,
  phone: '',
  email: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  real_name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  password: [{ required: !isEdit.value, message: '请输入密码', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }]
}

const getRoleType = (role: string) => {
  const map: Record<string, string> = {
    admin: 'danger',
    dept_manager: 'warning',
    team_leader: 'success',
    worker: ''
  }
  return map[role] || ''
}

const getRoleText = (role: string) => {
  const map: Record<string, string> = {
    admin: '管理员',
    dept_manager: '部门领导',
    team_leader: '班组长',
    worker: '工人'
  }
  return map[role] || role
}

const handleCreate = () => {
  isEdit.value = false
  form.id = null
  form.username = ''
  form.real_name = ''
  form.password = ''
  form.role = 'worker'
  form.dept_id = null
  form.team_id = null
  form.phone = ''
  form.email = ''
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  isEdit.value = true
  Object.assign(form, row)
  dialogVisible.value = true
}

const handleDeptChange = () => {
  form.team_id = null
}

const submitForm = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  
  submitting.value = true
  try {
    // TODO: 调用 API
    await new Promise(resolve => setTimeout(resolve, 500))
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    dialogVisible.value = false
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    submitting.value = false
  }
}

const handleStatusChange = (row: any, val: boolean) => {
  // TODO: 调用 API 更新状态
  ElMessage.success(val ? '用户已启用' : '用户已禁用')
}

const handleResetPassword = async (row: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要重置 ${row.real_name} 的密码吗？`,
      '确认重置',
      { type: 'warning' }
    )
    // TODO: 调用 API
    ElMessage.success('密码已重置为：123456')
  } catch {
    // 取消
  }
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 ${row.real_name} 吗？`,
      '确认删除',
      { type: 'warning' }
    )
    // TODO: 调用 API
    ElMessage.success('删除成功')
  } catch {
    // 取消
  }
}
</script>

<style lang="scss" scoped>
.users {
  .toolbar {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    
    .filter-group {
      display: flex;
      gap: 12px;
    }
  }
  
  .user-info {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .user-detail {
      .name {
        font-weight: 500;
        font-size: 14px;
      }
      
      .username {
        font-size: 12px;
        color: #999;
      }
    }
  }
  
  .pagination {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
  }
}
</style>
