#!/usr/bin/env python3
"""
compress_images.py: compresses images while preserving EXIF/GPS metadata.

Usage:
    python compress_images.py <input_dir> [output_dir] [--quality N] [--max-size WxH]

Arguments:
    input_dir       Directory of source images.
    output_dir      Where to write compressed images (default: <input_dir>_compressed).
    --quality N     JPEG quality 1-95 (default: 60).
    --max-size WxH  Max resolution, e.g. 2048x1365 (default: no resize).
"""

import argparse
import os
import sys
from pathlib import Path
from PIL import Image

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif"}


def compress_image(src: Path, dst: Path, quality: int, max_size: tuple | None):
    img = Image.open(src)

    # Pull raw EXIF bytes before any conversion
    exif_bytes = None
    if "exif" in img.info:
        exif_bytes = img.info["exif"]

    # Ensure RGB for JPEG output
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    if max_size:
        img.thumbnail(max_size, Image.LANCZOS)

    save_kwargs = {"quality": quality, "optimize": True}
    if exif_bytes:
        save_kwargs["exif"] = exif_bytes

    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst.with_suffix(".jpg"), "JPEG", **save_kwargs)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path, nargs="?")
    parser.add_argument("--quality", type=int, default=60)
    parser.add_argument("--max-size", type=str, default=None, help="e.g. 2048x1365")
    args = parser.parse_args()

    if not args.input_dir.is_dir():
        print(f"Error: '{args.input_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output_dir or args.input_dir.parent / (args.input_dir.name + "_compressed")

    max_size = None
    if args.max_size:
        w, h = args.max_size.lower().split("x")
        max_size = (int(w), int(h))

    images = sorted(p for p in args.input_dir.iterdir() if p.suffix.lower() in SUPPORTED_EXTENSIONS)
    if not images:
        print(f"No supported images found in '{args.input_dir}'.", file=sys.stderr)
        sys.exit(1)

    print(f"Compressing {len(images)} images -> '{output_dir}' (quality={args.quality}" +
          (f", max-size={args.max_size}" if max_size else "") + ")")

    total_in = total_out = 0
    for src in images:
        dst = output_dir / src.name
        compress_image(src, dst.with_suffix(".jpg"), args.quality, max_size)
        size_in = src.stat().st_size
        size_out = dst.with_suffix(".jpg").stat().st_size
        total_in += size_in
        total_out += size_out
        ratio = (1 - size_out / size_in) * 100
        print(f"  {src.name}: {size_in/1e6:.1f}MB -> {size_out/1e6:.1f}MB ({ratio:.0f}% smaller)")

    print(f"\nTotal: {total_in/1e6:.0f}MB -> {total_out/1e6:.0f}MB ({(1-total_out/total_in)*100:.0f}% reduction)")


if __name__ == "__main__":
    main()
