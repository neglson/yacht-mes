<template>
  <div class="quality">
    <el-page-header title="质量管理" content="质量检测与验收" @back="$router.back()" />
    
    <div class="content">
      <el-empty description="质量管理功能开发中，敬请期待">
        <template #image>
          <el-icon :size="60" color="#67C23A"><CircleCheck /></el-icon>
        </template>
      </el-empty>
    </div>
  </div>
</template>

<style scoped>
.quality {
  .content {
    padding: 40px;
  }
}
</style>
