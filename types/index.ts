export interface Group {
  id: number
  group_number: number
  group_name: string
  members: string
  project_name: string
  last_updated: string
  updated_by_name: string
  updated_by_avatar: string
}

export interface EditLog {
  id: number
  user_qq: string
  user_name: string
  user_avatar: string
  group_number: number
  field: string
  old_value: string
  new_value: string
  created_at: string
}

export interface QQUser {
  openid: string
  nickname: string
  figureurl_qq_2: string
  figureurl_qq_1: string
}

export interface UserSession {
  openid: string
  nickname: string
  avatar: string
  isAdmin: boolean
}
