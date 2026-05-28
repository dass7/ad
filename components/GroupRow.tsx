'use client'

import { useState, useCallback, useRef, useEffect } from 'react'
import { Loader2, AlertTriangle, CheckCircle, User } from 'lucide-react'
import type { Group, UserSession } from '@/types'

interface Props {
  group: Group
  index: number
  user: UserSession | null
  isSaving: boolean
  onUpdate: (
    id: number,
    groupNumber: number,
    field: 'members' | 'project_name',
    value: string,
    oldValue: string
  ) => Promise<void>
  onLoginRequired: () => void
}

const MEMBER_MIN = 3
const MEMBER_MAX = 7
const COLORS = [
  'bg-blue-100 text-blue-700',
  'bg-green-100 text-green-700',
  'bg-purple-100 text-purple-700',
  'bg-orange-100 text-orange-700',
  'bg-pink-100 text-pink-700',
  'bg-cyan-100 text-cyan-700',
  'bg-yellow-100 text-yellow-700',
  'bg-rose-100 text-rose-700',
  'bg-indigo-100 text-indigo-700',
]

export default function GroupRow({ group, index, user, isSaving, onUpdate, onLoginRequired }: Props) {
  const [membersValue, setMembersValue] = useState(group.members || '')
  const [projectValue, setProjectValue] = useState(group.project_name || '')
  const [membersError, setMembersError] = useState('')
  const membersTimerRef = useRef<ReturnType<typeof setTimeout>>()
  const projectTimerRef = useRef<ReturnType<typeof setTimeout>>()
  const prevMembersRef = useRef(group.members || '')
  const prevProjectRef = useRef(group.project_name || '')

  useEffect(() => {
    setMembersValue(group.members || '')
    setProjectValue(group.project_name || '')
  }, [group.members, group.project_name])

  const getMemberCount = (val: string) =>
    val.split('\n').map(s => s.trim()).filter(Boolean).length

  const handleMembersChange = useCallback(
    (e: React.ChangeEvent<HTMLTextAreaElement>) => {
      if (!user) { onLoginRequired(); return }
      const val = e.target.value
      const count = getMemberCount(val)
      if (count > MEMBER_MAX) {
        setMembersError(`最多 ${MEMBER_MAX} 人（当前 ${count} 人）`)
        setMembersValue(val)
        return
      }
      setMembersError('')
      setMembersValue(val)
      clearTimeout(membersTimerRef.current)
      membersTimerRef.current = setTimeout(() => {
        onUpdate(group.id, group.group_number, 'members', val, prevMembersRef.current)
        prevMembersRef.current = val
      }, 800)
    },
    [user, group.id, group.group_number, onUpdate, onLoginRequired]
  )

  const handleProjectChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (!user) { onLoginRequired(); return }
      const val = e.target.value
      setProjectValue(val)
      clearTimeout(projectTimerRef.current)
      projectTimerRef.current = setTimeout(() => {
        onUpdate(group.id, group.group_number, 'project_name', val, prevProjectRef.current)
        prevProjectRef.current = val
      }, 800)
    },
    [user, group.id, group.group_number, onUpdate, onLoginRequired]
  )

  const memberCount = getMemberCount(membersValue)
  const colorClass = COLORS[index % COLORS.length]
  const isComplete = memberCount >= MEMBER_MIN && memberCount <= MEMBER_MAX && projectValue.trim()
  const hasMembers = memberCount > 0

  const formatTime = (dateStr: string) => {
    if (!dateStr) return ''
    try {
      return new Date(dateStr).toLocaleString('zh-CN', {
        month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit',
      })
    } catch { return '' }
  }

  const inputClass = (mobile?: boolean) =>
    `w-full text-sm text-slate-700 placeholder-slate-300 bg-transparent border-0 focus:outline-none focus:ring-0 leading-6 p-0${!user ? ' cursor-pointer' : ''}${mobile ? ' bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 focus:ring-1 focus:ring-blue-400 focus:border-blue-400' : ''}`

  return (
    <>
      {/* Desktop */}
      <div className="hidden sm:grid grid-cols-12 hover:bg-slate-50 transition-colors min-h-[80px]">
        <div className="col-span-2 px-4 py-3 flex flex-col items-center justify-start pt-4 gap-1.5">
          <span className={`inline-flex items-center justify-center w-16 h-7 rounded-full text-xs font-semibold ${colorClass}`}>
            {group.group_name}
          </span>
          {isComplete && <CheckCircle className="w-3.5 h-3.5 text-green-500" />}
        </div>

        <div className="col-span-5 px-3 py-3">
          <textarea
            value={membersValue}
            onChange={handleMembersChange}
            onClick={() => !user && onLoginRequired()}
            placeholder={user ? '每行一位成员\n例：张三\n李四\n王五' : '点击登录后填写...'}
            rows={Math.max(3, memberCount + 1)}
            className={inputClass()}
          />
          <div className="flex items-center justify-between mt-1">
            {membersError ? (
              <span className="text-xs text-red-500 flex items-center gap-0.5">
                <AlertTriangle className="w-3 h-3" />{membersError}
              </span>
            ) : hasMembers ? (
              <span className={`text-xs ${memberCount < MEMBER_MIN ? 'text-amber-500' : 'text-slate-400'}`}>
                {memberCount} 人{memberCount < MEMBER_MIN ? `（至少 ${MEMBER_MIN} 人）` : ' ✓'}
              </span>
            ) : <span />}
            {isSaving && <Loader2 className="w-3 h-3 animate-spin text-blue-400" />}
          </div>
        </div>

        <div className="col-span-5 px-3 py-3">
          <input
            type="text"
            value={projectValue}
            onChange={handleProjectChange}
            onClick={() => !user && onLoginRequired()}
            placeholder={user ? '填写报名项目名称' : '点击登录后填写...'}
            className={inputClass()}
          />
          {group.updated_by_name && (
            <div className="flex items-center gap-1 mt-2">
              <User className="w-2.5 h-2.5 text-slate-300" />
              <span className="text-xs text-slate-400">
                {group.updated_by_name} · {formatTime(group.last_updated)}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Mobile */}
      <div className="sm:hidden p-4 hover:bg-slate-50 transition-colors">
        <div className="flex items-center justify-between mb-3">
          <span className={`inline-flex items-center justify-center px-3 h-7 rounded-full text-xs font-semibold ${colorClass}`}>
            {group.group_name}
          </span>
          <div className="flex items-center gap-1.5">
            {isComplete && <CheckCircle className="w-4 h-4 text-green-500" />}
            {isSaving && <Loader2 className="w-4 h-4 animate-spin text-blue-400" />}
          </div>
        </div>

        <div className="space-y-3">
          <div>
            <label className="text-xs font-medium text-slate-500 block mb-1">组内成员</label>
            <textarea
              value={membersValue}
              onChange={handleMembersChange}
              onClick={() => !user && onLoginRequired()}
              placeholder={user ? '每行填写一位成员姓名' : '登录后填写...'}
              rows={Math.max(3, memberCount + 1)}
              className={`w-full text-sm text-slate-700 placeholder-slate-300 bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-blue-400 focus:border-blue-400 leading-6${!user ? ' cursor-pointer' : ''}`}
            />
            {membersError && (
              <p className="text-xs text-red-500 mt-1 flex items-center gap-0.5">
                <AlertTriangle className="w-3 h-3" />{membersError}
              </p>
            )}
            {hasMembers && !membersError && (
              <p className={`text-xs mt-1 ${memberCount < MEMBER_MIN ? 'text-amber-500' : 'text-slate-400'}`}>
                {memberCount} 人{memberCount < MEMBER_MIN ? `（至少 ${MEMBER_MIN} 人）` : ' ✓'}
              </p>
            )}
          </div>

          <div>
            <label className="text-xs font-medium text-slate-500 block mb-1">报名项目</label>
            <input
              type="text"
              value={projectValue}
              onChange={handleProjectChange}
              onClick={() => !user && onLoginRequired()}
              placeholder={user ? '填写报名项目名称' : '登录后填写...'}
              className={`w-full text-sm text-slate-700 placeholder-slate-300 bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-blue-400 focus:border-blue-400${!user ? ' cursor-pointer' : ''}`}
            />
          </div>

          {group.updated_by_name && (
            <div className="flex items-center gap-1">
              <User className="w-2.5 h-2.5 text-slate-300" />
              <span className="text-xs text-slate-400">
                {group.updated_by_name} 修改于 {formatTime(group.last_updated)}
              </span>
            </div>
          )}
        </div>
      </div>
    </>
  )
}
