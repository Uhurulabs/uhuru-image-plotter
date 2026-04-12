# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this does

Reads GPS EXIF data from drone/camera images and produces a KML file with one placemark per image. A companion script compresses images while preserving EXIF metadata.

## Setup

```bash
pip install -r requirements.txt   # Pillow>=10.0.0
```

## Running the scripts

```bash
# Convert images to KML
python main.py <image_dir> [output.kml]

# Compress images (preserves GPS EXIF)
python compress_images.py <input_dir> [output_dir] [--quality 60] [--max-size 2048x1365]
```

## Architecture

Both scripts are single-file, dependency-free beyond Pillow. The pipeline in `main.py`:

1. `extract_coords` opens each image via Pillow, calls `img._getexif()` to get raw EXIF, then `get_gps_info` to pull the `GPSInfo` tag block.
2. `dms_to_decimal` converts degrees/minutes/seconds tuples + hemisphere reference (`N/S/E/W`) to signed decimal degrees. Altitude sign is determined by `GPSAltitudeRef` (`b"\x01"` = below sea level).
3. `build_kml` assembles the KML string with `<altitudeMode>absolute</altitudeMode>` — coordinates are ordered `lon,lat,alt` per KML spec.

`compress_images.py` extracts raw EXIF bytes (`img.info["exif"]`) before any conversion and passes them back to `img.save()` so GPS data survives compression.

Supported formats: `.jpg`, `.jpeg`, `.png`, `.tiff`, `.tif` (defined in `SUPPORTED_EXTENSIONS` in both files).
