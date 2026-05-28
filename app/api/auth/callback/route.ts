import { NextRequest, NextResponse } from 'next/server'

async function getAccessToken(code: string, redirectUri: string): Promise<string> {
  const params = new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: process.env.QQ_APP_ID!,
    client_secret: process.env.QQ_APP_SECRET!,
    code,
    redirect_uri: redirectUri,
    fmt: 'json',
  })
  const res = await fetch(`https://graph.qq.com/oauth2.0/token?${params.toString()}`)
  const text = await res.text()
  if (text.startsWith('{')) {
    const data = JSON.parse(text)
    if (data.error) throw new Error(data.error_description || data.error)
    return data.access_token
  }
  const parsed = new URLSearchParams(text)
  const token = parsed.get('access_token')
  if (!token) throw new Error('No access_token in response')
  return token
}

async function getOpenId(accessToken: string): Promise<string> {
  const res = await fetch(
    `https://graph.qq.com/oauth2.0/me?access_token=${accessToken}&fmt=json`
  )
  const data = await res.json()
  if (data.error) throw new Error(data.error_description || String(data.error))
  return data.openid
}

async function getUserInfo(accessToken: string, openid: string): Promise<Record<string, string>> {
  const params = new URLSearchParams({
    access_token: accessToken,
    oauth_consumer_key: process.env.QQ_APP_ID!,
    openid,
  })
  const res = await fetch(`https://graph.qq.com/user/get_user_info?${params.toString()}`)
  return res.json()
}

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const code = searchParams.get('code')
  const errorParam = searchParams.get('error')
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL!

  if (errorParam) {
    return NextResponse.redirect(`${baseUrl}/?error=${errorParam}`)
  }

  if (!code) {
    return NextResponse.redirect(`${baseUrl}/?error=no_code`)
  }

  try {
    const redirectUri = `${baseUrl}/api/auth/callback`
    const accessToken = await getAccessToken(code, redirectUri)
    const openid = await getOpenId(accessToken)
    const userInfo = await getUserInfo(accessToken, openid)

    const adminOpenId = process.env.ADMIN_QQ_OPENID || ''

    const userData = {
      openid,
      nickname: userInfo.nickname || 'QQ用户',
      avatar: userInfo.figureurl_qq_2 || userInfo.figureurl_qq_1 || '',
      isAdmin: openid === adminOpenId,
    }

    const encoded = encodeURIComponent(JSON.stringify(userData))
    return NextResponse.redirect(`${baseUrl}/?user=${encoded}`)
  } catch (error) {
    console.error('QQ OAuth callback error:', error)
    return NextResponse.redirect(`${baseUrl}/?error=auth_failed`)
  }
}
