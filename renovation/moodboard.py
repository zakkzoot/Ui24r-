#!/usr/bin/env python3
"""Compose the renovation MOOD BOARD / canvas (single PNG)."""
from PIL import Image, ImageDraw, ImageFont

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def fb(s): return ImageFont.truetype(FB, s)
def fr(s): return ImageFont.truetype(FR, s)

W, H = 1500, 2050
BG = (244, 241, 235)
INK = (44, 47, 52)
SUB = (122, 122, 128)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
M = 70

def card(x0, y0, x1, y1, fill=(255, 255, 255), r=18, border=None):
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill, outline=border, width=2)

def center(txt, x, y, font, fill):
    d.text((x - d.textlength(txt, font=font) / 2, y), txt, font=font, fill=fill)

# ---------------- header ----------------
d.text((M, 48), "APARTMENT RENOVATION", font=fb(58), fill=INK)
d.text((M, 116), "Maximum-ROI Refresh  ·  No construction, soft-furnishings only", font=fr(26), fill=SUB)
d.line([M, 168, W - M, 168], fill=(212, 206, 196), width=3)
d.text((M, 184), "MOOD BOARD & MATERIAL DIRECTION", font=fb(24), fill=(150, 120, 70))

# ---------------- palette ----------------
y = 240
d.text((M, y), "COLOUR PALETTE", font=fb(30), fill=INK)
y += 52
palette = [
    ("Warm White",  "#F2EFE9", "Walls — wash / touch-up"),
    ("Soft Linen",  "#E3DBCC", "New curtains"),
    ("Oat Greige",  "#C9BEA9", "Chair slipcovers"),
    ("Warm Taupe",  "#A89A85", "Throws / runner"),
    ("Charcoal",    "#3E4248", "Cushions, frames"),
    ("Navy Accent", "#2B4A6F", "Keep existing sofas"),
    ("Rattan Wood", "#B5854E", "Natural texture"),
    ("Sage Plant",  "#7E8E55", "Greenery"),
    ("Brushed Brass","#B49A60", "Lamp / handle accents"),
]
def hx(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
cols, cw, ch, gx, gy = 3, 420, 150, 30, 28
for i, (name, hexv, use) in enumerate(palette):
    cx = M + (i % cols) * (cw + gx)
    cy = y + (i // cols) * (ch + gy)
    card(cx, cy, cx + cw, cy + ch)
    d.rounded_rectangle([cx + 16, cy + 16, cx + 130, cy + ch - 16], radius=12, fill=hx(hexv),
                        outline=(225, 222, 215), width=1)
    d.text((cx + 150, cy + 26), name, font=fb(26), fill=INK)
    d.text((cx + 150, cy + 62), hexv, font=fr(20), fill=SUB)
    d.text((cx + 150, cy + 92), use, font=fr(19), fill=(120, 120, 126))
y = y + 3 * (ch + gy) + 18

# ---------------- two columns: materials + strategy ----------------
colw = (W - 2 * M - 40) // 2
lx, rx = M, M + colw + 40
top = y
# materials / textures
card(lx, top, lx + colw, top + 470, fill=(255, 255, 255))
d.text((lx + 28, top + 24), "TEXTURES & MATERIALS", font=fb(26), fill=INK)
mats = [
    ("Natural jute / sisal rug", "warms the cold grey tile, defines zones"),
    ("Linen curtains (oat/ivory)", "replace red drapes — calm, light"),
    ("Cotton slipcovers", "tame the lime chairs to greige"),
    ("Rattan & light wood", "papasan frame, baskets — keep/lean in"),
    ("Indoor plants", "monstera, palm, snake plant"),
    ("Warm-white LED 2700K", "swap cool bulbs; cozy evening light"),
    ("Brushed brass accents", "lamp, handles, mirror frame"),
    ("Framed art set, neutral mats", "gallery feel on big blank walls"),
]
yy = top + 70
for t, s in mats:
    d.ellipse([lx + 30, yy + 8, lx + 42, yy + 20], fill=(150, 120, 70))
    d.text((lx + 56, yy), t, font=fb(21), fill=INK)
    d.text((lx + 56, yy + 27), s, font=fr(18), fill=SUB)
    yy += 50
# strategy
card(rx, top, rx + colw, top + 470, fill=(33, 37, 43))
d.text((rx + 28, top + 24), "THE STRATEGY", font=fb(26), fill=(245, 243, 238))
strat = [
    "De-clutter & deep clean every surface",
    "Repaint scuffed walls the same warm white",
    "ONE accent colour (navy) — kill the rest",
    "Soft furnishings do the heavy lifting",
    "Layer texture, not colour, for warmth",
    "Style kitchen bar + add bar-stool cushions",
    "Greenery + mirrors to lift & enlarge",
    "Re-shoot listing photos in daylight",
]
yy = top + 70
for s in strat:
    d.text((rx + 30, yy), "—", font=fb(21), fill=(150, 170, 140))
    d.text((rx + 60, yy), s, font=fr(21), fill=(232, 230, 224))
    yy += 49
y = top + 470 + 36

# ---------------- budget snapshot ----------------
card(M, y, W - M, y + 150, fill=(255, 255, 255))
d.text((M + 28, y + 22), "BUDGET SNAPSHOT  (indicative, USD)", font=fb(26), fill=INK)
budget = [("Soft furnishings", "320"), ("Rug + plants", "140"),
          ("Paint + lighting", "120"), ("Art + decor", "90"), ("TOTAL", "~670")]
bx = M + 28
seg = (W - 2 * M - 56) // len(budget)
for i, (k, v) in enumerate(budget):
    cx = bx + i * seg
    big = (k == "TOTAL")
    d.text((cx, y + 78), k, font=fr(19), fill=SUB)
    d.text((cx, y + 104), "$" + v, font=fb(30 if big else 26),
           fill=(150, 120, 70) if big else INK)
y += 150 + 36

# ---------------- after thumbnails ----------------
d.text((M, y), "RESTYLED ROOMS  (after)", font=fb(28), fill=INK)
y += 50
thumbs = ["renders/reno_living.jpg", "renders/reno_lounge.jpg",
          "renders/reno_seating.jpg", "renders/reno_bedroom.jpg"]
tw = (W - 2 * M - 3 * 24) // 4
for i, t in enumerate(thumbs):
    im = Image.open(t).convert("RGB")
    th = int(tw * im.height / im.width)
    im = im.resize((tw, th))
    cx = M + i * (tw + 24)
    img.paste(im, (cx, y))
    d.rounded_rectangle([cx, y, cx + tw, y + th], radius=10, outline=(210, 205, 196), width=2)

d.text((M, H - 46), "Concept visualisation — colours simulated from listing photos.",
       font=fr(18), fill=(150, 150, 156))
img.save("moodboard/moodboard.png")
print("saved moodboard/moodboard.png", img.size)
