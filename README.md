# uhuru-image-plotter

Reads GPS EXIF data from drone/camera images and produces a KML file with one placemark per image. Includes a companion script to compress images while preserving GPS metadata.

---

## Features

- Extracts GPS coordinates (latitude, longitude, altitude) from image EXIF data
- Outputs a standards-compliant KML file ready for Google Earth, QGIS, or any KML viewer
- Supports JPEG, PNG, and TIFF formats
- Companion compression script shrinks images while keeping GPS EXIF intact

---

## Setup

```bash
pip install -r requirements.txt
```

**Requirement:** Python 3.10+ and Pillow ≥ 10.0.0

---

## Usage

### Generate a KML from images

```bash
python main.py <image_dir> [output.kml]
```

| Argument | Description |
|---|---|
| `image_dir` | Directory containing images with GPS EXIF data |
| `output.kml` | Output file path (default: `output.kml`) |

**Example:**
```bash
python main.py ./sample_images flight.kml
```

---

### Compress images (preserving GPS EXIF)

```bash
python compress_images.py <input_dir> [output_dir] [--quality N] [--max-size WxH]
```

| Argument | Description |
|---|---|
| `input_dir` | Directory of source images |
| `output_dir` | Destination directory (default: `<input_dir>_compressed`) |
| `--quality N` | JPEG quality 1–95 (default: `60`) |
| `--max-size WxH` | Max resolution, e.g. `2048x1365` (default: no resize) |

**Example:**
```bash
python compress_images.py ./sample_images ./compressed --quality 75 --max-size 2048x1365
```

---

## Supported Formats

`.jpg` · `.jpeg` · `.png` · `.tiff` · `.tif`

---

## Output

The generated KML file contains one `<Placemark>` per image with:
- The image filename as the placemark name
- Coordinates in `lon, lat, alt` order per the KML spec
- Altitude mode set to `absolute`

Open the `.kml` file in **Google Earth**, **QGIS**, or any compatible GIS tool to visualize the flight path.
