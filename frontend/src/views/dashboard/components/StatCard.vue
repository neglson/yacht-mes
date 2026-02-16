<template>
  <el-card class="stat-card" :style="{ borderLeft: `4px solid ${color}` }">
    <div class="stat-content">
      <div class="stat-info">
        <p class="stat-title">{{ title }}</p>
        <p class="stat-value" :style="{ color }">{{ value }}</p>
      </div>
      <div class="stat-icon" :style="{ backgroundColor: color + '20' }">
        <el-icon :size="32" :color="color">
          <component :is="icon" />
        </el-icon>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  value: number
  icon: string
  color: string
}>()
</script>

<style lang="scss" scoped>
.stat-card {
  .stat-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .stat-info {
    .stat-title {
      color: #666;
      font-size: 14px;
      margin-bottom: 8px;
    }
    
    .stat-value {
      font-size: 28px;
      font-weight: 600;
    }
  }
  
  .stat-icon {
    width: 60px;
    height: 60px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
