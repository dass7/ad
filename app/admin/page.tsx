'use client'

export const dynamic = 'force-dynamic'

import { useState, useEffect } from 'react'
import { supabase } from '@/lib/supabase'
import { Shield, Download, Trash2, RefreshCw, ArrowLeft, Clock, User } from 'lucide-react'
import type { Group, EditLog, UserSession } from '@/types'
import Link from 'next/link'

export default function AdminPage() {
  const [user, setUser] = useState<UserSession | null>(null)
  const [groups, setGroups] = useState<Group[]>([])
  const [logs, setLogs] = useState<EditLog[]>([])
  const [activeTab, setActiveTab] = useState<'overview' | 'logs'>('overview')
  const [clearing, setClearing] = useState(false)
  const [exportKey, setExportKey] = useState('')

  useEffect(() => {
    const stored = sessionStorage.getItem('qq_user')
    if (stored) {
      try {
        const u = JSON.parse(stored)
        if (!u.isAdmin) window.location.href = '/'
        setUser(u)
      } catch { window.location.href = '/' }
    } else {
      window.location.href = '/'
    }
  }, [])

  useEffect(() => {
    if (!user?.isAdmin) return
    fetchData()
  }, [user])

  const fetchData = async () => {
    const [{ data: g }, { data: l }] = await Promise.all([
      supabase.from('groups').select('*').order('group_number'),
      supabase.from('edit_logs').select('*').order('created_at', { ascending: false }).limit(100),
    ])
    if (g) setGroups(g)
    if (l) setLogs(l)
  }

  const handleClearData = async () => {
    if (!confirm('确定要清空所有报名数据吗？此操作不可撤销！')) return
    setClearing(true)
    const { error } = await supabase
      .from('groups')
      .update({ members: '', project_name: '', updated_by_name: '', updated_by_avatar: '' })
      .gte('group_number', 1)
    if (!error) {
      await supabase.from('edit_logs').delete().gte('id', 1)
      await fetchData()
    }
    setClearing(false)
  }

  const handleExport = () => {
    window.open(`/api/export?key=${encodeURIComponent(exportKey)}`)
  }

  const totalGroups = groups.length
  const filledGroups = groups.filter(g => g.members.trim() && g.project_name.trim()).length
  const totalMembers = groups.reduce((sum, g) => {
    return sum + g.members.split('\n').map(s => s.trim()).filter(Boolean).length
  }, 0)

  if (!user?.isAdmin) return null

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 h-14 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link href="/" className="p-1.5 hover:bg-slate-100 rounded-lg">
              <ArrowLeft className="w-4 h-4 text-slate-500" />
            </Link>
            <div className="flex items-center gap-2">
              <Shield className="w-5 h-5 text-purple-600" />
              <span className="font-semibold text-slate-800">管理员面板</span>
            </div>
          </div>
          <span className="text-sm text-slate-500">{user.nickname}</span>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-6 space-y-6">
        {/* Stats */}
        <div className="grid grid-cols-3 gap-4">
          {[
            { label: '总组数', value: totalGroups, color: 'text-blue-600' },
            { label: '已填写', value: filledGroups, color: 'text-green-600' },
            { label: '参赛人数', value: totalMembers, color: 'text-purple-600' },
          ].map(stat => (
            <div key={stat.label} className="bg-white rounded-xl p-4 border border-slate-200 text-center">
              <div className={`text-2xl font-bold mb-1 ${stat.color}`}>{stat.value}</div>
              <div className="text-xs text-slate-500">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Actions */}
        <div className="bg-white rounded-xl border border-slate-200 p-4 space-y-3">
          <h3 className="font-medium text-slate-700">操作</h3>

          <div className="flex gap-2">
            <input
              type="text"
              value={exportKey}
              onChange={e => setExportKey(e.target.value)}
              placeholder="输入导出密钥"
              className="flex-1 border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-blue-400"
            />
            <button
              onClick={handleExport}
              disabled={!exportKey}
              className="flex items-center gap-1.5 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              <Download className="w-4 h-4" />
              导出 Excel
            </button>
          </div>

          <div className="flex gap-2">
            <button
              onClick={fetchData}
              className="flex items-center gap-1.5 border border-slate-200 hover:bg-slate-50 text-slate-600 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
              刷新数据
            </button>
            <button
              onClick={handleClearData}
              disabled={clearing}
              className="flex items-center gap-1.5 border border-red-200 hover:bg-red-50 text-red-600 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              <Trash2 className="w-4 h-4" />
              {clearing ? '清空中...' : '一键清空'}
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="flex border-b border-slate-200">
            {(['overview', 'logs'] as const).map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`flex-1 py-3 text-sm font-medium transition-colors ${
                  activeTab === tab
                    ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50/50'
                    : 'text-slate-500 hover:text-slate-700'
                }`}
              >
                {tab === 'overview' ? '报名总览' : '修改记录'}
              </button>
            ))}
          </div>

          {activeTab === 'overview' && (
            <div className="divide-y divide-slate-100">
              {groups.map(g => {
                const members = g.members.split('\n').map(s => s.trim()).filter(Boolean)
                const count = members.length
                return (
                  <div key={g.id} className="p-4">
                    <div className="flex items-start justify-between">
                      <div>
                        <span className="font-medium text-slate-700 text-sm">{g.group_name}</span>
                        {count > 0 && (
                          <span className={`ml-2 text-xs px-2 py-0.5 rounded-full ${
                            count >= 3 && count <= 7 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                          }`}>{count} 人</span>
                        )}
                      </div>
                      {g.project_name && (
                        <span className="text-xs text-slate-500 bg-slate-50 px-2 py-1 rounded-lg">
                          {g.project_name}
                        </span>
                      )}
                    </div>
                    {members.length > 0 && (
                      <div className="mt-2 flex flex-wrap gap-1">
                        {members.map((m, i) => (
                          <span key={i} className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full">
                            {m}
                          </span>
                        ))}
                      </div>
                    )}
                    {!g.members && !g.project_name && (
                      <p className="text-xs text-slate-400 mt-1">尚未填写</p>
                    )}
                  </div>
                )
              })}
            </div>
          )}

          {activeTab === 'logs' && (
            <div className="divide-y divide-slate-100 max-h-96 overflow-y-auto">
              {logs.length === 0 ? (
                <div className="py-8 text-center text-slate-400 text-sm">暂无修改记录</div>
              ) : logs.map(log => (
                <div key={log.id} className="p-3 flex items-start gap-3">
                  <div className="w-7 h-7 rounded-full bg-slate-200 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <User className="w-3.5 h-3.5 text-slate-500" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-1.5 flex-wrap">
                      <span className="text-xs font-medium text-slate-700">{log.user_name}</span>
                      <span className="text-xs text-slate-400">修改了</span>
                      <span className="text-xs text-blue-600">第{log.group_number}组</span>
                      <span className="text-xs text-slate-400">{log.field === 'members' ? '成员' : '项目'}</span>
                    </div>
                    <div className="mt-1 text-xs text-slate-500 flex items-center gap-1">
                      <Clock className="w-2.5 h-2.5" />
                      {new Date(log.created_at).toLocaleString('zh-CN')}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
