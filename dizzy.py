import math
from PIL import Image, ImageDraw, ImageFilter

SRC = "/root/.claude/uploads/3327c047-f956-554e-a3bb-7362526c762c/b4bc20e5-49225.png"
OUT = "/home/user/ad/dizzy_output.png"

base = Image.open(SRC).convert("RGB")
W, H = base.size

# Eye centers (measured from the artwork)
LE = (int(W * 0.412), int(H * 0.632))
RE = (int(W * 0.632), int(H * 0.596))
SKIN = (252, 219, 191)
INK = (44, 34, 32)

# ---- 1. Cover the original eyes AND eyebrows with feathered skin ----
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
for (cx, cy) in (LE, RE):
    md.ellipse([cx - 96, cy - 72, cx + 96, cy + 70], fill=255)
# eyebrows (the upper "pair") -> removed so only one pair of eyes reads
md.ellipse([int(W * 0.445 - 104), int(H * 0.555 - 40),
            int(W * 0.445 + 104), int(H * 0.555 + 40)], fill=255)
md.ellipse([int(W * 0.665 - 92), int(H * 0.535 - 40),
            int(W * 0.665 + 92), int(H * 0.535 + 40)], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(9))
skin = Image.new("RGB", (W, H), SKIN)
base = Image.composite(skin, base, mask)

# ---- 2. Draw new dopey / dazed eyes (supersampled for clean lines) ----
S = 3
layer = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
ld = ImageDraw.Draw(layer)

def eye(cx, cy, tilt, pupil_dx):
    """Half-lidded vacant eye. tilt>0 raises the outer corner.
    pupil_dx pushes the pupil toward the nose (cross-eyed)."""
    cx, cy = cx * S, cy * S
    hw, hh = 86 * S, 40 * S          # eye opening half-size
    lid_w = 15 * S

    # eye white
    white = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    wd = ImageDraw.Draw(white)
    wd.ellipse([cx - hw, cy - hh, cx + hw, cy + hh], fill=(250, 248, 246, 255))
    white = white.rotate(tilt, center=(cx, cy))
    layer.alpha_composite(white)

    feature = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(feature)
    # upper-lid arc (lifted a bit -> awake, focused, not vacant)
    od.arc([cx - hw, cy - hh - 14 * S, cx + hw, cy + hh + 14 * S],
           start=182, end=358, fill=INK + (255,), width=lid_w)
    # little lash flick at the outer corner
    od.line([(cx + hw - 4 * S, cy - 4 * S), (cx + hw + 24 * S, cy - 22 * S)],
            fill=INK + (255,), width=lid_w)
    feature = feature.rotate(tilt, center=(cx, cy))
    layer.alpha_composite(feature)

    # full rounded iris (focused, not a vacant dot)
    pr = 37 * S
    px, py = cx + pupil_dx * S, cy + 6 * S
    ld.ellipse([px - pr, py - pr, px + pr, py + pr], fill=INK + (255,))
    # catchlight
    ld.ellipse([px - pr + 7 * S, py - pr + 7 * S, px - pr + 22 * S, py - pr + 22 * S],
               fill=(255, 255, 255, 235))

def closed_eye(cx, cy, tilt):
    """A simple closed-eye line for the other side."""
    cx, cy = cx * S, cy * S
    hw = 80 * S
    line = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(line)
    # gentle convex-up curve = closed lid
    cd.arc([cx - hw, cy - 28 * S, cx + hw, cy + 34 * S],
           start=200, end=340, fill=INK + (255,), width=15 * S)
    # lash flick at the outer corner to match the open eye
    cd.line([(cx + hw - 8 * S, cy - 8 * S), (cx + hw + 22 * S, cy - 24 * S)],
            fill=INK + (255,), width=15 * S)
    line = line.rotate(tilt, center=(cx, cy))
    layer.alpha_composite(line)

# keep one dazed eye (pupil centered, no cross-eye); closed line on the other
eye(*LE, tilt=8, pupil_dx=0)
closed_eye(*RE, tilt=-8)

layer = layer.resize((W, H), Image.LANCZOS)
base = base.convert("RGBA")
base.alpha_composite(layer)

base.convert("RGB").save(OUT, quality=95)
print("saved", OUT)
