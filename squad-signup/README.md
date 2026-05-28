# 组队报名表

一个简洁的在线组队报名表，支持多人实时协同编辑，手机优先设计。

---

## 功能清单

- 9 个固定组，支持填写成员名单和报名项目
- 多人实时同步（WebSocket）
- 自动防抖保存（停止输入 0.9s 后自动存储）
- 显示最后编辑人 + 时间
- 远端修改高亮提示
- 分享按钮 + 二维码生成（扫码即填写）
- 手机端全适配
- 纯静态前端，零服务器运维

---

## 快速部署（5 分钟）

### 第一步：创建 Supabase 项目（免费）

1. 访问 [supabase.com](https://supabase.com) → 注册登录
2. 点击 **New Project**，填写项目名（如 `squad-signup`），设置数据库密码
3. 等待约 1 分钟，项目启动完成

### 第二步：初始化数据库

1. 进入 Supabase 控制台 → 左侧菜单 **SQL Editor**
2. 新建查询，粘贴 `supabase/schema.sql` 全部内容
3. 点击 **Run** 执行

### 第三步：获取配置信息

在 Supabase 控制台：
- 左侧菜单 → **Project Settings** → **API**
- 复制 **Project URL**（形如 `https://xxxxx.supabase.co`）
- 复制 **anon public** Key（很长的字符串）

### 第四步：填入 index.html

打开 `index.html`，找到顶部这两行，替换为你的信息：

```js
const SUPABASE_URL      = 'https://YOUR_PROJECT_ID.supabase.co';
const SUPABASE_ANON_KEY = 'YOUR_ANON_KEY';
```

### 第五步：部署上线

**方式 A：Vercel（推荐，免费）**

```bash
# 安装 Vercel CLI
npm i -g vercel

# 在 squad-signup 目录执行
vercel
```

按提示操作，完成后会得到形如 `https://squad-signup-xxx.vercel.app` 的链接。

**方式 B：GitHub Pages（免费）**

1. 将 `squad-signup` 目录推送到 GitHub 仓库
2. 仓库 Settings → Pages → Source 选 `main` 分支的根目录
3. 保存后约 1 分钟，自动生成 `https://你的用户名.github.io/仓库名`

**方式 C：Netlify（免费）**

1. 访问 [netlify.com](https://netlify.com) → 拖拽 `squad-signup` 文件夹到页面
2. 立即获得链接，无需任何配置

---

## 分享给同学

部署完成后：

1. 复制部署链接
2. 发到群里，或点页面右上角 **分享 ↗** 按钮
3. 页面自动生成二维码，截图发给同学 → 扫码即填写

支持微信/QQ 内置浏览器直接打开，无需安装任何 App。

---

## 接入 QQ 登录（可选高级功能）

> 默认使用昵称模式（输入名字即用），已满足大多数场景。
> 如需强制 QQ 身份验证，参考以下步骤。

### QQ OAuth 接入步骤

1. 访问 [connect.qq.com](https://connect.qq.com) → 注册开发者账号
2. 创建应用（网站应用），填写回调域名（你的部署地址）
3. 审核通过后，获取 `AppID` 和 `AppKey`
4. 在页面添加 QQ 登录按钮：

```html
<!-- 在 <head> 中引入 SDK -->
<script src="https://connect.qq.com/qc_jssdk.js"
        data-appid="你的AppID"
        data-redirecturi="https://你的域名/callback"
        data-scope="get_user_info"
        data-cookielogin="true">
</script>

<!-- 在 body 中放登录按钮 -->
<div id="qqLoginBtn"></div>
<script>
  QC.Login({ btnId: 'qqLoginBtn' });
  QC.Login.signOut(); // 用于登出

  // 获取用户信息
  if (QC.Login.check()) {
    QC.api('get_user_info').success(res => {
      const nickname = res.data.nickname;
      const avatar   = res.data.figureurl_qq_1;
      // 用 nickname 替代手动输入的昵称
    });
  }
</script>
```

5. 将获取到的 `nickname` 替换 `doLogin()` 中手动输入的名字即可

> 注意：QQ 登录审核较慢（3-5 个工作日），建议先用昵称模式发给同学填写，后期再升级。

---

## 目录结构

```
squad-signup/
├── index.html          # 全部前端代码（HTML + CSS + JS）
├── supabase/
│   └── schema.sql      # 数据库初始化 SQL
└── README.md           # 本文档
```

---

## 常见问题

**Q：多人同时编辑同一格，会不会冲突？**  
A：最后保存的内容获胜（Last Write Wins），同时右下角会提示"谁刚刚编辑了第N组"。建议各组同学只填自己那一行。

**Q：数据会丢失吗？**  
A：Supabase 免费套餐提供 500MB 数据库存储，本项目数据量极小。数据保存在云端，关闭页面不丢失。

**Q：免费额度够用吗？**  
A：Supabase 免费版：500MB 数据库 + 2GB 文件 + 50,000 月活用户，完全够用。Vercel 免费版：无限静态部署，完全够用。

**Q：能加密码保护吗？**  
A：简单方法：在 `doLogin()` 函数里加一行 `if (password !== '班级密码') { return; }` 即可实现简单密码保护。
