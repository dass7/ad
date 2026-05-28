const QQ_APP_ID = process.env.QQ_APP_ID!
const QQ_APP_SECRET = process.env.QQ_APP_SECRET!
const REDIRECT_URI = process.env.NEXT_PUBLIC_BASE_URL + '/api/auth/callback'

export function getQQAuthUrl(state: string): string {
  const params = new URLSearchParams({
    response_type: 'code',
    client_id: QQ_APP_ID,
    redirect_uri: REDIRECT_URI,
    state,
    scope: 'get_user_info',
  })
  return `https://graph.qq.com/oauth2.0/authorize?${params.toString()}`
}

export async function getQQAccessToken(code: string): Promise<string> {
  const params = new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: QQ_APP_ID,
    client_secret: QQ_APP_SECRET,
    code,
    redirect_uri: REDIRECT_URI,
    fmt: 'json',
  })
  const res = await fetch(`https://graph.qq.com/oauth2.0/token?${params.toString()}`)
  const text = await res.text()
  // Response might be: access_token=xxx&expires_in=xxx or JSON
  if (text.startsWith('{')) {
    const data = JSON.parse(text)
    return data.access_token
  }
  const parsed = new URLSearchParams(text)
  return parsed.get('access_token')!
}

export async function getQQOpenId(accessToken: string): Promise<string> {
  const res = await fetch(`https://graph.qq.com/oauth2.0/me?access_token=${accessToken}&fmt=json`)
  const data = await res.json()
  return data.openid
}

export async function getQQUserInfo(accessToken: string, openid: string): Promise<any> {
  const params = new URLSearchParams({
    access_token: accessToken,
    oauth_consumer_key: QQ_APP_ID,
    openid,
  })
  const res = await fetch(`https://graph.qq.com/user/get_user_info?${params.toString()}`)
  const data = await res.json()
  return data
}
