# Manual Automatic Map Production

This is the concise master manual for turning coordinate data into publication-ready maps.

## Use This When

- You have CSV, GeoJSON, VRT, or GeoPackage coordinate data
- You need BIG / PALAPA-ready outputs
- You need PNG, PDF, SVG, metadata, and a reusable QGIS project
- You want SOPD teams to follow one consistent workflow

## Core Rules

- Base map: `kabupaten`, `kecamatan`, `desa`
- Prefer GeoPackage over shapefile
- Keep thematic data separate from the base map
- Use a sector profile from `shared/config/sector_profiles.json`
- Warn users that same-named outputs will be overwritten

## Minimal Steps

1. Put source data in `projects/<project>/data/`.
2. Create or update the project GeoPackage at `projects/<project>/data/<project>.gpkg`.
3. Generate metadata.
4. Render the map.
5. Check outputs in `projects/<project>/output/`.

## Commands

### Generate metadata

```bash
python3 shared/scripts/generate_big_metadata.py \
  --template shared/metadata/batas_admin_metadata.xml \
  --output projects/<project>/metadata/<dataset>_metadata.xml \
  --title "<Title>" \
  --abstract "<Abstract>" \
  --source "<Source>" \
  --bbox "xmin,ymin,xmax,ymax"
```

### Render maps

```bash
python3 shared/scripts/generate_professional_map.py \
  --project projects/<project> \
  --sector <sector-name> \
  --layers <thematic-layer> \
  --output-format png,pdf,svg \
  --dpi 300
```

## Outputs

- `output/*.png`
- `output/*.pdf`
- `output/*.svg`
- `qgis/*.qgs`

## Recommended Sector Profiles

- `admin`
- `health`
- `infrastructure`
- `education`
- `public_works`
- `agriculture`

## Metadata Must Include

- UUID file identifier
- `gmd:metadataExtensionInfo`
- `gmd:useLimitation`
- lineage
- source description
- contact information

## License

This repository is licensed under the **AW Non-Commercial License 1.0**.
Commercial use requires prior written permission.
