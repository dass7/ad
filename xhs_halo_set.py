#!/usr/bin/env python3
"""
小红书套图生成器 — 健康光环效应 (7张)
配色：薄荷奶冻  尺寸：1080×1440
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ── 尺寸 ─────────────────────────────────────────────────────────────────────
W, H = 1080, 1440
FONT_PATH = Path(__file__).parent / "fonts" / "SourceHanSansCN-Bold.otf"
OUT = Path(__file__).parent / "output" / "halo_set"

# ── 配色 ─────────────────────────────────────────────────────────────────────
BG_CREAM = (247, 250, 247)   # 奶白  背景 A
BG_MINT  = (230, 242, 237)   # 浅薄荷  背景 B
C_MAIN   = ( 46,  74,  66)   # 深灰绿  主文字
C_WARM   = (201, 123,  90)   # 暖陶土橙  情绪强调
C_MINT   = ( 91, 160, 138)   # 薄荷绿  概念强调
C_LIGHT  = (155, 185, 172)   # 浅灰绿  辅助/次要
C_RULE   = (195, 220, 210)   # 装饰线

GRAIN = 13

# ── 字号 ─────────────────────────────────────────────────────────────────────
XL, L, M, S, XS = 84, 68, 52, 34, 24

# ── 字体缓存 ─────────────────────────────────────────────────────────────────
_fc: dict[int, ImageFont.FreeTypeFont] = {}

def fnt(size: int) -> ImageFont.FreeTypeFont:
    if size not in _fc:
        _fc[size] = ImageFont.truetype(str(FONT_PATH), size)
    return _fc[size]

# ── 工具 ─────────────────────────────────────────────────────────────────────
_ref = ImageDraw.Draw(Image.new("RGB", (1, 1)))

def tw(text: str, size: int) -> float:
    return _ref.textlength(text, font=fnt(size))

Segs = list[tuple[str, tuple]]

def draw_segs(draw: ImageDraw.ImageDraw, segs: Segs, size: int, cx: float, y: float):
    total = sum(tw(t, size) for t, _ in segs)
    x = cx - total / 2
    for text, color in segs:
        draw.text((x, y), text, font=fnt(size), fill=color)
        x += tw(text, size)

def block_h(lines: list[dict]) -> float:
    """从第一行顶部到最后一行底部的高度。"""
    h = 0.0
    for i, ln in enumerate(lines):
        lh = ln['size'] * ln.get('lh', 1.48)
        gap = ln.get('gap', 0)
        if i < len(lines) - 1:
            h += lh + gap
        else:
            h += ln['size']   # 最后一行只算字高，不算行距和gap
    return h

def render_block(draw: ImageDraw.ImageDraw, lines: list[dict],
                 top_y: float, cx: float = W / 2):
    y = top_y
    for ln in lines:
        draw_segs(draw, ln['segs'], ln['size'], cx, y)
        y += ln['size'] * ln.get('lh', 1.48) + ln.get('gap', 0)

def center_block(draw: ImageDraw.ImageDraw, lines: list[dict],
                 cy: float, cx: float = W / 2):
    render_block(draw, lines, cy - block_h(lines) / 2, cx)

# ── 背景 ─────────────────────────────────────────────────────────────────────
def make_bg(color: tuple) -> Image.Image:
    np.random.seed(7)
    img = Image.new("RGB", (W, H), color)
    arr = np.array(img, dtype=np.int16)
    noise = np.random.normal(0, GRAIN, (H, W)).astype(np.int16)
    arr += noise[:, :, np.newaxis]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

# ── 装饰元素 ─────────────────────────────────────────────────────────────────
def top_rule(draw: ImageDraw.ImageDraw, y: int = 92, width: int = 50):
    draw.line([(W // 2 - width, y), (W // 2 + width, y)], fill=C_RULE, width=3)

def slide_num(draw: ImageDraw.ImageDraw, n: int, total: int = 7):
    txt = f"{n:02d}  /  {total:02d}"
    f = fnt(XS)
    x = W // 2 - tw(txt, XS) / 2
    draw.text((x, H - 76), txt, font=f, fill=C_LIGHT)

def h_rule(draw: ImageDraw.ImageDraw, y: int, width: int = 80):
    draw.line([(W // 2 - width, y), (W // 2 + width, y)], fill=C_RULE, width=2)

# ── 7 张幻灯片 ────────────────────────────────────────────────────────────────
def slide_01() -> Image.Image:          # 封面
    img = make_bg(BG_CREAM)
    d   = ImageDraw.Draw(img)
    top_rule(d)

    lines = [
        {'segs': [("不是你管不住嘴", C_MAIN)],                         'size': L, 'lh': 1.3},
        {'segs': [("是", C_MAIN), ("这俩字", C_WARM), ("在骗你", C_MAIN)], 'size': L},
    ]
    center_block(d, lines, cy=H * 0.44)

    bh   = block_h(lines)
    ry   = int(H * 0.44 + bh / 2 + 52)
    h_rule(d, ry, 72)

    sub  = "关于食物标签的一个心理学事实"
    d.text((W // 2 - tw(sub, S) / 2, ry + 28), sub, font=fnt(S), fill=C_LIGHT)
    return img


def slide_02() -> Image.Image:          # 场景代入
    img = make_bg(BG_MINT)
    d   = ImageDraw.Draw(img)
    top_rule(d)
    slide_num(d, 2)

    lines = [
        {'segs': [("买了一盒", C_MAIN), ("“低脂”", C_WARM), ("酸奶", C_MAIN)],  'size': M, 'gap': 6},
        {'segs': [("想着这个健康，吃一点没事", C_MAIN)],                          'size': M, 'gap': 48},
        {'segs': [("回过神来——", C_MAIN)],                                        'size': M, 'gap': 6},
        {'segs': [("一整盒，已经见底了", C_MAIN)],                                'size': M, 'gap': 48},
        {'segs': [("心里还有点", C_MAIN), ("踏实", C_WARM)],                      'size': M},
    ]
    center_block(d, lines, cy=H * 0.46)
    return img


def slide_03() -> Image.Image:          # 概念命名
    img = make_bg(BG_CREAM)
    d   = ImageDraw.Draw(img)
    top_rule(d)
    slide_num(d, 3)

    lines = [
        {'segs': [("这件事，有个名字", C_LIGHT)],    'size': S,  'gap': 68},
        {'segs': [("健康光环效应", C_MINT)],          'size': XL, 'gap': 36},
        {'segs': [("Health Halo Effect", C_LIGHT)],  'size': S},
    ]
    center_block(d, lines, cy=H * 0.45)
    return img


def slide_04() -> Image.Image:          # 机制拆解
    img = make_bg(BG_MINT)
    d   = ImageDraw.Draw(img)
    top_rule(d)
    slide_num(d, 4)

    lines = [
        {'segs': [("那根", C_MAIN), ("「该停了」", C_WARM), ("的弦", C_MAIN)],  'size': M, 'gap': 6},
        {'segs': [("平时，它是绷着的", C_MAIN)],                                 'size': M, 'gap': 52},
        {'segs': [("可只要食物上印着“健康”", C_MAIN)],                            'size': M, 'gap': 6},
        {'segs': [("大脑就收到", C_MAIN), ("一张通行证", C_MINT)],               'size': M, 'gap': 6},
        {'segs': [("悄悄把那根弦松开了", C_MAIN)],                               'size': M},
    ]
    center_block(d, lines, cy=H * 0.46)
    return img


def slide_05() -> Image.Image:          # 金句
    img = make_bg(BG_CREAM)
    d   = ImageDraw.Draw(img)
    top_rule(d)
    slide_num(d, 5)

    lines = [
        {'segs': [("你不是输给了", C_MAIN), ("食物本身", C_MINT)], 'size': L, 'gap': 64},
        {'segs': [("你是输给了", C_MAIN),   ("那两个字", C_WARM)], 'size': L},
    ]
    center_block(d, lines, cy=H * 0.45)

    bh = block_h(lines)
    h_rule(d, int(H * 0.45 + bh / 2 + 60), 48)
    return img


def slide_06() -> Image.Image:          # 行动建议
    img = make_bg(BG_MINT)
    d   = ImageDraw.Draw(img)
    top_rule(d)
    slide_num(d, 6)

    lines = [
        {'segs': [("下次看到“轻食”“低卡”", C_MAIN)],                             'size': M, 'gap': 6},
        {'segs': [("不用紧张，也不用克制", C_MAIN)],                              'size': M, 'gap': 56},
        {'segs': [("只要心里清楚——", C_LIGHT)],                                   'size': S, 'gap': 16},
        {'segs': [("刹车", C_WARM), ("，被人悄悄松了一下", C_MAIN)],              'size': M, 'gap': 56},
        {'segs': [("光是知道这件事", C_MAIN)],                                    'size': S, 'gap': 8},
        {'segs': [("那根弦，就回到你手里了", C_MAIN)],                            'size': S},
    ]
    center_block(d, lines, cy=H * 0.47)
    return img


def slide_07() -> Image.Image:          # 互动结尾
    img = make_bg(BG_CREAM)
    d   = ImageDraw.Draw(img)
    top_rule(d)
    slide_num(d, 7)

    lines = [
        {'segs': [("你有没有哪个食物", C_MAIN)],                                        'size': M, 'gap': 6},
        {'segs': [("就因为它", C_MAIN), ("看起来很健康", C_MINT)],                      'size': M, 'gap': 6},
        {'segs': [("结果默默吃超了的？", C_MAIN)],                                      'size': M, 'gap': 64},
        {'segs': [("评论区交出来  ↓", C_WARM)],                                         'size': S, 'gap': 72},
        {'segs': [("#健康光环效应  #行为心理学  #食物心理学", C_LIGHT)],                 'size': XS, 'gap': 8},
        {'segs': [("#原来如此  #吃饭这件小事  #自我觉察", C_LIGHT)],                    'size': XS},
    ]
    center_block(d, lines, cy=H * 0.46)
    return img


# ── 主程序 ────────────────────────────────────────────────────────────────────
SLIDES = [
    (slide_01, "01_cover.png"),
    (slide_02, "02_scene.png"),
    (slide_03, "03_concept.png"),
    (slide_04, "04_mechanism.png"),
    (slide_05, "05_quote.png"),
    (slide_06, "06_action.png"),
    (slide_07, "07_interaction.png"),
]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    paths = []
    for fn, name in SLIDES:
        img  = fn()
        path = OUT / name
        img.save(path, "PNG")
        print(f"  {name}")
        paths.append(path)
    print(f"\n全部完成 → {OUT}")
    return paths

if __name__ == "__main__":
    main()
