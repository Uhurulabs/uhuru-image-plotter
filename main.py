#!/usr/bin/env python3
"""
uhuru-image-plotter: reads GPS EXIF data from images and writes a KML file.

Usage:
    python main.py <image_dir> [output.kml]

Arguments:
    image_dir   Directory containing JPEG/PNG images with GPS EXIF data.
    output.kml  Output KML file path (default: output.kml).
"""

import os
import sys
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif"}


def get_gps_info(exif_data: dict) -> dict | None:
    """Extract the GPSInfo block from raw EXIF data."""
    for tag_id, value in exif_data.items():
        if TAGS.get(tag_id) == "GPSInfo":
            return {GPSTAGS.get(k, k): v for k, v in value.items()}
    return None


def dms_to_decimal(dms: tuple, ref: str) -> float:
    """Convert degrees/minutes/seconds + hemisphere ref to decimal degrees."""
    degrees, minutes, seconds = dms
    decimal = degrees + minutes / 60 + seconds / 3600
    if ref in ("S", "W"):
        decimal = -decimal
    return decimal


def extract_coords(image_path: Path) -> tuple[float, float, float] | None:
    """
    Return (latitude, longitude, altitude_m) for an image, or None if no GPS.
    """
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if not exif_data:
            return None
        gps = get_gps_info(exif_data)
        if not gps:
            return None

        lat = dms_to_decimal(gps["GPSLatitude"], gps.get("GPSLatitudeRef", "N"))
        lon = dms_to_decimal(gps["GPSLongitude"], gps.get("GPSLongitudeRef", "E"))
        alt = float(gps.get("GPSAltitude", 0))
        # AltitudeRef: 0 = above sea level, 1 = below
        if gps.get("GPSAltitudeRef") == b"\x01":
            alt = -alt

        return lat, lon, alt
    except Exception as e:
        print(f"  Warning: could not read {image_path.name}: {e}", file=sys.stderr)
        return None


def build_kml(points: list[tuple[str, float, float, float]]) -> str:
    """Build a KML string from a list of (name, lat, lon, alt) tuples."""
    placemarks = []
    for name, lat, lon, alt in points:
        placemarks.append(
            f"""    <Placemark>
      <name>{name}</name>
      <Point>
        <altitudeMode>absolute</altitudeMode>
        <coordinates>{lon},{lat},{alt}</coordinates>
      </Point>
    </Placemark>"""
        )

    body = "\n".join(placemarks)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Image Locations</name>
{body}
  </Document>
</kml>
"""


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    image_dir = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("output.kml")

    if not image_dir.is_dir():
        print(f"Error: '{image_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    image_files = sorted(
        p for p in image_dir.iterdir() if p.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not image_files:
        print(f"No supported images found in '{image_dir}'.", file=sys.stderr)
        sys.exit(1)

    print(f"Processing {len(image_files)} images...")

    points = []
    skipped = 0
    for img_path in image_files:
        coords = extract_coords(img_path)
        if coords is None:
            skipped += 1
            continue
        lat, lon, alt = coords
        points.append((img_path.name, lat, lon, alt))
        print(f"  {img_path.name}: {lat:.6f}, {lon:.6f}, {alt:.1f}m")

    if not points:
        print("No GPS data found in any image.", file=sys.stderr)
        sys.exit(1)

    kml = build_kml(points)
    output_path.write_text(kml, encoding="utf-8")

    print(f"\nWrote {len(points)} placemarks to '{output_path}'.")
    if skipped:
        print(f"Skipped {skipped} image(s) with no GPS data.")


if __name__ == "__main__":
    main()
