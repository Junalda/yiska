#!/usr/bin/env python3
"""
Yiska Cleaning VOF — logo build pipeline.

Maakt van het aangeleverde JPG-logo (witte achtergrond) een set web-klare,
transparante PNG's + favicons, met randbehoud van witte details BINNEN het logo.

Gebruik:
    python3 tools/build_logo.py pad/naar/logo.jpg
    python3 tools/build_logo.py pad/naar/logo.jpg --outdir assets/images

Output (in --outdir, standaard assets/images):
    logo.png            transparant, bijgesneden op de inhoud, web-geoptimaliseerd
    logo-512.png        512x512, transparant, gecentreerd
    logo-1024.png       1024x1024, transparant, gecentreerd
    apple-touch-icon.png 180x180, op navy achtergrond (iOS-vriendelijk)
    favicon.ico         multi-size (16/32/48), transparant

Achtergrondverwijdering: alleen near-witte pixels die VIA DE RAND met elkaar
verbonden zijn worden transparant gemaakt (connected components). Witte wolkjes,
sparkles en de witte "Yiska"-letters binnen het logo blijven dus behouden.
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

NAVY = (6, 34, 61, 255)  # #06223d — huisstijl, voor de apple-touch-icon


def remove_background(im: Image.Image, white_thresh: int = 236, feather: float = 0.8) -> Image.Image:
    """Maak de buitenste (rand-verbonden) witte achtergrond transparant."""
    im = im.convert("RGBA")
    arr = np.asarray(im).astype(np.int16)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]

    # near-wit = alle kanalen hoog én weinig kleurverschil (lage saturatie)
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    near_white = (mn >= white_thresh) & ((mx - mn) <= 16)

    # connected components op de near-white-mask
    labels, n = ndimage.label(near_white)
    if n > 0:
        border = np.concatenate([
            labels[0, :], labels[-1, :], labels[:, 0], labels[:, -1]
        ])
        bg_labels = np.unique(border)
        bg_labels = bg_labels[bg_labels != 0]
        background = np.isin(labels, bg_labels)
    else:
        background = np.zeros(near_white.shape, dtype=bool)

    alpha = np.where(background, 0, 255).astype(np.uint8)
    out = arr.astype(np.uint8).copy()
    out[..., 3] = alpha
    result = Image.fromarray(out, "RGBA")

    # randverbetering: alpha 1px krimpen (haalt witte halo weg) + zacht feather
    a = result.getchannel("A")
    a = a.filter(ImageFilter.MinFilter(3))          # erodeer 1px -> geen witte rand
    if feather:
        a = a.filter(ImageFilter.GaussianBlur(feather))  # anti-alias de rand
    result.putalpha(a)
    return result


def trim(im: Image.Image, pad_ratio: float = 0.04) -> Image.Image:
    """Snijd bij op de zichtbare inhoud (alpha-bbox) met wat marge."""
    bbox = im.getchannel("A").getbbox()
    if not bbox:
        return im
    im = im.crop(bbox)
    pad = int(max(im.size) * pad_ratio)
    if pad:
        canvas = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
        canvas.paste(im, (pad, pad), im)
        im = canvas
    return im


def square(im: Image.Image, size: int, bg=(0, 0, 0, 0)) -> Image.Image:
    """Plaats het logo gecentreerd op een vierkant canvas van size x size."""
    src = im.copy()
    src.thumbnail((size, size), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), bg)
    canvas.paste(src, ((size - src.width) // 2, (size - src.height) // 2), src)
    return canvas


def save_png(im: Image.Image, path: str):
    im.save(path, "PNG", optimize=True)
    print(f"  ✓ {path}  ({im.width}x{im.height})")


def main():
    ap = argparse.ArgumentParser(description="Bouw web-klare Yiska-logo-assets.")
    ap.add_argument("source", help="pad naar het bron-logo (JPG/PNG)")
    ap.add_argument("--outdir", default="assets/images", help="uitvoermap")
    ap.add_argument("--max", type=int, default=1024, help="max breedte voor logo.png")
    args = ap.parse_args()

    if not os.path.isfile(args.source):
        sys.exit(f"Bronbestand niet gevonden: {args.source}")
    os.makedirs(args.outdir, exist_ok=True)

    print(f"Bron: {args.source}")
    im = Image.open(args.source)
    cut = trim(remove_background(im))

    # 1) logo.png — transparant, bijgesneden, geoptimaliseerd (max breedte)
    main_logo = cut.copy()
    if main_logo.width > args.max:
        h = round(main_logo.height * args.max / main_logo.width)
        main_logo = main_logo.resize((args.max, h), Image.LANCZOS)
    save_png(main_logo, os.path.join(args.outdir, "logo.png"))

    # 2) vierkante transparante varianten
    save_png(square(cut, 512), os.path.join(args.outdir, "logo-512.png"))
    save_png(square(cut, 1024), os.path.join(args.outdir, "logo-1024.png"))

    # 3) apple-touch-icon — op navy, volledig dekkend (nette iOS-tegel)
    apple = square(cut, 180, bg=NAVY).convert("RGB")
    apple_path = os.path.join(args.outdir, "apple-touch-icon.png")
    apple.save(apple_path, "PNG", optimize=True)
    print(f"  ✓ {apple_path}  (180x180, dekkend)")

    # 4) favicon.ico — multi-size, transparant
    ico = square(cut, 64)
    ico_path = os.path.join(args.outdir, "favicon.ico")
    ico.save(ico_path, sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"  ✓ {ico_path}  (16/32/48)")

    print("Klaar. Alle logo-assets staan in:", args.outdir)


if __name__ == "__main__":
    main()
