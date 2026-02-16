// 用户类型定义

export interface UserInfo {
  id: number
  username: string
  real_name?: string
  phone?: string
  email?: string
  role: 'admin' | 'dept_manager' | 'team_leader' | 'worker'
  dept_id?: number
  team_id?: number
  avatar_url?: string
  is_active: boolean
  created_at: string
}

export interface LoginForm {
  username: string
  password: string
}

export interface LoginRes {
  access_token: string
  token_type: string
  expires_in: number
  user: UserInfo
}
