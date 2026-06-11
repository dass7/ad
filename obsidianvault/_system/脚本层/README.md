# 脚本层

| 脚本 | 用途 |
|---|---|
| `validate_vault.py` | 全库结构校验 + 可核验统计（单元数/MOC 数/装配稿数/关系数/孤立检测/待创建链接） |

运行方式：

```bash
python3 obsidianvault/_system/脚本层/validate_vault.py
```

退出码 0 = 结构稳定，允许批量推进；非 0 = 必须先修复再继续处理新来源。
每次新增/修改正文笔记后必须重跑。
