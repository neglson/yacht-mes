<template>
  <div class="gantt-page">
    <!-- 顶部工具栏 -->
    <div class="toolbar">
      <el-select v-model="selectedProject" placeholder="选择项目" style="width: 200px">
        <el-option v-for="p in projects" :key="p.id" :label="p.yacht_name" :value="p.id" />
      </el-select>
      
      <el-radio-group v-model="viewMode">
        <el-radio-button label="day">日</el-radio-button>
        <el-radio-button label="week">周</el-radio-button>
        <el-radio-button label="month">月</el-radio-button>
      </el-radio-group>
      
      <el-button @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回列表
      </el-button>
    </div>
    
    <!-- 甘特图容器 -->
    <div class="gantt-container" ref="ganttRef">
      <!-- 左侧任务列表 -->
      <div class="task-list">
        <div class="task-header">
          <div class="cell">序号</div>
          <div class="cell task-name">任务名称</div>
          <div class="cell">负责人</div>
          <div class="cell">进度</div>
        </div>
        
        <div class="task-body">
          <div
            v-for="task in tasks"
            :key="task.id"
            class="task-row"
            :class="{ 'task-completed': task.status === 'completed' }"
          >
            <div class="cell">{{ task.task_no }}</div>
            <div class="cell task-name">
              <span :style="{ paddingLeft: `${(task.level - 1) * 20}px` }">
                <el-icon v-if="task.children?.length" class="expand-icon"><ArrowDown /></el-icon>
                {{ task.name }}
              </span>
            </div>
            <div class="cell">{{ task.manager_name }}</div>
            <div class="cell">{{ task.progress_percent }}%</div>
          </div>
        </div>
      </div>
      
      <!-- 右侧时间轴 -->
      <div class="timeline">
        <!-- 时间刻度 -->
        <div class="timeline-header">
          <div
            v-for="date in dateRange"
            :key="date"
            class="date-cell"
            :class="{ 'weekend': isWeekend(date) }"
          >
            {{ formatDate(date) }}
          </div>
        </div>
        
        <!-- 任务条 -->
        <div class="timeline-body">
          <div
            v-for="task in tasks"
            :key="task.id"
            class="timeline-row"
          >
            <div
              v-if="task.plan_start && task.plan_end"
              class="task-bar"
              :class="`status-${task.status}`"
              :style="getTaskBarStyle(task)"
            >
              <div class="task-progress" :style="{ width: `${task.progress_percent}%` }" />
              <span class="task-label">{{ task.name }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import dayjs from 'dayjs'

const selectedProject = ref(1)
const viewMode = ref('week')
const ganttRef = ref()

const projects = ref([
  { id: 1, yacht_name: '海鹰号' },
  { id: 2, yacht_name: '蓝鲸号' }
])

const tasks = ref([
  {
    id: 1,
    task_no: '1.1',
    name: '飞桥结构设计交付',
    level: 1,
    status: 'completed',
    progress_percent: 100,
    manager_name: '张三',
    plan_start: '2024-01-15',
    plan_end: '2024-02-15',
    children: []
  },
  {
    id: 2,
    task_no: '1.2',
    name: '船体结构生产放样及制作',
    level: 1,
    status: 'in_progress',
    progress_percent: 65,
    manager_name: '李四',
    plan_start: '2024-02-01',
    plan_end: '2024-04-30',
    children: [
      {
        id: 21,
        task_no: '1.2.1',
        name: '放样',
        level: 2,
        status: 'completed',
        progress_percent: 100,
        manager_name: '王五',
        plan_start: '2024-02-01',
        plan_end: '2024-02-15'
      },
      {
        id: 22,
        task_no: '1.2.2',
        name: '下料',
        level: 2,
        status: 'in_progress',
        progress_percent: 80,
        manager_name: '赵六',
        plan_start: '2024-02-16',
        plan_end: '2024-03-15'
      }
    ]
  },
  {
    id: 3,
    task_no: '1.3',
    name: '外板及甲板矫正',
    level: 1,
    status: 'not_started',
    progress_percent: 0,
    manager_name: '王五',
    plan_start: '2024-03-01',
    plan_end: '2024-05-15'
  }
])

// 展开子任务
const allTasks = computed(() => {
  const result: any[] = []
  tasks.value.forEach(task => {
    result.push(task)
    if (task.children) {
      result.push(...task.children)
    }
  })
  return result
})

// 日期范围
const dateRange = computed(() => {
  const dates: string[] = []
  const start = dayjs('2024-01-01')
  const end = dayjs('2024-06-30')
  
  let current = start
  while (current.isBefore(end) || current.isSame(end)) {
    dates.push(current.format('YYYY-MM-DD'))
    current = current.add(1, 'day')
  }
  
  return dates
})

const formatDate = (date: string) => {
  return dayjs(date).format('MM-DD')
}

const isWeekend = (date: string) => {
  const day = dayjs(date).day()
  return day === 0 || day === 6
}

const getTaskBarStyle = (task: any) => {
  const start = dayjs(task.plan_start)
  const end = dayjs(task.plan_end)
  const rangeStart = dayjs(dateRange.value[0])
  
  const left = start.diff(rangeStart, 'day') * 40  // 每天40px
  const width = end.diff(start, 'day') * 40 + 40
  
  return {
    left: `${left}px`,
    width: `${width}px`
  }
}
</script>

<style lang="scss" scoped>
.gantt-page {
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
  
  .toolbar {
    display: flex;
    gap: 16px;
    margin-bottom: 16px;
    padding: 16px;
    background: #fff;
    border-radius: 8px;
  }
  
  .gantt-container {
    flex: 1;
    display: flex;
    background: #fff;
    border-radius: 8px;
    overflow: hidden;
    
    .task-list {
      width: 400px;
      border-right: 1px solid #e8e8e8;
      
      .task-header,
      .task-row {
        display: flex;
        height: 40px;
        line-height: 40px;
        border-bottom: 1px solid #f0f0f0;
        
        .cell {
          padding: 0 8px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          
          &:nth-child(1) { width: 60px; }
          &:nth-child(2) { flex: 1; }
          &:nth-child(3) { width: 80px; }
          &:nth-child(4) { width: 60px; }
        }
        
        .task-name {
          font-weight: 500;
          
          .expand-icon {
            margin-right: 4px;
            cursor: pointer;
          }
        }
      }
      
      .task-header {
        background: #fafafa;
        font-weight: 600;
      }
      
      .task-body {
        overflow-y: auto;
        
        .task-row {
          &:hover {
            background: #f5f5f5;
          }
          
          &.task-completed {
            color: #999;
          }
        }
      }
    }
    
    .timeline {
      flex: 1;
      overflow: auto;
      
      .timeline-header {
        display: flex;
        height: 40px;
        background: #fafafa;
        border-bottom: 1px solid #e8e8e8;
        
        .date-cell {
          width: 40px;
          text-align: center;
          line-height: 40px;
          font-size: 12px;
          border-right: 1px solid #f0f0f0;
          
          &.weekend {
            background: #fff7e6;
          }
        }
      }
      
      .timeline-body {
        .timeline-row {
          height: 40px;
          border-bottom: 1px solid #f0f0f0;
          position: relative;
          
          .task-bar {
            position: absolute;
            top: 8px;
            height: 24px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            padding: 0 8px;
            font-size: 12px;
            color: #fff;
            overflow: hidden;
            
            .task-progress {
              position: absolute;
              left: 0;
              top: 0;
              bottom: 0;
              background: rgba(255,255,255,0.3);
            }
            
            .task-label {
              position: relative;
              z-index: 1;
              white-space: nowrap;
            }
            
            &.status-not_started {
              background: #909399;
            }
            
            &.status-in_progress {
              background: #409EFF;
            }
            
            &.status-completed {
              background: #67C23A;
            }
            
            &.status-delayed {
              background: #F56C6C;
            }
          }
        }
      }
    }
  }
}
</style>
