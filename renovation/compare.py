#!/usr/bin/env python3
"""Build labelled BEFORE / AFTER comparison boards for each restyled room."""
from PIL import Image, ImageDraw, ImageFont

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
INK = (38, 42, 48)

PAIRS = [
    ("originals/343edbc6-1000001675.jpg", "renders/reno_living.jpg",
     "LIVING / KITCHEN", "Neutral drapes, greige accent chair, brightened"),
    ("originals/1f5ccd77-1000001677.jpg", "renders/reno_seating.jpg",
     "LOUNGE SEATING", "Loud red & lime swapped for linen + greige"),
    ("originals/e7c670e2-1000001676.jpg", "renders/reno_lounge.jpg",
     "OPEN-PLAN LOUNGE", "Cohesive palette; navy kept as the one accent"),
    ("originals/86bb0ced-1000001681.jpg", "renders/reno_bedroom.jpg",
     "MASTER BEDROOM", "Hotel-white bedding, soft linen curtains"),
]

def board(before, after, title, sub, out):
    a = Image.open(before).convert("RGB")
    b = Image.open(after).convert("RGB")
    W = 900
    def fit(im):
        return im.resize((W, int(W * im.height / im.width)))
    a, b = fit(a), fit(b)
    pad, gap, head, foot = 28, 18, 96, 34
    H = head + a.height + gap + b.height + foot
    canvas = Image.new("RGB", (W + pad * 2, H), (247, 245, 241))
    d = ImageDraw.Draw(canvas)
    d.text((pad, 24), title, font=ImageFont.truetype(FB, 40), fill=INK)
    d.text((pad, 70), sub, font=ImageFont.truetype(FR, 20), fill=(120, 120, 125))
    y = head
    for im, tag, col in [(a, "BEFORE", (176, 64, 60)), (b, "AFTER", (70, 120, 90))]:
        canvas.paste(im, (pad, y))
        chip = ImageFont.truetype(FB, 22)
        tw = d.textlength(tag, font=chip)
        d.rectangle([pad + 14, y + 14, pad + 14 + tw + 28, y + 50], fill=col)
        d.text((pad + 28, y + 18), tag, font=chip, fill=(255, 255, 255))
        y += im.height + gap
    d.text((pad, H - 28), "Virtual restyle - soft furnishings only, no construction",
           font=ImageFont.truetype(FR, 16), fill=(150, 150, 155))
    canvas.save(out, quality=92)
    print("  ->", out)

if __name__ == "__main__":
    for bef, aft, t, s in PAIRS:
        name = aft.split("/")[-1].replace("reno_", "compare_")
        board(bef, aft, t, s, f"renders/{name}")
