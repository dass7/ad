'use client'

import Image from 'next/image'
import type { UserSession } from '@/types'

interface OnlineUser {
  openid: string
  nickname: string
  avatar: string
}

interface Props {
  users: OnlineUser[]
  currentUser: UserSession | null
}

export default function OnlineUsers({ users, currentUser }: Props) {
  if (users.length === 0) return null

  const MAX_SHOWN = 8

  return (
    <div className="flex items-center gap-2 mb-4 px-1">
      <span className="text-xs text-slate-400 whitespace-nowrap">在线：</span>
      <div className="flex items-center -space-x-1.5">
        {users.slice(0, MAX_SHOWN).map((u, i) => (
          <div
            key={u.openid || i}
            className="relative"
            title={u.nickname + (u.openid === currentUser?.openid ? '（我）' : '')}
          >
            {u.avatar ? (
              <Image
                src={u.avatar}
                alt={u.nickname}
                width={24}
                height={24}
                className="rounded-full ring-2 ring-white"
              />
            ) : (
              <div className="w-6 h-6 rounded-full bg-blue-500 ring-2 ring-white flex items-center justify-center text-white text-xs font-bold">
                {u.nickname?.[0] || '?'}
              </div>
            )}
            <div className="absolute -bottom-0.5 -right-0.5 w-2 h-2 bg-green-400 rounded-full ring-1 ring-white" />
          </div>
        ))}
        {users.length > MAX_SHOWN && (
          <div className="w-6 h-6 rounded-full bg-slate-200 ring-2 ring-white flex items-center justify-center text-slate-600 text-xs font-medium">
            +{users.length - MAX_SHOWN}
          </div>
        )}
      </div>
      <span className="text-xs text-green-500 font-medium">{users.length} 人在线</span>
    </div>
  )
}
