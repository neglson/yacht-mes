import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, getUserInfo } from '@/api/auth'
import type { UserInfo, LoginForm } from '@/types/user'

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref<string>(localStorage.getItem('token') || '')
  const userInfo = ref<UserInfo | null>(null)
  
  // Getters
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.role === 'admin')
  const isManager = computed(() => 
    ['admin', 'dept_manager', 'team_leader'].includes(userInfo.value?.role || '')
  )
  
  // Actions
  const login = async (form: LoginForm) => {
    const res = await loginApi(form)
    token.value = res.access_token
    userInfo.value = res.user
    localStorage.setItem('token', res.access_token)
    return res
  }
  
  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }
  
  const fetchUserInfo = async () => {
    if (!token.value) return
    try {
      const res = await getUserInfo()
      userInfo.value = res
    } catch {
      logout()
    }
  }
  
  return {
    token,
    userInfo,
    isLoggedIn,
    isAdmin,
    isManager,
    login,
    logout,
    fetchUserInfo
  }
})
