# CLAUDE.md — AI 工具进库必读

这是一个 **AI First · Zettelkasten · MOC 导航 · 跨学科研究型** 的 Obsidian 营养学知识库（Nutrition OS）。任何 AI 助手在本仓库工作时遵守以下规则。

## 硬性原则

1. **零删除**：不删除任何笔记或内容。过时内容用 `> [!warning]` callout 标注并链接到新版本。
2. **保留历史**：移动/重命名一律 `git mv`。
3. **单一事实来源**：MOC 清单的权威版本是 `01_Maps/MOC-营养学总览.md`；模板的权威版本在 `00_System/Templates/`；架构文档 `00_System/Nutrition-OS-总体架构-V1.md` 中的对应章节是设计稿快照，不要直接修改快照来更新系统。

## Vault 结构（根目录 = `nutrition-os/`）

| 目录 | 用途 |
|------|------|
| `00_System/` | 主页 Home.md、架构文档、Vault-Schema、图谱入口、Templates/ |
| `01_Maps/` | 全部 MOC（`MOC-*.md`），1 张总览 + 9 张领域图 + 1 张跨学科横向图 |
| `02_Foundation/` ~ `07_Advanced/` | 知识内容区（基础医学→核心营养→临床→公共→特殊人群→前沿） |
| `08_Cases/` | 案例（`Case-[疾病]-[编号].md`） |
| `09_Exam/` | 考证（`Exam-L[级别]-*.md` / `Wrong-[日期]-*.md`） |
| `10_Journals/` | 每日笔记 `YYYY-MM-DD.md` / 周复习 `Week-YYYY-WXX.md` |
| `11_Inbox/` | 未分类内容入口，每周清空归位 |

## 写新笔记时

1. 从 `00_System/Templates/知识点模板.md` 起步，frontmatter 按 `00_System/Vault-Schema.md` 填写
2. **原子化**：一篇只回答一个问题，200-800 字；超过 1500 字必须拆分
3. **必填 `up` 字段**：链接到所属 MOC（保证图谱连通）
4. **至少 5 个双链**：向上链 MOC、向下链子概念、横向链同级、链先修、链应用
5. 文件名 = 用户搜索时会输入的词，格式 `[核心词]-[修饰词].md`，统一中文，禁止数字后缀
6. `domain` 含 2 个以上领域的笔记，登记到 `[[MOC-跨学科连接]]`
7. 新建笔记后，到对应 MOC 把 🔲 占位条目替换为真实链接

## Frontmatter 速查（完整版见 Vault-Schema）

```yaml
type: home|moc|concept|mechanism|clinical|case|daily|review|exam|template|system
status: seed|draft|developing|mature
up: "[[所属MOC]]"          # 必填
domain: [macronutrient, clinical, ...]   # 多值=跨学科
aliases: [同义词, 缩写]     # 利于 AI 与搜索
```

## 领域知识注意

本库是营养学专业库（中国国家营养师考证语境）。引用摄入量、膳食指南等数据以《中国居民膳食营养素参考摄入量（DRIs）》和《中国居民膳食指南2022》为准，不确定的数值标注来源或留待用户核实，不要编造。
