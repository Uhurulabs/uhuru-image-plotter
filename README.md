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
./get-locations-from-images <image_dir> [output.kml]
```

| Argument | Description |
|---|---|
| `image_dir` | Directory containing images with GPS EXIF data |
| `output.kml` | Output file path (default: `output.kml`) |

**Example:**
```bash
./get-locations-from-images ./sample_images flight.kml
```

**Example output:**
```
Processing 10 images...
  DJI_0001.jpg: -1.234567, 36.812345, 42.5m
  DJI_0002.jpg: -1.234612, 36.812401, 43.1m
  ...

Wrote 10 placemarks to 'flight.kml'.
```

Open `flight.kml` in **Google Earth**, **QGIS**, or any KML-compatible GIS tool to visualise the flight path.

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

> Note: PNG and TIFF inputs are converted to JPEG on compression.

---

## Output

The generated KML file contains one `<Placemark>` per image with:
- The image filename as the placemark name
- Coordinates in `lon, lat, alt` order per the KML spec
- Altitude mode set to `absolute`

---

## License

MIT — see [LICENSE](LICENSE).

## Origin

Folded from `Uhurulabs/uhuru-image-plotter` on 2026-04-25. Sample images from
the original repo (~25 MB of DJI test fixtures) were not folded; drop your
own images into a directory and point the script at it. The original repo
has been archived; future changes happen here.
