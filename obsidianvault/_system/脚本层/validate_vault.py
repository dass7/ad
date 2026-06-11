#!/usr/bin/env python3
"""Nutrition/Knowledge vault validator & stats reporter.

用法：在仓库根或 vault 根运行
    python3 obsidianvault/_system/脚本层/validate_vault.py

校验项（违反任意一条退出码非 0）：
  1. 正文区每个 .md 含完整 frontmatter（title/type/domain/source/author/status/created/updated/tags）
  2. type 合法：内容单元 ∈ {question, concept, claim, case, solution}；
     结构件 ∈ {moc, index, domain, project, book, course, home, draft, inbox}
  3. 无孤立文件：每个文件被至少一个其他文件 [[引用]]
  4. 每个文件至少 1 条出链
  5. 每个内容单元被至少一个 moc/index 类型页面引用（挂靠）
  6. 内容单元含 上位概念≥3 / 下位概念≥3 / 关联概念≥2
  7. 显式关系行格式合法，且关系目标笔记存在
非致命报告项：未解析链接（生长边界）→ 待创建概念清单
"""
import os
import re
import sys
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.abspath(os.path.join(HERE, "..", ".."))
EXCLUDE_DIRS = {"_system", "01-原始素材区", ".obsidian", ".git"}
UNIT_TYPES = {"question", "concept", "claim", "case", "solution"}
STRUCT_TYPES = {"moc", "index", "domain", "project", "book", "course", "home", "draft", "inbox"}
REQUIRED_KEYS = ["title", "type", "domain", "source", "author", "status", "created", "updated", "tags"]
REL_KINDS = ("回应", "解释", "证明", "冲突")
REL_RE = re.compile(r"^- (回应|解释|证明|冲突) → \[\[([^\]|#]+)\]\]")
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")


def collect_files():
    files = {}
    for root, dirs, names in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for n in names:
            if n.endswith(".md"):
                p = os.path.join(root, n)
                if os.path.dirname(p) == VAULT and n == "README.md":
                    continue  # 库根 README 是工程说明，不参与图谱
                files[n[:-3]] = p
    return files


def parse(path):
    text = open(path, encoding="utf-8").read()
    fm = {}
    body = text
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            for line in text[4:end].splitlines():
                m = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
                if m:
                    fm[m.group(1)] = m.group(2).strip().strip('"')
            body = text[end + 5:]
    return fm, body, text


def section_links(body, header):
    m = re.search(rf"^### {header}\n(.*?)(?=^### |^---|^## |\Z)", body, re.M | re.S)
    return LINK_RE.findall(m.group(1)) if m else None


def main():
    files = collect_files()
    errors, warnings = [], []
    meta, links_out, relations = {}, {}, []

    for name, path in files.items():
        fm, body, _ = parse(path)
        rel = os.path.relpath(path, VAULT)
        meta[name] = fm
        missing = [k for k in REQUIRED_KEYS if k not in fm]
        if missing:
            errors.append(f"[frontmatter] {rel} 缺少键: {missing}")
        t = fm.get("type", "")
        if t not in UNIT_TYPES | STRUCT_TYPES:
            errors.append(f"[type] {rel} 非法 type: {t!r}")
        out = [l.strip() for l in LINK_RE.findall(body)]
        links_out[name] = out
        if not out:
            errors.append(f"[outlink] {rel} 没有任何出链")
        for line in body.splitlines():
            m = REL_RE.match(line.strip())
            if m:
                relations.append((name, m.group(1), m.group(2).strip()))
        if t in UNIT_TYPES:
            for header, n_min in (("上位概念", 3), ("下位概念", 3), ("关联概念", 2)):
                got = section_links(body, header)
                if got is None:
                    errors.append(f"[结构] {rel} 缺少小节: {header}")
                elif len(got) < n_min:
                    errors.append(f"[结构] {rel} {header} 链接数 {len(got)} < {n_min}")

    # 反向引用 / 孤立检测
    referenced = collections.defaultdict(set)
    for src, outs in links_out.items():
        for o in outs:
            referenced[o].add(src)
    unresolved = collections.Counter()
    for name in files:
        refs = referenced.get(name, set())
        if not refs:
            errors.append(f"[孤立] {name}.md 未被任何文件引用")
    for src, outs in links_out.items():
        for o in outs:
            if o not in files:
                unresolved[o] += 1

    # 挂靠检测：单元须被 moc/index 页引用
    nav_pages = {n for n, fm in meta.items() if fm.get("type") in ("moc", "index")}
    for name, fm in meta.items():
        if fm.get("type") in UNIT_TYPES:
            if not referenced.get(name, set()) & nav_pages:
                errors.append(f"[挂靠] {name}.md 未被任何 MOC/索引页引用")

    # 关系目标必须存在
    for src, kind, tgt in relations:
        if tgt not in files:
            errors.append(f"[关系] {src}.md: {kind} → [[{tgt}]] 目标不存在")

    units = {n: fm for n, fm in meta.items() if fm.get("type") in UNIT_TYPES}
    by_type = collections.Counter(fm["type"] for fm in units.values())
    mocs = [n for n, fm in meta.items() if fm.get("type") == "moc"]
    drafts = [n for n, fm in meta.items() if fm.get("type") == "draft"]
    rel_by_kind = collections.Counter(k for _, k, _ in relations)

    print("=" * 60)
    print("VAULT 验证报告")
    print("=" * 60)
    print(f"正文区文件总数        : {len(files)}")
    print(f"内容单元总数          : {len(units)}")
    for t in ("concept", "claim", "case", "solution", "question"):
        print(f"  - {t:<10}        : {by_type.get(t, 0)}")
    print(f"  - 其中思维模型      : {sum(1 for fm in units.values() if fm.get('subtype') == 'mental-model')}")
    print(f"主题地图（MOC）       : {len(mocs)}  -> {', '.join(sorted(mocs))}")
    print(f"选题装配稿            : {len(drafts)}  -> {', '.join(sorted(drafts))}")
    print(f"显式关系总数          : {len(relations)}")
    for k in REL_KINDS:
        print(f"  - {k}              : {rel_by_kind.get(k, 0)}")
    print(f"未解析链接（待创建）  : {len(unresolved)} 种 / {sum(unresolved.values())} 处")
    for tgt, c in sorted(unresolved.items(), key=lambda x: -x[1]):
        print(f"    [[{tgt}]] x{c}")
    print("-" * 60)
    if warnings:
        print(f"警告 {len(warnings)} 条：")
        for w in warnings:
            print("  ⚠ " + w)
    if errors:
        print(f"错误 {len(errors)} 条：")
        for e in errors:
            print("  ✗ " + e)
        print("结论：未通过")
        return 1
    print("错误 0 条。结论：通过 ✅（结构稳定，可批量推进）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
