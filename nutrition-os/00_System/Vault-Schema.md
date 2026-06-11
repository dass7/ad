---
title: Vault-Schema
aliases:
  - Frontmatter规范
  - 元数据规范
type: system
up: "[[Home]]"
status: mature
created: 2026-06-11
updated: 2026-06-11
tags:
  - system/schema
---

# 📐 Vault-Schema — Frontmatter 字段规范

> 本文件是全库 YAML frontmatter 的**唯一权威定义**。Dataview 查询和 AI 工具都依赖这些字段，写法不统一查询就会漏数据。

## 必填字段（所有笔记）

| 字段 | 类型 | 取值 | 说明 |
|------|------|------|------|
| `title` | 文本 | 与文件名一致 | |
| `type` | 枚举 | `home` `moc` `concept` `mechanism` `clinical` `case` `daily` `review` `exam` `template` `system` | **全小写** |
| `up` | 链接 | `"[[所属MOC]]"` | 图谱层级骨架，除 Home 外必填 |
| `created` / `updated` | 日期 | `YYYY-MM-DD` | |
| `tags` | 列表 | 见架构文档第三节标签体系 | |

## 推荐字段

| 字段 | 类型 | 取值 | 说明 |
|------|------|------|------|
| `aliases` | 列表 | 同义词/缩写/英文名 | 供搜索与 AI 检索 |
| `status` | 枚举 | `seed`（Inbox原始想法）→ `draft` → `developing` → `mature` | **英文枚举，禁止中文自由文本** |
| `domain` | 列表 | `biochemistry` `physiology` `macronutrient` `micronutrient` `clinical` `public` `disease` `special_group` `advanced` `food_safety` `interdisciplinary` | 多值 = 跨学科，≥2 值登记到 [[MOC-跨学科连接]] |

## concept 类型专属字段

| 字段 | 取值 | 说明 |
|------|------|------|
| `importance` | `★` ~ `★★★★★` | 学习优先级 |
| `exam_level` | `[level4, level3, level2]` | 考级覆盖 |
| `exam_freq` | `高频` `中` `低` | 考试频率 |
| `review_count` / `next_review` | 数字 / 日期 | 间隔复习（1→3→7→14→30→90天） |
| `source` | 文本 | 知识来源（教材/指南/论文） |
| `related` | 链接列表 | 关联笔记 |

## 校验口诀

```
type 小写、status 英文、up 必填、日期横杠
```

---
*相关：[[Nutrition-OS-总体架构-V1#🏷️ 三、标签体系]] | [[知识点模板]] | 返回：[[Home]]*
