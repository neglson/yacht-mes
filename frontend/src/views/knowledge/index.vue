<template>
  <div class="knowledge">
    <el-page-header title="工艺知识库" content="焊接、涂装、检验等工艺规范" @back="$router.back()" />
    
    <div class="content">
      <el-empty description="知识库功能开发中，敬请期待">
        <template #image>
          <el-icon :size="60" color="#409EFF"><Reading /></el-icon>
        </template>
      </el-empty>
    </div>
  </div>
</template>

<style scoped>
.knowledge {
  .content {
    padding: 40px;
  }
}
</style>
