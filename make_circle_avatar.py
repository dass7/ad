from PIL import Image, ImageDraw

src = '/home/user/ad/dazed_character.png'
img = Image.open(src).convert('RGBA')
W, H = img.size

# ── 1. Crop to circle ──────────────────────────────────────────────────
mask = Image.new('L', (W, H), 0)
ImageDraw.Draw(mask).ellipse([0, 0, W, H], fill=255)

circle_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
circle_img.paste(img, mask=mask)

# ── 2. Add white circle background behind the character ────────────────
canvas_size = int(W * 1.12)
canvas = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))

# White filled circle (background)
bg = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
ImageDraw.Draw(bg).ellipse([0, 0, canvas_size, canvas_size], fill=(255, 255, 255, 255))
canvas = Image.alpha_composite(canvas, bg)

# Paste the character circle centered
offset = (canvas_size - W) // 2
canvas.paste(circle_img, (offset, offset), circle_img)

# ── 3. Dark background (like the reference) ────────────────────────────
final_size = int(canvas_size * 1.5)
final = Image.new('RGB', (final_size, final_size), (15, 15, 15))

final_rgba = final.convert('RGBA')
cx = (final_size - canvas_size) // 2
cy = (final_size - canvas_size) // 2
final_rgba.paste(canvas, (cx, cy), canvas)

out = final_rgba.convert('RGB')
out.save('/home/user/ad/dazed_avatar_circle.png', quality=95)
print(f"Saved → dazed_avatar_circle.png  ({final_size}x{final_size})")
