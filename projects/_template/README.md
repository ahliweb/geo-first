# {{project-name}}

Geospatial map project for Kotawaringin Barat Regency.

## Project Structure

```
{{project-name}}/
├── data/              # Source data (CSV, GPKG, etc.)
├── shapefiles/        # Exported shapefiles
├── scripts/           # Project-specific processing scripts
├── metadata/          # ISO 19139 XML metadata
├── qgis/              # QGIS project files
├── styles/            # QML style files
├── output/            # PNG/SVG/PDF exports
└── README.md          # This file
```

## Generate Maps

```bash
python3 ../../shared/scripts/generate_professional_map.py \
  --project projects/{{project-name}} \
  --sector admin \
  --layers my-layer \
  --output-format png,pdf,svg \
  --dpi 300
```

## Base Map Convention

Use `kabupaten`, `kecamatan`, and `desa` as the default map base for BIG-compliant output.

The generator also writes a reusable QGIS project into `qgis/` with relative datasource paths.

If your project includes an integrated GeoPackage, keep it in `data/` and name it after the project.

## License

This project is licensed under the **AW Non-Commercial License 1.0**.
See [../../LICENSE.md](../../LICENSE.md) for the full legal text.

For commercial licensing inquiries, contact: [commercial@ahliweb.com](mailto:commercial@ahliweb.com)
