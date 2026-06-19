import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = "/root/.claude/uploads/3327c047-f956-554e-a3bb-7362526c762c/b4bc20e5-49225.png"
OUT = "/home/user/ad/dizzy_output.png"

img = Image.open(SRC).convert("RGBA")
W, H = img.size

# ---- 1. Very gentle swirl (a faint woozy lean, face stays clear) ----
cx, cy = W * 0.5, H * 0.52
radius = W * 0.48
strength = 0.42                       # subtle — just a hint of warp

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

base = img.convert("RGB")

# ---- 1b. Glassy unfocused gaze (the quiet "懵" lives in the eyes) ----
eye_blur = base.filter(ImageFilter.GaussianBlur(5))
eye_mask = Image.new("L", (W, H), 0)
em = ImageDraw.Draw(eye_mask)
# two soft ovals over the eyes (positions after the gentle swirl)
for ex, ey in [(W * 0.41, H * 0.63), (W * 0.62, H * 0.605)]:
    rx, ry = W * 0.075, H * 0.05
    em.ellipse([ex - rx, ey - ry, ex + rx, ey + ry], fill=120)
eye_mask = eye_mask.filter(ImageFilter.GaussianBlur(int(W * 0.03)))
base = Image.composite(eye_blur, base, eye_mask)

# ---- 2. Dreamy soft-focus glow (the "out of it" depth) ----
glow = base.filter(ImageFilter.GaussianBlur(6))
base = Image.blend(base, glow, 0.18)

# ---- 3. Whisper of double vision (very faint, low offset) ----
ghost = base.filter(ImageFilter.GaussianBlur(2))
shifted = Image.new("RGB", (W, H), (255, 255, 255))
shifted.paste(ghost, (7, 3))
base = Image.blend(base, shifted, 0.12)

# ---- 4. Subtle chromatic shimmer ----
r, g, b = base.split()
r = r.transform((W, H), Image.AFFINE, (1, 0, -3, 0, 1, 0))
b = b.transform((W, H), Image.AFFINE, (1, 0, 3, 0, 1, 0))
base = Image.merge("RGB", (r, g, b))

# ---- 5. Soft depth vignette (pulls focus inward, dreamy) ----
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([int(-W * 0.10), int(-H * 0.10), int(W * 1.10), int(H * 1.10)], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(int(W * 0.12)))
dark = Image.new("RGB", (W, H), (245, 244, 248))   # gentle, light vignette
base = Image.composite(base, dark, vig)

base.save(OUT, quality=95)
print("saved", OUT)
