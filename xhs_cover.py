"""
小红书封面图生成器
尺寸: 1080×1440 (3:4)
"""

import argparse
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


# ── 配置 ──────────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1080, 1440

BG_COLOR        = (252, 248, 242)   # 奶油白
GRAIN_INTENSITY = 18                # 颗粒强度 (0~255)
TEXT_COLOR      = (50, 50, 52)      # 深灰
TITLE_Y_RATIO   = 0.30              # 标题中心线距顶部比例
MAX_CHARS_PER_LINE = 9              # 每行最多字符数（自动换行）
FONT_SIZE       = 96                # 初始字体大小
LINE_SPACING    = 1.35              # 行间距倍数

FONT_PATHS = [
    Path(__file__).parent / "fonts" / "SourceHanSansCN-Bold.otf",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
]

OUTPUT_DIR = Path(__file__).parent / "output"
# ─────────────────────────────────────────────────────────────────────────────


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(str(path), size)
        except (IOError, OSError):
            continue
    # 最后兜底：PIL 内置字体（很小，仅防崩溃）
    return ImageFont.load_default()


def add_grain(img: Image.Image, intensity: int) -> Image.Image:
    """在图像上叠加灰度高斯颗粒纹理（单通道噪声避免色偏）。"""
    arr   = np.array(img, dtype=np.int16)
    noise = np.random.normal(0, intensity, (arr.shape[0], arr.shape[1])).astype(np.int16)
    arr  += noise[:, :, np.newaxis]          # 同一噪声值广播到 RGB 三通道
    arr   = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def wrap_text(text: str, max_chars: int) -> list[str]:
    """按标点或最大字符数自动换行，保留原有换行符。"""
    lines = []
    for paragraph in text.split("\n"):
        if len(paragraph) <= max_chars:
            lines.append(paragraph)
            continue
        # 在标点前断行（中文逗号、句号、感叹号、问号）
        buf = ""
        for ch in paragraph:
            buf += ch
            if len(buf) >= max_chars or ch in "，。！？、；：":
                lines.append(buf)
                buf = ""
        if buf:
            lines.append(buf)
    return lines


def measure_block(lines: list[str], font: ImageFont.FreeTypeFont, spacing: float):
    """返回文字块的 (width, height)。"""
    dummy = Image.new("RGB", (1, 1))
    draw  = ImageDraw.Draw(dummy)
    line_h = font.size * spacing
    total_h = line_h * len(lines)
    max_w   = max(draw.textlength(ln, font=font) for ln in lines)
    return max_w, total_h


def render_title(img: Image.Image, text: str) -> Image.Image:
    font  = load_font(FONT_SIZE)
    lines = wrap_text(text, MAX_CHARS_PER_LINE)
    block_w, block_h = measure_block(lines, font, LINE_SPACING)

    # 若文字块超出画布宽度，等比缩小字号
    if block_w > WIDTH * 0.85:
        scale = (WIDTH * 0.85) / block_w
        font  = load_font(int(FONT_SIZE * scale))
        block_w, block_h = measure_block(lines, font, LINE_SPACING)

    line_h  = font.size * LINE_SPACING
    block_y = HEIGHT * TITLE_Y_RATIO - block_h / 2   # 垂直居中于目标位置
    draw    = ImageDraw.Draw(img)

    for i, line in enumerate(lines):
        lw, _ = draw.textlength(line, font=font), 0
        lw     = draw.textlength(line, font=font)
        x      = (WIDTH - lw) / 2
        y      = block_y + i * line_h
        draw.text((x, y), line, font=font, fill=TEXT_COLOR)

    return img


def generate_cover(title: str, output_path: str | None = None) -> Path:
    np.random.seed(42)

    # 1. 背景
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)

    # 2. 颗粒纹理
    img = add_grain(img, GRAIN_INTENSITY)

    # 3. 标题文字
    img = render_title(img, title)

    # 4. 保存
    OUTPUT_DIR.mkdir(exist_ok=True)
    if output_path is None:
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in title[:20])
        output_path = OUTPUT_DIR / f"cover_{safe}.png"
    img.save(output_path, "PNG", optimize=True)
    return Path(output_path)


def main():
    parser = argparse.ArgumentParser(description="生成小红书封面图")
    parser.add_argument("title", nargs="?",
                        default="不是你管不住嘴，是这俩字在骗你",
                        help="封面标题文字")
    parser.add_argument("-o", "--output", default=None, help="输出路径（可选）")
    args = parser.parse_args()

    out = generate_cover(args.title, args.output)
    print(f"已生成: {out}")


if __name__ == "__main__":
    main()
