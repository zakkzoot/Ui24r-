#!/usr/bin/env python3
"""Assemble the renovation deliverable into a single multi-page PDF
(cover + mood board + before/after boards + written plan with ROI table).
Pages are composed with Pillow so every image is embedded reliably."""
from PIL import Image, ImageDraw, ImageFont

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def fb(s): return ImageFont.truetype(FB, s)
def fr(s): return ImageFont.truetype(FR, s)

# A4 portrait @ ~150 dpi
PW, PH = 1240, 1754
CREAM = (244, 241, 235)
WHITE = (255, 255, 255)
INK = (44, 47, 52)
SUB = (122, 122, 128)
GOLD = (150, 120, 70)
M = 90
pages = []

def new_page(bg=WHITE):
    p = Image.new("RGB", (PW, PH), bg)
    return p, ImageDraw.Draw(p)

def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def paste_fit(page, im, box):
    """Fit im inside box (x0,y0,x1,y1) preserving aspect, centered; return drawn rect."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    s = min(bw / im.width, bh / im.height)
    nw, nh = int(im.width * s), int(im.height * s)
    im = im.resize((nw, nh))
    px, py = x0 + (bw - nw) // 2, y0 + (bh - nh) // 2
    page.paste(im, (px, py))
    return px, py, px + nw, py + nh

# ---------------- 1. COVER ----------------
p, d = new_page(CREAM)
d.rectangle([0, 0, PW, 14], fill=GOLD)
d.text((M, 120), "APARTMENT", font=fb(86), fill=INK)
d.text((M, 210), "RENOVATION", font=fb(86), fill=INK)
d.text((M, 330), "Maximum-ROI Refresh", font=fr(38), fill=GOLD)
d.text((M, 386), "No construction  ·  soft-furnishings only", font=fr(28), fill=SUB)
hero = Image.open("renders/reno_living.jpg").convert("RGB")
hx0, hy0, hx1, hy1 = paste_fit(p, hero, (M, 470, PW - M, 470 + 620))
d.rounded_rectangle([hx0, hy0, hx1, hy1], radius=4, outline=(210, 205, 196), width=3)
# stat strip
sy = hy1 + 60
stats = [("BUDGET", "~$670"), ("TIMELINE", "1 weekend"), ("WORKS", "Minor only")]
seg = (PW - 2 * M) // 3
for i, (k, v) in enumerate(stats):
    cx = M + i * seg
    d.text((cx, sy), k, font=fr(22), fill=SUB)
    d.text((cx, sy + 32), v, font=fb(40), fill=INK)
d.text((M, PH - 70), "Concept visualisation — colours simulated from the listing photos.",
       font=fr(20), fill=SUB)
pages.append(p)

def image_page(path, title, caption):
    p, d = new_page(WHITE)
    d.text((M, 56), title, font=fb(40), fill=INK)
    d.line([M, 116, PW - M, 116], fill=(225, 222, 215), width=2)
    im = Image.open(path).convert("RGB")
    paste_fit(p, im, (M, 140, PW - M, PH - 120))
    d.text((M, PH - 78), caption, font=fr(22), fill=SUB)
    pages.append(p)

# ---------------- 2. MOOD BOARD ----------------
image_page("moodboard/moodboard.png", "Mood Board & Material Direction",
           "Palette, textures, strategy and budget at a glance.")

# ---------------- 3-6. BEFORE / AFTER ----------------
for f, t in [("compare_living.jpg",  "Before / After — Living & Kitchen"),
             ("compare_lounge.jpg",  "Before / After — Open-plan Lounge"),
             ("compare_seating.jpg", "Before / After — Lounge Seating"),
             ("compare_bedroom.jpg", "Before / After — Master Bedroom")]:
    image_page(f"renders/{f}", t, "Soft-furnishings restyle — no construction.")

# ---------------- 7+. WRITTEN PLAN ----------------
# lightweight block renderer with pagination
BLOCKS = [
    ("h1", "The Plan"),
    ("body", "The apartment has good bones — high ceilings, an open plan, a granite "
             "kitchen bar and an already-renovated bathroom. What drags the value down "
             "is visual chaos: red curtains, lime-green chairs, an orange papasan and "
             "yellow bedding all clashing against cold grey tile. The fix is the "
             "palette, not the structure."),
    ("h2", "Design direction"),
    ("bul", "Warm white walls + soft-linen curtains + greige upholstery as the base."),
    ("bul", "ONE accent colour — the existing navy sofas — everything else neutral."),
    ("bul", "Layer texture not colour: jute rug, rattan, light wood, plants, brass."),
    ("bul", "Warm-white 2700K bulbs throughout to kill the clinical feel."),
    ("h2", "Room-by-room"),
    ("bul", "Living/lounge: linen curtains, greige slipcovers on the lime chairs, "
            "jute rug under the table, a tall plant in the empty corner, neutral art."),
    ("bul", "Bedroom: hotel-white bedding + charcoal throw, soft-linen curtains, "
            "small bedside rug, one piece of art."),
    ("bul", "Kitchen/bar: already strong — just style it (stool cushions, bowl, herb "
            "plant, declutter). Optional peel-and-stick backsplash."),
    ("bul", "Bathroom: already on-trend — leave it; add white towels + a plant."),
    ("bul", "Balcony: bistro set + potted plants turns it into an outdoor selling point."),
    ("h2", "Budget (indicative, USD)"),
    ("tbl", [("Curtains (linen) x3-4", "$90"), ("Chair slipcovers / re-covers", "$80"),
             ("Cushions, throws, hotel bedding", "$110"), ("Jute rug + bedside rug", "$70"),
             ("Plants x4-5 + pots", "$70"), ("Warm-white LED bulbs", "$30"),
             ("Paint touch-ups + sundries", "$60"), ("Framed art / mirrors", "$90"),
             ("Balcony bistro set", "$70"), ("TOTAL", "~$670")]),
    ("h2", "Why the ROI is high"),
    ("body", "Spend is one-off and mostly portable, with no permits, trades or downtime — "
             "doable in a weekend. A cohesive, bright, move-in-ready look supports a higher "
             "asking rent, lets faster and photographs far better. A $600-700 outlay like "
             "this commonly supports $30-60/month more rent and a shorter void — a payback "
             "in roughly a year, then pure profit."),
    ("body", "Deliberately avoided: wall removal, re-tiling, kitchen/bath rebuild, rewiring "
             "— all high-cost, low-return for a rental at this level."),
]

def render_blocks(blocks):
    p, d = new_page(WHITE)
    d.rectangle([0, 0, PW, 14], fill=GOLD)
    y = 70
    cw = PW - 2 * M
    for kind, content in blocks:
        if kind == "h1":
            need = 90
        elif kind == "h2":
            need = 70
        elif kind == "tbl":
            need = 40 * len(content) + 30
        else:
            need = 40
        if y + need > PH - 90:
            pages.append(p); p, d = new_page(WHITE); y = 70
        if kind == "h1":
            d.text((M, y), content, font=fb(48), fill=INK); y += 70
            d.line([M, y, PW - M, y], fill=(225, 222, 215), width=2); y += 28
        elif kind == "h2":
            y += 14
            d.text((M, y), content, font=fb(30), fill=GOLD); y += 50
        elif kind == "bul":
            d.ellipse([M + 4, y + 10, M + 16, y + 22], fill=GOLD)
            for ln in wrap(d, content, fr(24), cw - 40):
                d.text((M + 34, y), ln, font=fr(24), fill=INK); y += 34
            y += 12
        elif kind == "body":
            for ln in wrap(d, content, fr(24), cw):
                d.text((M, y), ln, font=fr(24), fill=INK); y += 34
            y += 16
        elif kind == "tbl":
            for k, v in content:
                big = k == "TOTAL"
                f1 = fb(25) if big else fr(24)
                d.text((M + 10, y), k, font=f1, fill=GOLD if big else INK)
                d.text((PW - M - d.textlength(v, font=f1) - 10, y), v, font=f1,
                       fill=GOLD if big else INK)
                y += 38
                d.line([M, y - 6, PW - M, y - 6], fill=(238, 235, 229), width=1)
            y += 16
    pages.append(p)

render_blocks(BLOCKS)

out = "Renovation_Plan.pdf"
pages[0].save(out, save_all=True, append_images=pages[1:], resolution=150.0)
print(f"saved {out}  ({len(pages)} pages)")
