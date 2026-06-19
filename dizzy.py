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

# ---- 1. Cover the original eyes with feathered skin ----
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
for (cx, cy) in (LE, RE):
    md.ellipse([cx - 96, cy - 72, cx + 96, cy + 70], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(10))
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
    hw, hh = 86 * S, 34 * S          # eye opening half-size (shallow = half-lidded)
    lid_w = 15 * S

    # eye white (thin lens shape under the heavy lid)
    white = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    wd = ImageDraw.Draw(white)
    wd.ellipse([cx - hw, cy - hh, cx + hw, cy + hh], fill=(250, 248, 246, 255))
    white = white.rotate(tilt, center=(cx, cy))
    layer.alpha_composite(white)

    feature = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(feature)
    # heavy upper-lid arc dipping low over the eye -> sleepy / 半睁放空
    od.arc([cx - hw, cy - hh - 30 * S, cx + hw, cy + hh + 8 * S],
           start=182, end=358, fill=INK + (255,), width=lid_w)
    # little lash flick at the outer corner
    od.line([(cx + hw - 4 * S, cy - 4 * S), (cx + hw + 24 * S, cy - 22 * S)],
            fill=INK + (255,), width=lid_w)
    # faint lower-lid / tired bag line
    od.arc([cx - hw + 18 * S, cy - 6 * S, cx + hw - 18 * S, cy + hh + 26 * S],
           start=20, end=160, fill=(150, 120, 110, 180), width=5 * S)
    feature = feature.rotate(tilt, center=(cx, cy))
    layer.alpha_composite(feature)

    # tiny vacant dot pupil, pulled toward the nose & sitting low (looking down-in)
    pr = 18 * S
    px, py = cx + pupil_dx * S, cy + 12 * S
    ld.ellipse([px - pr, py - pr, px + pr, py + pr], fill=INK + (255,))
    # faint catchlight
    ld.ellipse([px - pr + 4 * S, py - pr + 4 * S, px - pr + 12 * S, py - pr + 12 * S],
               fill=(255, 255, 255, 220))

# left eye pupil drifts right(+), right eye pupil drifts left(-) => cross-eyed
eye(*LE, tilt=8, pupil_dx=34)
eye(*RE, tilt=-8, pupil_dx=-34)

layer = layer.resize((W, H), Image.LANCZOS)
base = base.convert("RGBA")
base.alpha_composite(layer)

base.convert("RGB").save(OUT, quality=95)
print("saved", OUT)
