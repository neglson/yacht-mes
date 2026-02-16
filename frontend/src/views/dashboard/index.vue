<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <stat-card
          title="进行中的项目"
          :value="stats.activeProjects"
          icon="Ship"
          color="#409EFF"
        />
      </el-col>
      <el-col :span="6">
        <stat-card
          title="今日任务"
          :value="stats.todayTasks"
          icon="List"
          color="#67C23A"
        />
      </el-col>
      <el-col :span="6">
        <stat-card
          title="待审批采购"
          :value="stats.pendingProcurement"
          icon="ShoppingCart"
          color="#E6A23C"
        />
      </el-col>
      <el-col :span="6">
        <stat-card
          title="库存预警"
          :value="stats.inventoryAlert"
          icon="Warning"
          color="#F56C6C"
        />
      </el-col>
    </el-row>
    
    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>项目进度概览</span>
              <el-radio-group v-model="timeRange" size="small">
                <el-radio-button label="week">本周</el-radio-button>
                <el-radio-button label="month">本月</el-radio-button>
                <el-radio-button label="quarter">本季</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container">
            <project-chart :time-range="timeRange" />
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>任务状态分布</span>
          </template>
          <div class="chart-container">
            <task-pie-chart />
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 快捷操作和待办 -->
    <el-row :gutter="20" class="action-row">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>快捷操作</span>
          </template>
          <div class="quick-actions">
            <el-button type="primary" @click="$router.push('/tasks')">
              <el-icon><Plus /></el-icon>
              新建任务
            </el-button>
            <el-button @click="$router.push('/procurement')">
              <el-icon><ShoppingCart /></el-icon>
              采购申请
            </el-button>
            <el-button @click="$router.push('/inventory')">
              <el-icon><Box /></el-icon>
              入库登记
            </el-button>
            <el-button @click="$router.push('/quality')">
              <el-icon><CircleCheck /></el-icon>
              质量检测
            </el-button>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>我的待办</span>
            <el-link type="primary" @click="$router.push('/tasks')">查看全部</el-link>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="task in pendingTasks"
              :key="task.id"
              :type="task.priority === 'urgent' ? 'danger' : 'primary'"
              :timestamp="task.deadline"
            >
              {{ task.name }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import StatCard from './components/StatCard.vue'
import ProjectChart from './components/ProjectChart.vue'
import TaskPieChart from './components/TaskPieChart.vue'

const timeRange = ref('week')

const stats = reactive({
  activeProjects: 5,
  todayTasks: 12,
  pendingProcurement: 3,
  inventoryAlert: 2
})

const pendingTasks = ref([
  { id: 1, name: '飞桥结构设计审核', priority: 'urgent', deadline: '今天 18:00' },
  { id: 2, name: '铝合金板材入库验收', priority: 'normal', deadline: '明天 10:00' },
  { id: 3, name: '电气系统接线检查', priority: 'normal', deadline: '后天 14:00' }
])
</script>

<style lang="scss" scoped>
.dashboard {
  .chart-row,
  .action-row {
    margin-top: 20px;
  }
  
  .chart-container {
    height: 300px;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .quick-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    
    .el-button {
      flex: 1;
      min-width: 120px;
    }
  }
}
</style>
