# Obsidian 第二大脑工程（obsidianvault）

> 本目录是一个完整的 Obsidian 库：直接把整个 `obsidianvault/` 复制到本机 `D:\obsidianvault`，
> 用 Obsidian「打开文件夹作为仓库」即可使用（建议安装 Dataview 插件）。

## 目录结构

```
00-MOC ~ 10-Inbox      知识区（入口：00-MOC/知识地图.md）
01-原始素材区/完整副本   原始素材只读副本（SHA256 对账）
_system/规则层          处理规则（5 类单元、4 种关系、命名、挂靠）
_system/状态层          来源候选/原始索引/待处理/关系索引/去重候选/状态总览/待创建清单
_system/模板层          7 份标准模板
_system/脚本层          validate_vault.py 结构校验与统计
```

## 核心约定

- 内容单元只有 5 类：问题 / 概念 / 观点 / 案例 / 方案
- 显式关系只有 4 种：回应 / 解释 / 证明 / 冲突
- 引用一律 `[[文件名]]` 直链；禁止孤立笔记；一切以脚本校验为准

## 验证

```bash
python3 _system/脚本层/validate_vault.py
```

## 喂入新素材（dbskill-main 等本机内容）

云端会话无法读取本机磁盘。请将素材推送到本仓库（建议放 `incoming/` 目录，可按"纳入目录"分子目录），
流水线会从 `_system/状态层/来源候选清单.md` 开始接管。
