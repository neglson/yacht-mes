<template>
  <div class="breadcrumb">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item v-for="(item, index) in breadcrumbs" :key="index">
        {{ item }}
      </el-breadcrumb-item>
    </el-breadcrumb>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const breadcrumbs = computed(() => {
  const matched = route.matched
  const titles: string[] = []
  
  matched.forEach((item) => {
    if (item.meta?.title) {
      titles.push(item.meta.title as string)
    }
  })
  
  return titles
})
</script>

<style scoped>
.breadcrumb {
  padding: 0;
}
</style>
