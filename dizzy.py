import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = "/root/.claude/uploads/3327c047-f956-554e-a3bb-7362526c762c/b4bc20e5-49225.png"
OUT = "/home/user/ad/dizzy_output.png"

img = Image.open(SRC).convert("RGBA")
W, H = img.size

# ---- 1. Spiral "@_@" dizzy eyes (drawn first so the swirl warps them in place) ----
def spiral_eye(d, ex, ey, er, turns=3.2, col=(35, 25, 25)):
    pts = []
    steps = 260
    for i in range(steps):
        t = i / steps
        a = t * turns * 2 * math.pi
        rad = er * t
        pts.append((ex + rad * math.cos(a), ey + rad * math.sin(a)))
    d.line(pts, fill=col, width=max(4, er // 7), joint="curve")

draw0 = ImageDraw.Draw(img)
# cover the original eyes with skin-ish discs, then draw spirals on top
def disc(d, ex, ey, er, col):
    d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=col)

LE = (int(W * 0.41), int(H * 0.63))
RE = (int(W * 0.63), int(H * 0.60))
ER = int(W * 0.058)
disc(draw0, *LE, ER, (250, 222, 198, 255))
disc(draw0, *RE, ER, (250, 222, 198, 255))
spiral_eye(draw0, *LE, ER)
spiral_eye(draw0, *RE, ER)

# ---- 2. Swirl / twist distortion (the woozy warp) ----
cx, cy = W * 0.5, H * 0.50          # head/eye center
radius = W * 0.50                    # area affected by the swirl
strength = 1.25                      # rotation amount at the center

arr = np.asarray(img).astype(np.float32)
ys, xs = np.mgrid[0:H, 0:W]
dx = xs - cx
dy = ys - cy
dist = np.sqrt(dx * dx + dy * dy)
angle = np.arctan2(dy, dx)
amount = np.clip(1.0 - dist / radius, 0, 1) ** 1.5
twist = angle + strength * amount
src_x = np.clip((cx + dist * np.cos(twist)).astype(np.int32), 0, W - 1)
src_y = np.clip((cy + dist * np.sin(twist)).astype(np.int32), 0, H - 1)
img = Image.fromarray(arr[src_y, src_x].astype(np.uint8), "RGBA")

# ---- 3. Double-vision ghosting + chromatic split (swimmy / blurry feel) ----
base = img.convert("RGB")
ghost = base.filter(ImageFilter.GaussianBlur(4))
shifted = Image.new("RGB", (W, H), (255, 255, 255))
shifted.paste(ghost, (14, 6))
base = Image.blend(base, shifted, 0.26)

r, g, b = base.split()
r = r.transform((W, H), Image.AFFINE, (1, 0, -8, 0, 1, 0))
b = b.transform((W, H), Image.AFFINE, (1, 0, 8, 0, 1, 0))
base = Image.merge("RGB", (r, g, b))
img = base.convert("RGBA")

draw = ImageDraw.Draw(img)

# ---- 4. Orbiting stars circling the head ----
def star(d, cxp, cyp, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cxp + rr * math.cos(ang), cyp + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)

orbit_cx, orbit_cy = W * 0.5, H * 0.15
orbit_rx, orbit_ry = W * 0.30, H * 0.075
n = 6
for i in range(n):
    a = i / n * 2 * math.pi
    sx = orbit_cx + orbit_rx * math.cos(a)
    sy = orbit_cy + orbit_ry * math.sin(a)
    size = int(W * (0.018 + 0.012 * (0.5 + 0.5 * math.sin(a))))
    star(draw, sx, sy, size, (255, 205, 40))
    star(draw, sx, sy, max(2, size // 3), (255, 245, 180))

draw.arc([orbit_cx - orbit_rx, orbit_cy - orbit_ry,
          orbit_cx + orbit_rx, orbit_cy + orbit_ry],
         start=0, end=360, fill=(255, 220, 120), width=4)

img.convert("RGB").save(OUT, quality=95)
print("saved", OUT)
