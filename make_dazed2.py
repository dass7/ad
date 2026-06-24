from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math

src = '/root/.claude/uploads/3d3fb752-d065-5468-83f5-36e690384e27/69d15c0e-49225.png'
img = Image.open(src).convert('RGBA')
W, H = img.size  # 1194 x 1194
print(f"Image size: {W}x{H}")

overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(overlay)

# Scale factor vs original 300px concept
S = W / 300  # ≈ 3.98

def s(v):
    return int(v * S)

# ── 1. Blush on cheeks ─────────────────────────────────────────────────
# In 300px space: left cheek (90,195), right cheek (210,195)
for cx, cy in [(s(88), s(197)), (s(212), s(197))]:
    for r, alpha in [(s(32), 55), (s(22), 80), (s(12), 105)]:
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(255, 90, 110, alpha))

# ── 2. Swirly / vacant eye overlays (@ style dizzy eyes) ─────────────
# Left eye ≈(110,162), right eye ≈(175,162) in 300px
def draw_eye_swirl(draw, cx, cy, max_r, color):
    """Draw a tight spiral over an eye to give 'swirly dizzy eye' look."""
    steps = 200
    for i in range(steps - 1):
        t1 = i / steps
        t2 = (i + 1) / steps
        a1 = math.radians(t1 * 360 * 3)
        a2 = math.radians(t2 * 360 * 3)
        r1 = max_r * t1
        r2 = max_r * t2
        x1 = cx + r1 * math.cos(a1)
        y1 = cy + r1 * math.sin(a1)
        x2 = cx + r2 * math.cos(a2)
        y2 = cy + r2 * math.sin(a2)
        draw.line([x1, y1, x2, y2], fill=color, width=int(S * 2.2))

# White base to "blank out" the eye area first
# Eyes in 300px: left ~(112, 178), right ~(178, 178) — slightly lower than brows
for ex, ey in [(s(112), s(178)), (s(179), s(178))]:
    rw, rh = s(19), s(14)
    d.ellipse([ex-rw, ey-rh, ex+rw, ey+rh], fill=(240, 228, 210, 255))

# Then draw swirl on top
for ex, ey in [(s(112), s(178)), (s(179), s(178))]:
    draw_eye_swirl(d, ex, ey, s(13), (60, 30, 90, 220))
    # White shine dot
    d.ellipse([ex+s(3), ey-s(6), ex+s(7), ey-s(1)], fill=(255, 255, 255, 240))

# ── 3. Slightly open mouth ─────────────────────────────────────────────
mx, my = s(150), s(213)
d.ellipse([mx-s(12), my-s(6), mx+s(12), my+s(8)], fill=(55, 20, 20, 170))

# ── 4. Dizzy spirals above head ────────────────────────────────────────
def draw_spiral(draw, cx, cy, max_r, color, width=4):
    steps = 120
    for i in range(steps - 1):
        t1 = i / steps
        t2 = (i + 1) / steps
        a1 = math.radians(t1 * 360 * 2.2)  # ~2.2 turns
        a2 = math.radians(t2 * 360 * 2.2)
        r1 = max_r * t1
        r2 = max_r * t2
        x1 = cx + r1 * math.cos(a1)
        y1 = cy + r1 * math.sin(a1)
        x2 = cx + r2 * math.cos(a2)
        y2 = cy + r2 * math.sin(a2)
        draw.line([x1, y1, x2, y2], fill=color, width=width)

# Three spirals: left, top-center, right
spiral_cfg = [
    (s(90),  s(38), s(24), (200, 80, 240, 230)),
    (s(150), s(22), s(22), (255, 195, 0,  230)),
    (s(210), s(38), s(24), (80,  150, 255, 230)),
]
for sx, sy, sr, sc in spiral_cfg:
    draw_spiral(d, sx, sy, sr, sc, width=int(S*2.5))

# Question marks
try:
    font_q = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s(28))
except Exception:
    font_q = ImageFont.load_default()

d.text((s(118), s(12)), '?', fill=(255, 195, 0, 235), font=font_q)
d.text((s(168), s(12)), '?', fill=(200, 80, 240, 235), font=font_q)

# ── 5. Small stars / sparkles for extra dizzy flair ───────────────────
star_pts = [(s(72), s(55)), (s(228), s(55)), (s(150), s(8))]
sc_list  = [(255, 220, 0, 200), (180, 100, 255, 200), (100, 200, 255, 200)]
for (spx, spy), spc in zip(star_pts, sc_list):
    sr = s(8)
    # Simple 4-point star
    d.polygon([
        (spx, spy-sr), (spx+sr//3, spy-sr//3),
        (spx+sr, spy), (spx+sr//3, spy+sr//3),
        (spx, spy+sr), (spx-sr//3, spy+sr//3),
        (spx-sr, spy), (spx-sr//3, spy-sr//3),
    ], fill=spc)

# ── 6. Composite & slight tilt ─────────────────────────────────────────
merged = Image.alpha_composite(img, overlay)
tilted = merged.rotate(-7, resample=Image.BICUBIC, expand=False,
                        center=(W//2, int(H * 0.55)))

tilted.convert('RGBA').save('/home/user/ad/dazed_character2.png')
print("Saved → /home/user/ad/dazed_character2.png")
