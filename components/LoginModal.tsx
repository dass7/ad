'use client'

import { useState, useEffect } from 'react'
import { X, Loader2, Shield } from 'lucide-react'
import type { UserSession } from '@/types'

interface Props {
  onClose: () => void
  onLogin: (user: UserSession) => void
}

export default function LoginModal({ onClose, onLogin }: Props) {
  const [loading, setLoading] = useState(false)
  const [adminMode, setAdminMode] = useState(false)
  const [adminPass, setAdminPass] = useState('')
  const [adminError, setAdminError] = useState('')

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const userParam = params.get('user')
    if (userParam) {
      try {
        const userData = JSON.parse(decodeURIComponent(userParam))
        onLogin(userData)
        window.history.replaceState({}, '', window.location.pathname)
      } catch {}
    }
  }, [onLogin])

  const handleQQLogin = () => {
    setLoading(true)
    window.location.href = '/api/auth/qq'
  }

  const handleAdminLogin = () => {
    const ADMIN_PASSWORD = process.env.NEXT_PUBLIC_ADMIN_PASSWORD || 'admin123'
    if (adminPass === ADMIN_PASSWORD) {
      const adminUser: UserSession = {
        openid: 'admin',
        nickname: '管理员',
        avatar: '',
        isAdmin: true,
      }
      onLogin(adminUser)
    } else {
      setAdminError('密码错误')
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in"
      onClick={e => e.target === e.currentTarget && onClose()}
    >
      <div className="bg-white rounded-2xl w-full max-w-sm shadow-xl">
        <div className="flex justify-center pt-3 pb-1 sm:hidden">
          <div className="w-10 h-1 bg-slate-200 rounded-full" />
        </div>

        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100">
          <h2 className="text-lg font-semibold text-slate-800">
            {adminMode ? '管理员登录' : '登录账号'}
          </h2>
          <button onClick={onClose} className="p-1.5 hover:bg-slate-100 rounded-lg transition-colors">
            <X className="w-4 h-4 text-slate-500" />
          </button>
        </div>

        <div className="p-6 space-y-4">
          {!adminMode ? (
            <>
              <p className="text-sm text-slate-500 text-center">
                使用 QQ 账号登录，即可填写报名信息
              </p>

              <button
                onClick={handleQQLogin}
                disabled={loading}
                className="w-full flex items-center justify-center gap-3 bg-[#12B7F5] hover:bg-[#0ea5e0] disabled:opacity-70 text-white font-medium py-3.5 rounded-xl transition-colors"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    正在跳转...
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm4.5 14.5c-.8.5-2.2.8-3 .8-.5 0-1-.1-1.5-.2-.5.3-1.2.7-2 .7-.5 0-1-.1-1.5-.4 0 0 .5-1.5.5-2.5C7.5 13.7 7 12 7 10.5 7 8 9 6.5 12 6.5s5 1.5 5 4c0 1.5-.5 3.2-1.5 4.1.1 1 .5 2.5.5 2.5-.5.2-1 .3-1.5.3-.7 0-1.4-.3-2-.9z"/>
                    </svg>
                    QQ 一键登录
                  </>
                )}
              </button>

              <div className="text-center">
                <button
                  onClick={() => setAdminMode(true)}
                  className="text-xs text-slate-400 hover:text-slate-600 transition-colors"
                >
                  管理员入口
                </button>
              </div>
            </>
          ) : (
            <>
              <p className="text-sm text-slate-500 text-center flex items-center justify-center gap-1.5">
                <Shield className="w-4 h-4 text-purple-500" />
                输入管理员密码
              </p>
              <input
                type="password"
                value={adminPass}
                onChange={e => { setAdminPass(e.target.value); setAdminError('') }}
                onKeyDown={e => e.key === 'Enter' && handleAdminLogin()}
                placeholder="管理员密码"
                autoFocus
                className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent"
              />
              {adminError && (
                <p className="text-xs text-red-500 text-center">{adminError}</p>
              )}
              <button
                onClick={handleAdminLogin}
                className="w-full bg-slate-800 hover:bg-slate-700 text-white font-medium py-3 rounded-xl transition-colors"
              >
                进入管理员模式
              </button>
              <div className="text-center">
                <button
                  onClick={() => { setAdminMode(false); setAdminError('') }}
                  className="text-xs text-slate-400 hover:text-slate-600"
                >
                  ← 返回 QQ 登录
                </button>
              </div>
            </>
          )}

          <p className="text-xs text-slate-400 text-center">
            登录即代表同意数据用于创新大赛统计
          </p>
        </div>
      </div>
    </div>
  )
}
