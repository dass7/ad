import math
from PIL import Image, ImageDraw, ImageFilter

SRC = "/root/.claude/uploads/3327c047-f956-554e-a3bb-7362526c762c/8655663a-49225.png"
OUTDIR = "/home/user/ad"

base0 = Image.open(SRC).convert("RGB")
W, H = base0.size
LE = (int(W * 0.412), int(H * 0.632))
RE = (int(W * 0.632), int(H * 0.596))
SKIN = (252, 219, 191)
INK = (40, 32, 30)
S = 3

def cover_eyes(img):
    """Paint feathered skin over the two original eyes."""
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    for (cx, cy) in (LE, RE):
        md.ellipse([cx - 92, cy - 64, cx + 92, cy + 62], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(8))
    return Image.composite(Image.new("RGB", (W, H), SKIN), img, mask)

def new_layer():
    return Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))

def flatten(img, layer):
    layer = layer.resize((W, H), Image.LANCZOS)
    out = img.convert("RGBA")
    out.alpha_composite(layer)
    return out.convert("RGB")

def star(d, cx, cy, r, fill, outline=INK, ow=3, rot=-90):
    pts = []
    for i in range(10):
        ang = math.radians(rot + i * 36)
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill, outline=outline, width=ow)

def spiral(d, cx, cy, rmax, turns, width, color):
    pts = []
    steps = int(turns * 48)
    for i in range(steps + 1):
        t = i / steps
        ang = t * turns * 2 * math.pi
        rad = rmax * t
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.line(pts, fill=color, width=width, joint="curve")


# ============ V1 : circling stars ============
def v1():
    img = base0.copy()
    L = new_layer(); d = ImageDraw.Draw(L)
    cx, cy = int(W * 0.50 * S), int(H * 0.155 * S)
    rx, ry = int(W * 0.30 * S), int(H * 0.085 * S)
    n = 7
    for i in range(n):
        a = math.radians(i * 360 / n - 90)
        x = cx + rx * math.cos(a)
        y = cy + ry * math.sin(a)
        sz = (26 + 10 * math.cos(a)) * S
        col = (255, 208, 60) if i % 2 == 0 else (255, 235, 130)
        star(d, x, y, sz, col, ow=3 * S)
    # little motion swirls near temples
    for (ex, ey, fl) in [(W * 0.30, H * 0.40, 1), (W * 0.72, H * 0.40, -1)]:
        spiral(d, int(ex * S), int(ey * S), 34 * S, 1.6, 5 * S, (120, 120, 130, 220))
    return flatten(img, L)


# ============ V2 : swirl (mosquito-coil) eyes ============
def v2():
    img = cover_eyes(base0.copy())
    L = new_layer(); d = ImageDraw.Draw(L)
    for (cx, cy) in (LE, RE):
        spiral(d, cx * S, cy * S, 46 * S, 2.6, 7 * S, INK + (255,))
    # tiny dizzy sweat drop
    dx, dy = int(W * 0.74 * S), int(H * 0.56 * S)
    d.ellipse([dx - 12 * S, dy - 16 * S, dx + 12 * S, dy + 20 * S],
              fill=(150, 205, 235, 235), outline=INK + (255,), width=2 * S)
    return flatten(img, L)


# ============ V3 : X eyes / fainted ============
def v3():
    img = cover_eyes(base0.copy())
    # bluish gloom over the upper face
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    gd.rectangle([int(W * 0.24), int(H * 0.30), int(W * 0.78), int(H * 0.62)],
                 fill=(70, 110, 160, 70))
    gl = gl.filter(ImageFilter.GaussianBlur(40))
    img = Image.alpha_composite(img.convert("RGBA"), gl).convert("RGB")
    L = new_layer(); d = ImageDraw.Draw(L)
    for (cx, cy) in (LE, RE):
        r = 34 * S
        for (ax, ay) in [(-1, -1), (1, -1)]:
            d.line([(cx * S - r, cy * S - r * ay), (cx * S + r, cy * S + r * ay)],
                   fill=INK + (255,), width=9 * S)
        d.line([(cx * S - r, cy * S - r), (cx * S + r, cy * S + r)],
               fill=INK + (255,), width=9 * S)
        d.line([(cx * S - r, cy * S + r), (cx * S + r, cy * S - r)],
               fill=INK + (255,), width=9 * S)
    # blue vertical shadow lines on forehead
    for k in range(3):
        fx = int((0.44 + k * 0.06) * W * S)
        d.line([(fx, int(H * 0.34 * S)), (fx, int(H * 0.42 * S))],
               fill=(90, 130, 175, 230), width=5 * S)
    return flatten(img, L)


# ============ V4 : feverish blush + steam ============
def v4():
    img = base0.copy()
    # blush
    bl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bl)
    for cx in (int(W * 0.34), int(W * 0.70)):
        bd.ellipse([cx - 60, int(H * 0.66) - 34, cx + 60, int(H * 0.66) + 34],
                   fill=(240, 110, 110, 150))
    bl = bl.filter(ImageFilter.GaussianBlur(18))
    img = Image.alpha_composite(img.convert("RGBA"), bl).convert("RGB")
    L = new_layer(); d = ImageDraw.Draw(L)
    # blush hatch lines
    for cx in (W * 0.34, W * 0.70):
        for k in range(3):
            x = int((cx + (k - 1) * 0.035 * W) * S)
            d.line([(x, int(H * 0.655 * S)), (x, int(H * 0.685 * S))],
                   fill=(200, 70, 70, 235), width=4 * S)
    # steam puffs above head
    for (sx, sy, r) in [(0.39, 0.045, 26), (0.50, 0.02, 32), (0.61, 0.045, 24)]:
        d.ellipse([int((sx * W - r) * S), int((sy * H - r) * S),
                   int((sx * W + r) * S), int((sy * H + r) * S)],
                  fill=(235, 235, 235, 180), outline=(180, 180, 180, 200), width=3 * S)
    # sweat drop
    dx, dy = int(W * 0.74 * S), int(H * 0.50 * S)
    d.ellipse([dx - 12 * S, dy - 16 * S, dx + 12 * S, dy + 20 * S],
              fill=(150, 205, 235, 235), outline=INK + (255,), width=2 * S)
    return flatten(img, L)


# ============ V5 : spiral background + wavy eyes ============
def v5():
    img = cover_eyes(base0.copy())
    # radial spiral behind everything-ish (drawn as translucent overlay)
    bg = new_layer(); bd = ImageDraw.Draw(bg)
    spiral(bd, int(W * 0.5 * S), int(H * 0.42 * S), int(W * 0.62 * S),
           5.5, 10 * S, (255, 170, 70, 90))
    img = flatten(img, bg)
    L = new_layer(); d = ImageDraw.Draw(L)
    for (cx, cy) in (LE, RE):
        pts = []
        for i in range(33):
            t = i / 32
            x = cx * S - 44 * S + t * 88 * S
            y = cy * S + math.sin(t * 4 * math.pi) * 13 * S
            pts.append((x, y))
        d.line(pts, fill=INK + (255,), width=7 * S, joint="curve")
    return flatten(img, L)


outs = []
for name, fn in [("v1_stars", v1), ("v2_swirl", v2), ("v3_xeyes", v3),
                 ("v4_fever", v4), ("v5_spiral", v5)]:
    p = f"{OUTDIR}/dizzy_{name}.png"
    fn().save(p)
    outs.append(p)
    print("saved", p)
