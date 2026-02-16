import api from './index'
import type { LoginForm, LoginRes, UserInfo } from '@/types/user'

export const login = (data: LoginForm): Promise<LoginRes> => {
  const formData = new URLSearchParams()
  formData.append('username', data.username)
  formData.append('password', data.password)
  
  return api.post('/auth/login', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  })
}

export const getUserInfo = (): Promise<UserInfo> => {
  return api.get('/auth/me')
}

export const logout = () => {
  return api.post('/auth/logout')
}
