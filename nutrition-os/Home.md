---
title: Nutrition OS — 主页
type: home
created: 2026-05-27
updated: 2026-05-27
tags:
  - system/home
---

# 🏠 Nutrition OS 主页

> **我的目标**：两年后实习时具备真正专业能力，国家营养师四级→三级→二级考试无压力。

---

## 📍 今日快速入口

```dataview
TABLE date, energy_level
FROM "10_Journals/每日笔记"
SORT date DESC
LIMIT 5
```

---

## 🎓 导师课程（优先入口）

> 从这里开始。每一课建立底层思维，而不只是知识点。

| # | 课程 | 核心问题 | 状态 |
|---|-----|---------|------|
| 01 | [[第一课-营养学的本质]] | 为什么生命必须吃东西？ | ✅ |
| 02 | 第二课-碳水化合物的本质 | 葡萄糖只是能量吗？ | 🔲 |
| 03 | 第三课-脂肪的本质 | 脂肪为什么被冤枉了50年？ | 🔲 |

→ 全部课程：[[MOC-导师课程]]

---

## 🗺️ 知识地图导航

| 领域 | 地图 | 进度 |
|-----|------|------|
| 基础医学 | [[MOC-基础医学]] | 🔲 |
| 宏量营养素 | [[MOC-宏量营养素]] | 🔲 |
| 微量营养素 | [[MOC-微量营养素]] | 🔲 |
| 临床营养 | [[MOC-临床营养]] | 🔲 |
| 公共营养 | [[MOC-公共营养]] | 🔲 |
| 特殊人群 | [[MOC-特殊人群营养]] | 🔲 |
| 疾病营养 | [[MOC-疾病营养]] | 🔲 |
| 前沿方向 | [[MOC-前沿方向]] | 🔲 |
| 考证指南 | [[MOC-考证指南]] | 🔲 |

---

## 📅 学习进度追踪

### 当前阶段
**Phase 1：打地基（M1-M6）**
- 当前月份：Month 1
- 本月主题：系统搭建 + 生物化学入门
- 本月目标：理解三大营养素化学本质

### 考证倒计时
- 四级：~ 待定
- 三级：~ 待定
- 二级：~ 待定

---

## 🔥 今日待复习

```dataview
TABLE title, domain, review_count
FROM "03_Nutrition_Core" OR "04_Clinical" OR "05_Public_Nutrition"
WHERE next_review <= date(today)
AND type = "concept"
SORT next_review ASC
LIMIT 10
```

---

## ⚡ 近期新增笔记

```dataview
TABLE title, domain, status
WHERE type = "concept"
SORT created DESC
LIMIT 8
```

---

## 📋 系统文档
- [[Nutrition-OS-总体架构-V1]] — 完整系统设计
- [[00_System/Templates/导师课程模板]] — 导师课程笔记模板（13节+4尾）
- [[00_System/Templates/知识点模板]] — 原子知识点写作模板
- [[00_System/Templates/每日笔记模板]] — 每日记录模板
- [[00_System/Templates/周复习模板]] — 周复习报告模板
- [[00_System/Templates/案例模板]] — 临床案例笔记模板

---

*上次更新：2026-05-27*
