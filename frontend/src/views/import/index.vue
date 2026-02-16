<template>
  <div class="data-import">
    <el-page-header title="数据导入" content="从 Excel 导入项目、任务、物料等初始数据" @back="$router.back()" />
    
    <el-card class="import-card">
      <template #header>
        <div class="card-header">
          <span>📁 上传 Excel 文件</span>
          <el-button type="primary" link @click="downloadTemplate">
            <el-icon><Download /></el-icon>
            下载模板
          </el-button>
        </div>
      </template>
      
      <!-- 上传区域 -->
      <el-upload
        class="upload-area"
        drag
        action="/api/import/excel"
        :headers="uploadHeaders"
        :on-success="handleSuccess"
        :on-error="handleError"
        :before-upload="beforeUpload"
        accept=".xlsx,.xls"
      >
        <el-icon class="upload-icon"><Upload /></el-icon>
        <div class="upload-text">
          拖拽文件到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="upload-tip">
            支持 .xlsx, .xls 格式，文件大小不超过 10MB
            <br>
            请按照模板格式准备数据
          </div>
        </template>
      </el-upload>
    </el-card>
    
    <!-- 预览数据 -->
    <template v-if="previewData">
      <el-card class="preview-card">
        <template #header>
        <div class="card-header">
          <span>📊 导入结果</span>
        </div>
      </template>
        
        <!-- 统计信息 -->
        <el-row :gutter="20" class="stats-row">
          <el-col :span="4" v-for="(count, name) in previewData.preview" :key="name">
            <el-statistic :title="getStatTitle(name)" :value="count" />
          </el-col>
        </el-row>
        
        <!-- 示例数据 -->
        <el-tabs v-model="activeTab" class="preview-tabs">
          <el-tab-pane label="项目" name="projects" v-if="previewData.sample_data?.projects?.length">
            <el-table :data="previewData.sample_data.projects" size="small">
              <el-table-column prop="project_no" label="项目编号" />
              <el-table-column prop="yacht_name" label="游艇名称" />
              <el-table-column prop="yacht_model" label="船型" />
              <el-table-column prop="status" label="状态" />
            </el-table>
          </el-tab-pane>
          
          <el-tab-pane label="任务" name="tasks" v-if="previewData.sample_data?.tasks?.length">
            <el-table :data="previewData.sample_data.tasks" size="small">
              <el-table-column prop="task_no" label="序号" width="80" />
              <el-table-column prop="name" label="任务名称" />
              <el-table-column prop="task_type" label="类型" />
              <el-table-column prop="status" label="状态" />
            </el-table>
          </el-tab-pane>
          
          <el-tab-pane label="物料" name="materials" v-if="previewData.sample_data?.materials?.length">
            <el-table :data="previewData.sample_data.materials" size="small">
              <el-table-column prop="code" label="物料编码" />
              <el-table-column prop="name" label="物料名称" />
              <el-table-column prop="brand" label="品牌" />
              <el-table-column prop="unit" label="单位" />
            </el-table>
          </el-tab-pane>
        </el-tabs>
        
        <!-- 警告信息 -->
        <el-alert
          v-if="previewData.warnings?.length"
          :title="`警告 (${previewData.warnings.length})`"
          type="warning"
          :closable="false"
          class="alert-box"
        >
          <ul>
            <li v-for="(warning, index) in previewData.warnings" :key="index">{{ warning }}</li>
          </ul>
        </el-alert>
        
        <!-- 错误信息 -->
        <el-alert
          v-if="previewData.errors?.length"
          :title="`错误 (${previewData.errors.length})`"
          type="error"
          :closable="false"
          class="alert-box"
        >
          <ul>
            <li v-for="(error, index) in previewData.errors" :key="index">{{ error }}</li>
          </ul>
        </el-alert>
      </el-card>
    </template>
    
    <!-- 导入说明 -->
    <el-card class="help-card">
      <template #header>
        <span>📖 导入说明</span>
      </template>
      
      <el-collapse v-model="activeCollapse">
        <el-collapse-item title="支持的 Sheet 名称" name="1">
          <ul>
            <li><strong>项目</strong> - 游艇项目基本信息</li>
            <li><strong>时间轴</strong> - 建造任务计划与实际进度</li>
            <li><strong>物料</strong> - 物料清单与库存设置</li>
            <li><strong>采购</strong> - 采购订单信息</li>
            <li><strong>部门</strong> - 部门组织架构</li>
            <li><strong>班组</strong> - 生产班组信息</li>
            <li><strong>用户</strong> - 系统用户账号</li>
          </ul>
        </el-collapse-item>
        
        <el-collapse-item title="数据格式要求" name="2">
          <ul>
            <li>日期格式: YYYY-MM-DD 或 YYYY/MM/DD</li>
            <li>状态值: 未开始/进行中/已完成/延期/已取消</li>
            <li>角色值: 管理员/部门领导/班组长/工人</li>
            <li>数字字段: 支持整数和小数</li>
          </ul>
        </el-collapse-item>
      </el-collapse>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const previewData = ref<any>(null)
const activeTab = ref('projects')
const activeCollapse = ref(['1'])
const importing = ref(false)

const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${userStore.token}`
}))

const getStatTitle = (name: string) => {
  const titles: Record<string, string> = {
    projects: '项目',
    tasks: '任务',
    materials: '物料',
    procurement: '采购',
    departments: '部门',
    teams: '班组',
    users: '用户'
  }
  return titles[name] || name
}

const beforeUpload = (file: File) => {
  const isExcel = file.name.endsWith('.xlsx') || file.name.endsWith('.xls')
  const isLt10M = file.size / 1024 / 1024 < 10
  
  if (!isExcel) {
    ElMessage.error('只支持 .xlsx 或 .xls 文件')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB')
    return false
  }
  return true
}

const handleSuccess = (response: any) => {
  previewData.value = response
  if (response.errors?.length > 0) {
    ElMessage.warning(`导入完成，但有 ${response.errors.length} 个错误`)
  } else {
    ElMessage.success('数据导入成功')
  }
}

const handleError = (error: any) => {
  ElMessage.error(error.message || '文件上传失败')
}

const confirmImport = async () => {
  importing.value = true
  try {
    // TODO: 调用确认导入 API
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('数据导入成功')
    previewData.value = null
  } catch (error: any) {
    ElMessage.error(error.message || '导入失败')
  } finally {
    importing.value = false
  }
}

const downloadTemplate = () => {
  // TODO: 下载模板文件
  ElMessage.info('模板下载功能开发中')
}
</script>

<style lang="scss" scoped>
.data-import {
  .import-card {
    margin-top: 20px;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .upload-area {
    :deep(.el-upload-dragger) {
      width: 100%;
      height: 200px;
    }
    
    .upload-icon {
      font-size: 48px;
      color: #409EFF;
      margin-bottom: 16px;
    }
    
    .upload-text {
      font-size: 16px;
      color: #666;
      
      em {
        color: #409EFF;
        font-style: normal;
      }
    }
    
    .upload-tip {
      margin-top: 16px;
      color: #999;
      font-size: 14px;
    }
  }
  
  .preview-card {
    margin-top: 20px;
    
    .stats-row {
      margin-bottom: 20px;
    }
    
    .preview-tabs {
      margin-top: 20px;
    }
    
    .alert-box {
      margin-top: 16px;
    }
  }
  
  .help-card {
    margin-top: 20px;
    
    ul {
      padding-left: 20px;
      
      li {
        margin-bottom: 8px;
        line-height: 1.6;
      }
    }
  }
}
</style>
