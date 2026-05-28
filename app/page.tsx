'use client'

export const dynamic = 'force-dynamic'

import { useState, useEffect, useCallback, useRef } from 'react'
import { supabase } from '@/lib/supabase'
import type { Group, UserSession } from '@/types'
import Header from '@/components/Header'
import GroupRow from '@/components/GroupRow'
import LoginModal from '@/components/LoginModal'
import OnlineUsers from '@/components/OnlineUsers'
import { CheckCircle, AlertCircle } from 'lucide-react'

export default function Home() {
  const [user, setUser] = useState<UserSession | null>(null)
  const [groups, setGroups] = useState<Group[]>([])
  const [showLogin, setShowLogin] = useState(false)
  const [saving, setSaving] = useState<number | null>(null)
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle')
  const [onlineUsers, setOnlineUsers] = useState<any[]>([])
  const presenceChannelRef = useRef<any>(null)

  // Load user from sessionStorage
  useEffect(() => {
    const stored = sessionStorage.getItem('qq_user')
    if (stored) {
      try { setUser(JSON.parse(stored)) } catch {}
    }
  }, [])

  // Fetch groups
  const fetchGroups = useCallback(async () => {
    const { data } = await supabase
      .from('groups')
      .select('*')
      .order('group_number')
    if (data) setGroups(data)
  }, [])

  useEffect(() => { fetchGroups() }, [fetchGroups])

  // Real-time subscription
  useEffect(() => {
    const channel = supabase
      .channel('groups-changes')
      .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'groups',
      }, (payload) => {
        if (payload.eventType === 'UPDATE') {
          setGroups(prev => prev.map(g =>
            g.id === (payload.new as Group).id ? payload.new as Group : g
          ))
        }
      })
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [])

  // Presence tracking
  useEffect(() => {
    if (!user) return
    const channel = supabase.channel('online-users', {
      config: { presence: { key: user.openid } }
    })
    channel
      .on('presence', { event: 'sync' }, () => {
        const state = channel.presenceState()
        const users = Object.values(state).flat() as any[]
        setOnlineUsers(users)
      })
      .subscribe(async (status) => {
        if (status === 'SUBSCRIBED') {
          await channel.track({
            openid: user.openid,
            nickname: user.nickname,
            avatar: user.avatar,
            online_at: new Date().toISOString(),
          })
        }
      })
    presenceChannelRef.current = channel
    return () => { supabase.removeChannel(channel) }
  }, [user])

  const handleUpdate = useCallback(async (
    groupId: number,
    groupNumber: number,
    field: 'members' | 'project_name',
    value: string,
    oldValue: string
  ) => {
    if (!user) { setShowLogin(true); return }
    setSaving(groupId)
    setSaveStatus('saving')

    const { error } = await supabase
      .from('groups')
      .update({
        [field]: value,
        last_updated: new Date().toISOString(),
        updated_by_name: user.nickname,
        updated_by_avatar: user.avatar,
      })
      .eq('id', groupId)

    if (!error) {
      // Log the edit
      await supabase.from('edit_logs').insert({
        user_qq: user.openid,
        user_name: user.nickname,
        user_avatar: user.avatar,
        group_number: groupNumber,
        field,
        old_value: oldValue,
        new_value: value,
      })
      setSaveStatus('saved')
      setTimeout(() => setSaveStatus('idle'), 2000)
    } else {
      setSaveStatus('error')
      setTimeout(() => setSaveStatus('idle'), 3000)
    }
    setSaving(null)
  }, [user])

  const handleLogin = (userData: UserSession) => {
    setUser(userData)
    sessionStorage.setItem('qq_user', JSON.stringify(userData))
    setShowLogin(false)
  }

  const handleLogout = () => {
    setUser(null)
    sessionStorage.removeItem('qq_user')
    if (presenceChannelRef.current) {
      presenceChannelRef.current.untrack()
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Header
        user={user}
        onLoginClick={() => setShowLogin(true)}
        onLogout={handleLogout}
        saveStatus={saveStatus}
      />

      <main className="max-w-4xl mx-auto px-4 py-6">
        {/* Title Section */}
        <div className="text-center mb-8">
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-800 mb-2">
            创新大赛报名表
          </h1>
          <p className="text-slate-500 text-sm sm:text-base">
            请各组填写组员与报名项目，每组限制 3-7 人
          </p>
          {!user && (
            <div className="mt-4 inline-flex items-center gap-2 bg-amber-50 border border-amber-200 text-amber-700 px-4 py-2 rounded-full text-sm">
              <AlertCircle className="w-4 h-4" />
              请先登录后再填写报名信息
            </div>
          )}
        </div>

        {/* Online Users */}
        <OnlineUsers users={onlineUsers} currentUser={user} />

        {/* Table Header */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden mb-4">
          {/* Desktop header */}
          <div className="hidden sm:grid grid-cols-12 bg-slate-700 text-white text-sm font-medium">
            <div className="col-span-2 px-4 py-3 text-center">组数</div>
            <div className="col-span-5 px-4 py-3">组内成员</div>
            <div className="col-span-5 px-4 py-3">报名项目</div>
          </div>

          {/* Group rows */}
          <div className="divide-y divide-slate-100">
            {groups.length > 0 ? (
              groups.map((group, index) => (
                <GroupRow
                  key={group.id}
                  group={group}
                  index={index}
                  user={user}
                  isSaving={saving === group.id}
                  onUpdate={handleUpdate}
                  onLoginRequired={() => setShowLogin(true)}
                />
              ))
            ) : (
              <div className="py-12 text-center text-slate-400">
                <div className="w-8 h-8 border-2 border-slate-300 border-t-blue-500 rounded-full animate-spin mx-auto mb-3" />
                加载中...
              </div>
            )}
          </div>
        </div>

        {/* Footer info */}
        <div className="text-center text-xs text-slate-400 mt-6 space-y-1">
          <div className="flex items-center justify-center gap-1">
            <CheckCircle className="w-3 h-3 text-green-400" />
            数据实时同步，自动保存
          </div>
          <div>每组成员限 3-7 人 · 数据修改有记录</div>
        </div>
      </main>

      {showLogin && (
        <LoginModal onClose={() => setShowLogin(false)} onLogin={handleLogin} />
      )}
    </div>
  )
}
