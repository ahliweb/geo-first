# {{project-name}} (`awcms-geospatialTemplate`)

Geospatial map project scaffold for the `awcms-geospatialTemplate` template.

For the quick start, see `../../docs/guides/sopd-quick-start.md`.
For the master manual, see `../../docs/guides/manual-automatic-map-production.md`.
For plugin rules, see `../../docs/guides/awcms-geospatial-plugin.md`.

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
python3 ../../shared/scripts/generate_professional_map.py
```

## Base Map Convention

Use `kabupaten`, `kecamatan`, and `desa` as the default map base for BIG-compliant output.

The generator also writes a reusable QGIS project into `qgis/` with relative datasource paths.

If your project includes an integrated GeoPackage, keep it in `data/` and name it after the project.

If an output filename already exists, the next export replaces it.

For automatic coordinate-based workflows, follow `../../docs/guides/sopd-quick-start.md` and `../../docs/guides/manual-automatic-map-production.md`.

## License

This project is licensed under the **AW Non-Commercial License 1.0**.
See [../../LICENSE.md](../../LICENSE.md) for the full legal text.

For commercial licensing inquiries, contact: [commercial@ahliweb.com](mailto:commercial@ahliweb.com)
