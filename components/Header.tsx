'use client'

import Image from 'next/image'
import Link from 'next/link'
import { Trophy, LogIn, LogOut, CheckCircle, XCircle, Loader2, Shield } from 'lucide-react'
import type { UserSession } from '@/types'

interface Props {
  user: UserSession | null
  onLoginClick: () => void
  onLogout: () => void
  saveStatus: 'idle' | 'saving' | 'saved' | 'error'
}

export default function Header({ user, onLoginClick, onLogout, saveStatus }: Props) {
  return (
    <header className="sticky top-0 z-40 bg-white border-b border-slate-200 shadow-sm">
      <div className="max-w-4xl mx-auto px-4 h-14 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <Trophy className="w-4 h-4 text-white" />
          </div>
          <span className="font-semibold text-slate-800 text-sm sm:text-base">
            创新大赛报名系统
          </span>
        </div>

        {/* Right side */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Save status */}
          {saveStatus === 'saving' && (
            <div className="flex items-center gap-1 text-xs text-slate-500">
              <Loader2 className="w-3 h-3 animate-spin" />
              <span className="hidden sm:inline">保存中...</span>
            </div>
          )}
          {saveStatus === 'saved' && (
            <div className="flex items-center gap-1 text-xs text-green-600">
              <CheckCircle className="w-3 h-3" />
              <span className="hidden sm:inline">已保存</span>
            </div>
          )}
          {saveStatus === 'error' && (
            <div className="flex items-center gap-1 text-xs text-red-500">
              <XCircle className="w-3 h-3" />
              <span className="hidden sm:inline">保存失败</span>
            </div>
          )}

          {user ? (
            <div className="flex items-center gap-2">
              {user.isAdmin && (
                <Link
                  href="/admin"
                  className="hidden sm:flex items-center gap-1 text-xs text-purple-600 bg-purple-50 px-2 py-1 rounded-full hover:bg-purple-100 transition-colors"
                >
                  <Shield className="w-3 h-3" />
                  管理员
                </Link>
              )}
              <div className="flex items-center gap-2">
                {user.avatar && (
                  <Image
                    src={user.avatar}
                    alt={user.nickname}
                    width={28}
                    height={28}
                    className="rounded-full ring-2 ring-blue-100"
                  />
                )}
                <span className="text-sm text-slate-700 hidden sm:block max-w-24 truncate">
                  {user.nickname}
                </span>
              </div>
              <button
                onClick={onLogout}
                className="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
                title="退出登录"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <button
              onClick={onLoginClick}
              className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white text-sm px-3 py-1.5 rounded-lg font-medium transition-colors"
            >
              <LogIn className="w-3.5 h-3.5" />
              QQ登录
            </button>
          )}
        </div>
      </div>
    </header>
  )
}
