#!/usr/bin/env python3
"""
Yiska Cleaning VOF — premium tijdelijke placeholder-afbeeldingen.

Genereert hoogwaardige, on-brand placeholder-JPG's (geen cartoons, geen stock,
geen lege vlakken). Naast de huisstijl-gradient en architectuur-/glasmotieven
krijgen ze nu een fotografische afwerking:
  • dieptescherpte (depth-of-field): zachte focus-afval naar de randen
  • fijne film-/duotone-textuur voor een organische, niet-vlakke uitstraling
  • vignet + korrel
Bestandsgroottes zijn geoptimaliseerd (progressive JPEG).

    python3 tools/make_placeholders.py
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = "assets/images"

# Huisstijlkleuren
NAVY = (6, 34, 61)
NAVY2 = (10, 44, 77)
BLUE = (21, 119, 194)
BLUE2 = (31, 138, 224)
CYAN = (120, 196, 244)
GREEN = (67, 173, 70)
GREEN2 = (95, 200, 95)
STEEL = (34, 62, 92)


# ---------- achtergrond / licht ----------
def grad(w, h, top, bot, t_dir="diag"):
    ys = np.linspace(0, 1, h)[:, None]
    xs = np.linspace(0, 1, w)[None, :]
    if t_dir == "diag":
        t = (xs + ys) / 2
    elif t_dir == "v":
        t = np.repeat(ys, w, axis=1)
    else:
        t = np.repeat(xs, h, axis=0)
    t = t[..., None]
    return np.array(top)[None, None, :] * (1 - t) + np.array(bot)[None, None, :] * t


def glow(arr, center, color, sigma, strength=1.0):
    h, w, _ = arr.shape
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = center[0] * w, center[1] * h
    d2 = (xx - cx) ** 2 + (yy - cy) ** 2
    g = np.exp(-d2 / (2 * (sigma * max(w, h)) ** 2))[..., None] * strength
    return arr + (255 - arr) * (g * (np.array(color)[None, None, :] / 255.0))


def base_image(w, h, top, bot, glow_center, glow_color, glow_sigma=0.5, glow_str=0.9):
    return glow(grad(w, h, top, bot), glow_center, glow_color, glow_sigma, glow_str)


# ---------- fotografische afwerking ----------
def fractal(w, h, seed, octaves=5):
    """Zachte fractale ruis (0..1) — wolk-/lichtachtige textuur."""
    acc = np.zeros((h, w))
    amp, total = 1.0, 0.0
    rng = np.random.default_rng(seed)
    for o in range(octaves):
        cells = 3 * (2 ** o)
        small = (rng.random((cells, cells)) * 255).astype(np.uint8)
        up = np.asarray(Image.fromarray(small).resize((w, h), Image.BICUBIC)) / 255.0
        acc += amp * up
        total += amp
        amp *= 0.55
    return acc / total


def photo_texture(arr, seed, strength=0.12, tint=BLUE2):
    """Fijne duotone/film-textuur: organische licht-donkervariatie + lichte tint."""
    h, w, _ = arr.shape
    fr = fractal(w, h, seed)
    t = (fr - fr.mean())[..., None]
    arr = arr * (1 + strength * t)                      # luminantie-modulatie
    arr = arr + (np.array(tint)[None, None, :] - arr) * (np.clip(t, 0, None) * 0.06)
    return arr


def depth_of_field(img, focal=(0.5, 0.45), radius=7, focus_sigma=0.42):
    """Zachte dieptescherpte: scherp rond het focuspunt, vervaagd naar de randen."""
    w, h = img.size
    blurred = img.filter(ImageFilter.GaussianBlur(radius))
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = focal[0] * w, focal[1] * h
    d2 = ((xx - cx) / w) ** 2 + ((yy - cy) / h) ** 2
    focus = np.exp(-d2 / (2 * focus_sigma ** 2))        # 1 = scherp, 0 = vervaagd
    mask = Image.fromarray((focus * 255).astype(np.uint8), "L")
    return Image.composite(img, blurred, mask)


def vignette(arr, amount=0.40):
    h, w, _ = arr.shape
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    v = np.clip(1 - amount * np.clip(d - 0.45, 0, 1.5), 0, 1)[..., None]
    return arr * v


def grain(arr, amount=5.0, seed=7):
    n = np.random.default_rng(seed).normal(0, amount, arr.shape[:2])[..., None]
    return arr + n


def finish(img, path, focal=(0.5, 0.45), seed=1, quality=80, dof=7, max_w=None):
    if max_w and img.size[0] > max_w:
        nh = round(img.size[1] * max_w / img.size[0])
        img = img.resize((max_w, nh), Image.LANCZOS)
    img = depth_of_field(img, focal=focal, radius=dof)         # dieptescherpte
    arr = np.asarray(img).astype(np.float64)
    arr = photo_texture(arr, seed=seed)                        # film/duotone-textuur
    arr = vignette(arr)
    arr = grain(arr, seed=seed)
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    Image.fromarray(arr, "RGB").save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    kb = os.path.getsize(path) // 1024
    print(f"  ✓ {path}  ({arr.shape[1]}x{arr.shape[0]}, {kb} KB)")


def pil(arr):
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def overlay(img, draw_fn, blur=0):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(ov), img.size)
    if blur:
        ov = ov.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")


# ---------- motieven ----------
def window_grid(d, size, cols, rows, color, lit=0.25, alpha=42, lit_alpha=120,
                x0=0.05, x1=0.95, y0=0.1, y1=0.95):
    w, h = size
    rng = np.random.default_rng(3)
    cw = (x1 - x0) * w / cols
    ch = (y1 - y0) * h / rows
    for i in range(cols):
        for j in range(rows):
            x = x0 * w + i * cw
            y = y0 * h + j * ch
            pad = cw * 0.10
            a = lit_alpha if rng.random() < lit else alpha
            d.rectangle([x + pad, y + pad, x + cw - pad, y + ch - pad], fill=color + (a,))


def skyline(d, size, color=(4, 22, 40), alpha=150):
    w, h = size
    rng = np.random.default_rng(11)
    x = -20
    while x < w + 20:
        bw = rng.integers(40, 110)
        bh = rng.integers(int(h * 0.18), int(h * 0.5))
        d.rectangle([x, h - bh, x + bw, h], fill=color + (alpha,))
        for vy in range(h - bh + 12, h - 10, 26):
            for vx in range(int(x) + 10, int(x + bw) - 8, 22):
                if rng.random() < 0.5:
                    d.rectangle([vx, vy, vx + 9, vy + 12], fill=CYAN + (60,))
        x += bw + rng.integers(6, 22)


def droplet(d, size, cx, cy, s, color, alpha=70):
    w, h = size
    x, y = cx * w, cy * h
    d.ellipse([x - s, y - s * 0.78, x + s, y + s * 1.0], fill=color + (alpha,))
    d.polygon([(x, y - s * 1.7), (x - s * 0.62, y - s * 0.2), (x + s * 0.62, y - s * 0.2)],
              fill=color + (alpha,))


def streak(img, p0, p1, width, color=(255, 255, 255), alpha=46, blur=22):
    def fn(d, sz):
        w, h = sz
        d.line([(p0[0] * w, p0[1] * h), (p1[0] * w, p1[1] * h)], fill=color + (alpha,), width=width)
    return overlay(img, fn, blur=blur)


# ---------- afbeeldingen ----------
def make_hero():
    w, h = 1760, 1100
    arr = base_image(w, h, NAVY, BLUE, (0.78, 0.28), BLUE2, 0.55, 1.0)
    arr = glow(arr, (0.12, 0.85), GREEN, 0.4, 0.5)
    img = pil(arr)
    img = overlay(img, lambda d, s: skyline(d, s))
    img = overlay(img, lambda d, s: window_grid(d, s, 9, 6, (200, 228, 250), x0=0.5, x1=0.98, y0=0.05, y1=0.8))
    img = overlay(img, lambda d, s: droplet(d, s, 0.30, 0.42, 140, CYAN, 60))
    img = streak(img, (0.45, 0.1), (0.7, 0.95), 120, alpha=40, blur=40)
    finish(img, f"{OUT}/hero-placeholder.jpg", focal=(0.72, 0.42), seed=21, quality=80, dof=8)


def make_office():
    w, h = 1600, 1067
    arr = base_image(w, h, NAVY2, BLUE, (0.7, 0.25), BLUE2, 0.5, 0.85)
    img = pil(arr)
    img = overlay(img, lambda d, s: window_grid(d, s, 4, 3, (210, 232, 252), lit=0.35, alpha=34, lit_alpha=120, x0=0.06, x1=0.94, y0=0.08, y1=0.92))

    def desks(d, s):
        ww, hh = s
        for x in np.linspace(0.1, 0.85, 4):
            d.rectangle([x * ww, hh * 0.74, x * ww + ww * 0.12, hh * 0.8], fill=(8, 26, 46, 150))
    img = overlay(img, desks)
    img = streak(img, (0.2, 0.0), (0.5, 1.0), 90, alpha=36, blur=34)
    finish(img, f"{OUT}/office-cleaning-placeholder.jpg", focal=(0.5, 0.4), seed=32, dof=6)


def make_glass():
    w, h = 1600, 1067
    arr = base_image(w, h, (12, 60, 104), CYAN, (0.5, 0.4), (170, 215, 250), 0.6, 0.7)
    img = pil(arr)
    img = overlay(img, lambda d, s: window_grid(d, s, 3, 2, (255, 255, 255), lit=0.0, alpha=30, x0=0.05, x1=0.95, y0=0.06, y1=0.94))

    def drops(d, s):
        ww, hh = s
        rng = np.random.default_rng(5)
        for _ in range(120):
            x, y = rng.random() * ww, rng.random() * hh
            r = rng.integers(2, 7)
            d.ellipse([x, y, x + r, y + r], fill=(255, 255, 255, 40))
    img = overlay(img, drops)
    img = streak(img, (0.1, 0.15), (0.85, 0.7), 150, alpha=70, blur=30)
    img = streak(img, (0.12, 0.2), (0.87, 0.75), 8, alpha=120, blur=4)
    finish(img, f"{OUT}/glass-cleaning-placeholder.jpg", focal=(0.5, 0.45), seed=43, dof=5)


def make_commercial():
    w, h = 1600, 1067
    arr = base_image(w, h, NAVY, STEEL, (0.25, 0.2), BLUE, 0.5, 0.7)
    arr = glow(arr, (0.85, 0.9), GREEN, 0.35, 0.45)
    img = pil(arr)

    def facades(d, s):
        ww, hh = s
        for x, bw, bh in [(0.05, 0.2, 0.8), (0.28, 0.16, 0.62), (0.47, 0.22, 0.92), (0.72, 0.18, 0.7), (0.9, 0.14, 0.5)]:
            d.rectangle([x * ww, hh * (1 - bh), (x + bw) * ww, hh], fill=(6, 24, 44, 120))
            window_grid(d, s, 4, int(bh * 14), (190, 222, 248), lit=0.3, alpha=26, lit_alpha=90,
                        x0=x, x1=x + bw, y0=1 - bh, y1=1.0)
    img = overlay(img, facades)
    finish(img, f"{OUT}/commercial-cleaning-placeholder.jpg", focal=(0.5, 0.5), seed=54, dof=6)


def make_about():
    w, h = 1600, 1067
    arr = base_image(w, h, (10, 50, 70), GREEN, (0.7, 0.7), GREEN2, 0.5, 0.55)
    arr = glow(arr, (0.25, 0.25), BLUE2, 0.45, 0.7)
    img = pil(arr)

    def circles(d, s):
        ww, hh = s
        for cx, cy, r in [(0.3, 0.55, 0.22), (0.5, 0.45, 0.26), (0.68, 0.6, 0.2)]:
            d.ellipse([(cx - r) * ww, (cy - r) * hh, (cx + r) * ww, (cy + r) * hh],
                      outline=(255, 255, 255, 70), width=3)
    img = overlay(img, circles)
    img = overlay(img, lambda d, s: droplet(d, s, 0.5, 0.42, 90, (255, 255, 255), 26))
    img = streak(img, (0.3, 0.0), (0.6, 1.0), 80, alpha=30, blur=36)
    finish(img, f"{OUT}/about-placeholder.jpg", focal=(0.5, 0.48), seed=65, dof=7)


def make_business():
    w, h = 1600, 1067
    arr = base_image(w, h, NAVY, BLUE, (0.8, 0.2), BLUE2, 0.5, 0.85)
    img = pil(arr)
    img = overlay(img, lambda d, s: skyline(d, s, color=(5, 24, 44), alpha=130))

    def bars(d, s):
        ww, hh = s
        for i, x in enumerate(np.linspace(0.12, 0.4, 5)):
            bh = 0.12 + i * 0.06
            d.rectangle([x * ww, hh * (0.7 - bh), x * ww + ww * 0.035, hh * 0.7], fill=GREEN2 + (150,))
    img = overlay(img, bars)
    img = overlay(img, lambda d, s: window_grid(d, s, 6, 5, (200, 228, 250), x0=0.55, x1=0.97, y0=0.1, y1=0.78))
    finish(img, f"{OUT}/business-placeholder.jpg", focal=(0.72, 0.4), seed=76, dof=6)


def make_contact():
    w, h = 1600, 900
    arr = base_image(w, h, (8, 40, 66), BLUE, (0.5, 0.35), BLUE2, 0.55, 0.8)
    arr = glow(arr, (0.5, 0.9), GREEN, 0.4, 0.4)
    img = pil(arr)

    def pin(d, s):
        ww, hh = s
        cx, cy, r = 0.5 * ww, 0.42 * hh, 0.12 * hh
        for rr, a in [(2.6, 26), (2.0, 34), (1.4, 50)]:
            d.ellipse([cx - r * rr, cy - r * rr, cx + r * rr, cy + r * rr], outline=(255, 255, 255, a), width=3)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 235))
        d.polygon([(cx - r * 0.7, cy + r * 0.5), (cx + r * 0.7, cy + r * 0.5), (cx, cy + r * 1.9)], fill=(255, 255, 255, 235))
        d.ellipse([cx - r * 0.36, cy - r * 0.36, cx + r * 0.36, cy + r * 0.36], fill=BLUE + (255,))
    img = overlay(img, pin)
    finish(img, f"{OUT}/contact-placeholder.jpg", focal=(0.5, 0.42), seed=87, dof=5)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("Premium placeholders genereren (fotografische afwerking)…")
    make_hero(); make_office(); make_glass(); make_commercial()
    make_about(); make_business(); make_contact()
    print("Klaar.")
