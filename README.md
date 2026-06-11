# Nutrition OS — 营养学知识库

> AI First · Zettelkasten · MOC 导航 · 跨学科研究型 Obsidian 知识库

## 这是什么

一个面向"两年成为专业营养师（四级→三级→二级）"目标的 Obsidian 知识操作系统。

**使用方式**：用 Obsidian 打开 `nutrition-os/` 目录作为 Vault 根目录（Dataview 查询路径以此为基准）。

## 入口

| 入口 | 路径 | 用途 |
|------|------|------|
| 🏠 每日主页 | `00_System/Home.md` | 日常起点 |
| 🗺️ 知识总地图 | `01_Maps/MOC-营养学总览.md` | 导航到任何知识点 |
| 🕸️ 图谱入口 | `00_System/图谱入口.md` | 知识图谱使用说明 |
| 📐 系统架构 | `00_System/Nutrition-OS-总体架构-V1.md` | 完整系统设计书 |
| 🤖 AI 规范 | `CLAUDE.md` | AI 工具进库必读规则 |

## 目录结构

```
nutrition-os/
├── 00_System/    系统中心（主页/架构/模板/Schema）
├── 01_Maps/      MOC 地图层（10 张导航地图）
├── 02_Foundation/ ~ 07_Advanced/   六层知识内容区
├── 08_Cases/     案例库
├── 09_Exam/      考证专区
├── 10_Journals/  每日笔记 / 周复习
└── 11_Inbox/     收件箱（未分类内容入口）
```

## 核心约定

- **零删除原则**：内容只增不删，过时内容用 callout 标注并指向新版本
- **原子化笔记**：一张卡片只回答一个问题（200-800字）
- **frontmatter 规范**：见 `00_System/Vault-Schema.md`
- **每篇笔记必有 `up` 链接**：保证图谱连通
