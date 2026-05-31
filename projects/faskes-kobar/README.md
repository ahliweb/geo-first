# Faskes Kotawaringin Barat (`awcms-geospatial` sample)

Health facility map project for the `awcms-geospatial` plugin.

For the quick start, see `../../docs/guides/sopd-quick-start.md`.
For the master manual, see `../../docs/guides/manual-automatic-map-production.md`.
For plugin rules, see `../../docs/guides/awcms-geospatial-plugin.md`.

## Project Structure

```
faskes-kobar/
├── data/              # Source data (CSV, GPKG, etc.)
├── shapefiles/        # Exported shapefiles (faskes.shp)
├── scripts/           # Project-specific processing scripts
├── metadata/          # ISO 19139 XML metadata
├── qgis/              # QGIS project files
├── styles/            # QML style files
├── output/            # PNG/SVG/PDF exports
└── README.md          # This file
```

## Data Sources

- **Project GeoPackage**: `data/faskes_kobar.gpkg` — contains `kabupaten`, `kecamatan`, `desa` (94 villages), and `faskes` (10 points)
- **Example data**: `data/faskes_contoh.csv` — 10 sample health facility points
- **Shapefile**: `shapefiles/faskes.shp` — derived from CSV via VRT for interchange/legacy use
- **Base map**: `kabupaten`, `kecamatan`, and `desa` are the cartographic base layers

## Generate Maps

```bash
python3 ../../shared/scripts/generate_professional_map.py \
  --project projects/faskes-kobar \
  --sector health \
  --layers faskes \
  --output-format png,pdf,svg \
  --dpi 300
```

## Output Files

- `output/peta_faskes_kobar.png` — 300 DPI raster map
- `output/peta_faskes_kobar.pdf` — vector PDF for print
- `output/peta_faskes_kobar.svg` — vector SVG for editing
- `qgis/peta_faskes_kobar.qgs` — reusable QGIS project with relative datasource paths
- `output/faskes_summary.csv` — quick summary by kecamatan
- `data/faskes_kobar.gpkg` — self-contained project GeoPackage for reuse

Warning: if these filenames already exist, new runs will overwrite them.

## Base Map Convention

All exports use the village/sub-district administrative boundary map as the cartographic base:
- `kabupaten`
- `kecamatan`
- `desa`

Thematic layers are rendered on top of this base map.

If a filename already exists in `output/`, the next export replaces it.

## License

This project is licensed under the **AW Non-Commercial License 1.0**.
See [../../LICENSE.md](../../LICENSE.md) for the full legal text.

For commercial licensing inquiries, contact: [commercial@ahliweb.com](mailto:commercial@ahliweb.com)
