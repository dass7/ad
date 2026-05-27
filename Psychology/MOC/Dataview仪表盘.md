---
tags: [Dashboard, Dataview]
created: 2026-05-27
---

# 心理学效应 · Dataview 仪表盘

## 全部效应（按年份排序）

```dataview
TABLE difficulty, category, scholar, year
FROM "Psychology/Effects"
SORT year ASC
```

## 按类别分组

```dataview
TABLE difficulty, scholar, year
FROM "Psychology/Effects"
WHERE category = "认知偏差"
SORT file.name ASC
```

```dataview
TABLE difficulty, scholar, year
FROM "Psychology/Effects"
WHERE category = "社会心理学"
SORT file.name ASC
```

```dataview
TABLE difficulty, scholar, year
FROM "Psychology/Effects"
WHERE category = "行为心理学"
SORT file.name ASC
```

```dataview
TABLE difficulty, scholar, year
FROM "Psychology/Effects"
WHERE category = "决策心理学"
SORT file.name ASC
```

```dataview
TABLE difficulty, scholar, year
FROM "Psychology/Effects"
WHERE category = "情绪心理学"
SORT file.name ASC
```

```dataview
TABLE difficulty, scholar, year
FROM "Psychology/Effects"
WHERE category = "人际心理学"
SORT file.name ASC
```

## 入门效应（⭐ 难度）

```dataview
TABLE category, scholar
FROM "Psychology/Effects"
WHERE difficulty = "⭐"
SORT file.name ASC
```

## 进阶效应（⭐⭐⭐ 难度）

```dataview
TABLE category, scholar
FROM "Psychology/Effects"
WHERE difficulty = "⭐⭐⭐"
SORT file.name ASC
```

## 最近修改

```dataview
TABLE file.mtime AS "修改时间", category
FROM "Psychology/Effects"
SORT file.mtime DESC
LIMIT 10
```
