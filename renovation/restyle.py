#!/usr/bin/env python3
"""
Virtual restyle engine for the apartment ROI renovation.

Strategy (no construction, soft-furnishings only):
  - Detect loud / clashing items by hue (red curtains, lime-green chairs,
    yellow bedding, orange runner, red papasan cushion).
  - Remap each region's LUMINANCE onto a new neutral material palette.
    Mapping luminance -> (shadow..highlight) of the new fabric keeps the
    folds, creases and shading, so it reads as a real reupholster / new
    drape rather than a flat paint fill.
  - Keep the navy sofa (timeless accent) and add a gentle warm,
    brightened "listing-grade" tone pass at the end.
"""
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

ORIG = "originals"
OUT = "renders"

# ---- new material palettes: (shadow_rgb, highlight_rgb) ----
LINEN_DRAPE   = ((150, 142, 128), (226, 220, 206))  # warm oatmeal linen curtains
TAUPE_FABRIC  = (( 99,  96,  90), (180, 176, 168))  # soft greige upholstery (was lime green)
WHITE_LINEN   = ((196, 196, 190), (246, 245, 241))  # hotel-white bedding (was yellow)
GREIGE_SOFT   = ((138, 132, 122), (214, 208, 196))  # greige cushions / runner

def open_mask(mask, size=5):
    """Morphological opening (erode->dilate) to delete small specks while
    preserving large upholstery regions."""
    m = Image.fromarray((mask * 255).astype(np.uint8), "L")
    # erode (kills specks) then dilate slightly larger (recovers thin rims)
    m = m.filter(ImageFilter.MinFilter(size)).filter(ImageFilter.MaxFilter(size + 2))
    return (np.asarray(m, dtype=np.float32) / 255.0 > 0.5).astype(np.float32)

def feather(mask, radius=2.0):
    m = Image.fromarray((mask * 255).astype(np.uint8), "L")
    m = m.filter(ImageFilter.GaussianBlur(radius))
    return np.asarray(m, dtype=np.float32) / 255.0

# ---- detectors ----
def _hsv(a):
    """Return per-pixel hue(deg 0-360), saturation(0-1), value(0-1)."""
    r, g, b = a[..., 0] / 255., a[..., 1] / 255., a[..., 2] / 255.
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    d = mx - mn + 1e-9
    h = np.zeros_like(mx)
    h = np.where(mx == r, ((g - b) / d) % 6, h)
    h = np.where(mx == g, (b - r) / d + 2, h)
    h = np.where(mx == b, (r - g) / d + 4, h)
    h = (h * 60) % 360
    return h, d / (mx + 1e-9), mx

def m_green(a):
    """Lime / chartreuse upholstery. Hue band 47-85 deg is lighting-invariant
    and sits just above the warm window/wood/floor yellows (~35-50 deg)."""
    h, s, v = _hsv(a)
    return ((h >= 47) & (h <= 85) & (s >= 0.50) & (v >= 0.18)).astype(np.float32)

def m_red(a):
    """Red drapes + terracotta papasan via true-red hue band (340-360/0-18 deg).
    Excludes the orange window blinds (~27 deg) and warm wood/floor."""
    h, s, v = _hsv(a)
    red_hue = (h >= 340) | (h <= 18)
    return (red_hue & (s >= 0.40) & (v >= 0.10) & (v <= 0.94)).astype(np.float32)

def m_yellow(a):
    """Yellow bed sheets -> hotel white."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return ((r > 150) & (g > 150) & (b < g - 22) & (np.abs(r - g) < 48)
            ).astype(np.float32)

def remap_luma(rgb, region_mask, shadow, highlight, lo_pct=8, hi_pct=92):
    """Replace masked pixels with new material, preserving luminance variation."""
    out = rgb.copy()
    L = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2])
    sel = region_mask > 0.04
    if sel.sum() < 30:
        return out, np.zeros(rgb.shape[:2], np.float32)
    lo = np.percentile(L[sel], lo_pct)
    hi = np.percentile(L[sel], hi_pct)
    if hi - lo < 1:
        hi = lo + 1
    t = np.clip((L - lo) / (hi - lo), 0, 1)[..., None]
    shadow = np.array(shadow, np.float32)
    highlight = np.array(highlight, np.float32)
    new = shadow + t * (highlight - shadow)
    alpha = feather(region_mask)[..., None]
    out = out * (1 - alpha) + new * alpha
    return out, alpha[..., 0]

def listing_tone(img):
    """Gentle warm + bright + clean pass that real-estate photos get."""
    img = ImageEnhance.Brightness(img).enhance(1.07)
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(1.0)
    arr = np.asarray(img, np.float32)
    arr[..., 0] = np.clip(arr[..., 0] * 1.035 + 3, 0, 255)   # warm: lift red
    arr[..., 2] = np.clip(arr[..., 2] * 0.972, 0, 255)        # cut blue cast
    img = Image.fromarray(arr.astype(np.uint8), "RGB")
    img = ImageEnhance.Sharpness(img).enhance(1.15)
    return img

def process(infile, outfile, passes):
    im = Image.open(f"{ORIG}/{infile}").convert("RGB")
    rgb = np.asarray(im, np.float32)
    a0 = np.asarray(im).astype(int)            # detect on the ORIGINAL pixels
    touched = np.zeros(rgb.shape[:2], np.float32)
    for detector, (shadow, highlight) in passes:
        m = open_mask(detector(a0))            # drop small specks
        m = np.maximum(m - touched, 0)         # don't re-touch changed pixels
        rgb, a = remap_luma(rgb, m, shadow, highlight)
        touched = np.clip(touched + a, 0, 1)
    out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")
    out = listing_tone(out)
    out.save(f"{OUT}/{outfile}", quality=92)
    print(f"  -> {outfile}  (changed pixels ~{int((touched>0.1).mean()*100)}%)")

JOBS = {
    "reno_living.jpg": [
        (m_red,    LINEN_DRAPE),   # red curtain, right
        (m_green,  TAUPE_FABRIC),  # lime green accent chair
    ],
    "reno_seating.jpg": [
        (m_red,    LINEN_DRAPE),   # tall red curtains
        (m_green,  TAUPE_FABRIC),  # two lime green chairs
    ],
    "reno_lounge.jpg": [
        (m_red,    GREIGE_SOFT),   # red papasan cushion
        (m_green,  TAUPE_FABRIC),  # lime chairs
    ],
    "reno_bedroom.jpg": [
        (m_red,    LINEN_DRAPE),   # red curtains
        (m_yellow, WHITE_LINEN),   # yellow bedding -> hotel white
    ],
}

SRC = {
    "reno_living.jpg":  "343edbc6-1000001675.jpg",
    "reno_seating.jpg": "1f5ccd77-1000001677.jpg",
    "reno_lounge.jpg":  "e7c670e2-1000001676.jpg",
    "reno_bedroom.jpg": "86bb0ced-1000001681.jpg",
}

if __name__ == "__main__":
    for out, passes in JOBS.items():
        print(f"Processing {out} from {SRC[out]}")
        process(SRC[out], out, passes)
    print("Done.")
