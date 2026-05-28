import { NextResponse } from 'next/server'

export async function GET() {
  const QQ_APP_ID = process.env.QQ_APP_ID
  const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL

  if (!QQ_APP_ID || !BASE_URL) {
    return NextResponse.json(
      { error: 'QQ OAuth not configured. Please set QQ_APP_ID and NEXT_PUBLIC_BASE_URL.' },
      { status: 500 }
    )
  }

  const redirectUri = `${BASE_URL}/api/auth/callback`
  const state = Math.random().toString(36).substring(2, 15)

  const params = new URLSearchParams({
    response_type: 'code',
    client_id: QQ_APP_ID,
    redirect_uri: redirectUri,
    state,
    scope: 'get_user_info',
  })

  const authUrl = `https://graph.qq.com/oauth2.0/authorize?${params.toString()}`
  return NextResponse.redirect(authUrl)
}
