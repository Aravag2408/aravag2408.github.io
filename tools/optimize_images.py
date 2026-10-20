"""Resize an image and save it as WebP under 250 KB.

Usage: python tools/optimize_images.py SRC DEST.webp [--width N] [--crop L,T,R,B]
"""
import argparse
import io
from pathlib import Path

from PIL import Image

MAX_BYTES = 250 * 1024


def optimize(src, dest, width=1600, crop=None):
    img = Image.open(src).convert("RGB")
    if crop:
        img = img.crop(crop)
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    for quality in range(80, 20, -5):
        buf = io.BytesIO()
        img.save(buf, "WEBP", quality=quality, method=6)
        if buf.tell() <= MAX_BYTES:
            break
    Path(dest).write_bytes(buf.getvalue())
    return img.size, quality, buf.tell()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dest")
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--crop", type=lambda s: tuple(int(v) for v in s.split(",")))
    a = ap.parse_args()
    size, q, n = optimize(a.src, a.dest, a.width, a.crop)
    print(f"{a.dest}: {size[0]}x{size[1]} q{q} {n // 1024} KB")
