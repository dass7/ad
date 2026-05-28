# 创新大赛报名在线文档系统

腾讯文档风格的在线报名网页，支持 QQ 登录、实时协同编辑、自动保存。

## 功能特性

- **QQ 一键登录** — 同学点击即可授权，自动获取昵称头像
- **实时协同** — 多人同时编辑，数据秒级同步，无需刷新
- **自动保存** — 800ms 防抖后自动保存到云端
- **手机端适配** — 移动端优先设计，适合 QQ 群分享链接
- **编辑验证** — 每组限 3-7 人，超限自动提示
- **管理员面板** — 查看总览、修改记录、一键导出 Excel、清空数据
- **编辑日志** — 记录每次修改的用户、时间和内容

## 快速部署

### 1. 克隆并安装
```bash
git clone <repo-url>
cd ad
npm install
```

### 2. 配置 Supabase 数据库
1. 注册 [Supabase](https://supabase.com)，新建项目
2. 进入 **SQL Editor**，粘贴并执行 `supabase/schema.sql`
3. 在 **Database → Replication** 中勾选 `groups` 表开启实时推送
4. 在 **Settings → API** 复制 URL、anon key、service_role key

### 3. 配置 QQ OAuth
1. 访问 [QQ 互联](https://connect.qq.com)，注册开发者
2. 创建**网站应用**，回调地址填：`https://你的域名/api/auth/callback`
3. 审核通过后获取 App ID 和 App Secret

### 4. 配置环境变量
```bash
cp .env.local.example .env.local
# 编辑 .env.local 填入上述所有配置
```

### 5. 部署到 Vercel
```bash
npx vercel --prod
```
在 Vercel 控制台 **Settings → Environment Variables** 填入所有变量。

## 使用方法

| 场景 | 操作 |
|------|------|
| 分享给同学 | 将 Vercel 部署链接发到 QQ 群 |
| 同学填写 | 打开链接 → QQ 登录 → 点击对应组填写 |
| 管理员查看 | 登录 → 管理员入口 → 输入密码 |
| 导出数据 | 管理员面板 → 输入导出密钥 → 导出 Excel |
| 手机访问 | 直接在手机浏览器或 QQ 内置浏览器打开链接 |

## 技术栈

- **Next.js 14** App Router + TypeScript
- **Tailwind CSS** + lucide-react 图标
- **Supabase** — PostgreSQL 数据库 + 实时订阅 + RLS 安全策略
- **QQ OAuth 2.0** — connect.qq.com
- **Vercel** — 免费一键部署

## 项目结构

```
├── app/
│   ├── page.tsx              # 主页（报名表）
│   ├── admin/page.tsx        # 管理员面板
│   └── api/
│       ├── auth/qq/          # QQ OAuth 发起
│       ├── auth/callback/    # QQ OAuth 回调
│       └── export/           # Excel 导出
├── components/
│   ├── Header.tsx            # 顶栏（登录状态/保存状态）
│   ├── GroupRow.tsx          # 每组报名行
│   ├── LoginModal.tsx        # 登录弹窗
│   └── OnlineUsers.tsx       # 在线用户头像
├── lib/supabase.ts           # Supabase 客户端
├── types/index.ts            # TypeScript 类型
├── supabase/schema.sql       # 数据库初始化 SQL
└── .env.local.example        # 环境变量模板
```
