<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-left">
        <div class="brand">
          <el-icon size="64" color="#fff"><Ship /></el-icon>
          <h1>Yacht MES</h1>
          <p>铝合金电动游艇建造管理系统</p>
        </div>
        <div class="features">
          <div class="feature-item">
            <el-icon><Calendar /></el-icon>
            <span>智能排产</span>
          </div>
          <div class="feature-item">
            <el-icon><Box /></el-icon>
            <span>物料追溯</span>
          </div>
          <div class="feature-item">
            <el-icon><Cpu /></el-icon>
            <span>AI 助手</span>
          </div>
        </div>
      </div>
      
      <div class="login-right">
        <div class="login-form-wrapper">
          <h2>欢迎登录</h2>
          
          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            size="large"
            @keyup.enter="handleLogin"
          >
            <el-form-item prop="username">
              <el-input
                v-model="form.username"
                placeholder="用户名"
                :prefix-icon="User"
                clearable
              />
            </el-form-item>
            
            <el-form-item prop="password">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="密码"
                :prefix-icon="Lock"
                show-password
                clearable
              />
            </el-form-item>
            
            <el-form-item>
              <el-button
                type="primary"
                :loading="loading"
                class="login-btn"
                @click="handleLogin"
              >
                登录
              </el-button>
            </el-form-item>
          </el-form>
          
          <div class="login-tips">
            <p>测试账号：admin / admin</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  
  loading.value = true
  try {
    await userStore.login(form)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error: any) {
    ElMessage.error(error.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-container {
  display: flex;
  width: 900px;
  height: 500px;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.login-left {
  flex: 1;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 60px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  color: #fff;
  
  .brand {
    h1 {
      font-size: 36px;
      margin: 20px 0 10px;
    }
    
    p {
      font-size: 16px;
      opacity: 0.8;
    }
  }
  
  .features {
    .feature-item {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 20px;
      font-size: 16px;
      
      .el-icon {
        font-size: 24px;
        color: #409EFF;
      }
    }
  }
}

.login-right {
  width: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  
  .login-form-wrapper {
    width: 100%;
    
    h2 {
      text-align: center;
      margin-bottom: 30px;
      color: #333;
    }
    
    .login-btn {
      width: 100%;
    }
    
    .login-tips {
      text-align: center;
      color: #999;
      font-size: 12px;
      margin-top: 20px;
    }
  }
}
</style>
