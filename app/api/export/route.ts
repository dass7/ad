import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'
import * as XLSX from 'xlsx'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const adminKey = searchParams.get('key')

  if (adminKey !== process.env.ADMIN_EXPORT_KEY) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  )

  const { data: groups } = await supabase
    .from('groups')
    .select('*')
    .order('group_number')

  if (!groups) return NextResponse.json({ error: 'No data' }, { status: 500 })

  const rows = groups.map(g => ({
    '组数': g.group_name,
    '组内成员': g.members,
    '报名项目': g.project_name,
    '最后修改人': g.updated_by_name,
    '最后修改时间': g.last_updated ? new Date(g.last_updated).toLocaleString('zh-CN') : '',
  }))

  const wb = XLSX.utils.book_new()
  const ws = XLSX.utils.json_to_sheet(rows)

  ws['!cols'] = [
    { wch: 10 }, { wch: 30 }, { wch: 25 }, { wch: 15 }, { wch: 20 },
  ]

  XLSX.utils.book_append_sheet(wb, ws, '报名表')
  const buf = XLSX.write(wb, { type: 'buffer', bookType: 'xlsx' })

  return new NextResponse(buf, {
    headers: {
      'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'Content-Disposition': 'attachment; filename="创新大赛报名表.xlsx"',
    },
  })
}
