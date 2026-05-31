# SOPD Quick Start

Use this one-page workflow when you need to create a map from coordinate data fast.

For the master manual, see `docs/guides/manual-automatic-map-production.md`.

If you need a print-ready reference, the master manual is formatted for PDF export.

## What You Need

- CSV, GeoJSON, VRT, or GeoPackage with coordinate fields
- Descriptive fields such as `nama`, `kategori`, and optional `alamat`, `kecamatan`, `desa`
- A sector choice from `shared/config/sector_profiles.json`

## Default Map Base

Always use these as the base map:
- `kabupaten`
- `kecamatan`
- `desa`

## Fast Workflow

Before you start, run `bash scripts/setup-awcms-geospatial.sh` once after clone to create a local `.env`.

1. Put your source data into `projects/<project-name>/data/`.
2. If needed, convert coordinate CSV to point data using VRT or `ogr2ogr`.
3. Build or update `projects/<project-name>/data/<project-name>.gpkg`.
4. Generate metadata:

```bash
python3 shared/scripts/generate_big_metadata.py \
  --template shared/metadata/batas_admin_metadata.xml \
  --output projects/<project-name>/metadata/<dataset>_metadata.xml \
  --title "<Judul Peta>" \
  --abstract "<Deskripsi dataset>" \
  --source "<Sumber data>" \
  --bbox "xmin,ymin,xmax,ymax"
```

5. Render the map:

```bash
python3 shared/scripts/generate_professional_map.py

# Or override the defaults explicitly:
python3 shared/scripts/generate_professional_map.py \
  --project projects/<project-name> \
  --sector <sector-name> \
  --layers <thematic-layer> \
  --output-format png,pdf,svg \
  --dpi 300
```

6. Review the outputs in `projects/<project-name>/output/`.

## Output Rule

If a file with the same name already exists, the next export will replace it.

Current repository state: `projects/faskes-kobar/data/faskes_kobar.gpkg` is the self-contained example package with `kabupaten`, `kecamatan`, `desa`, and `faskes`.

## Best Practice

- Prefer GeoPackage over shapefile.
- Keep thematic layers separate from the base map.
- Save the reusable QGIS project in `projects/<project-name>/qgis/`.
- Include ISO 19139 metadata before upload.

## Common Sector Profiles

- `admin`
- `health`
- `infrastructure`
- `education`
- `public_works`
- `agriculture`

## License

This repository is licensed under the **AW Non-Commercial License 1.0**.
Commercial use requires prior written permission.
