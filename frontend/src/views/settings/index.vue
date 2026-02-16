<template>
  <div class="settings">
    <el-page-header title="系统设置" @back="$router.back()" />
    
    <el-tabs v-model="activeTab" class="settings-tabs">
      <el-tab-pane label="基本设置" name="basic">
        <el-form :model="basicForm" label-width="120px">
          <el-form-item label="系统名称">
            <el-input v-model="basicForm.systemName" />
          </el-form-item>
          
          <el-form-item label="公司Logo">
            <el-upload
              action="/api/attachments/upload"
              :show-file-list="false"
            >
              <el-button type="primary">上传Logo</el-button>
            </el-upload>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="saveBasic">保存</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      
      <el-tab-pane label="安全设置" name="security">
        <el-form :model="securityForm" label-width="120px">
          <el-form-item label="密码有效期">
            <el-input-number v-model="securityForm.passwordExpiry" :min="30" :max="180" /> 天
          </el-form-item>
          
          <el-form-item label="登录失败锁定">
            <el-switch v-model="securityForm.loginLock" />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="saveSecurity">保存</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('basic')

const basicForm = reactive({
  systemName: 'Yacht MES',
  logo: ''
})

const securityForm = reactive({
  passwordExpiry: 90,
  loginLock: true
})

const saveBasic = () => {
  ElMessage.success('保存成功')
}

const saveSecurity = () => {
  ElMessage.success('保存成功')
}
</script>

<style lang="scss" scoped>
.settings {
  .settings-tabs {
    margin-top: 20px;
    
    :deep(.el-tabs__content) {
      padding: 20px;
      background: #fff;
      border-radius: 8px;
    }
  }
}
</style>
