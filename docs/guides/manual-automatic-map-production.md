# Manual Automatic Map Production

This is the master manual for turning coordinate data into publication-ready maps.

## Document Metadata

- Audience: SOPD operators, GIS staff, and community contributors
- Scope: automated map production from coordinate data
- Output types: PNG, PDF, SVG, QGIS project, ISO 19139 metadata
- Cartographic base: `kabupaten`, `kecamatan`, `desa`

## Use This When

- You have CSV, GeoJSON, VRT, or GeoPackage coordinate data
- You need BIG / PALAPA-ready outputs
- You need PNG, PDF, SVG, metadata, and a reusable QGIS project
- You want SOPD teams to follow one consistent workflow

## Fast Path

If you only need the shortest possible workflow, start here:
- `docs/guides/sopd-quick-start.md`

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

## Validation Checklist

- CSV or GeoJSON coordinates are valid
- `longitude` / `latitude` are populated and correct
- Base map layers are present
- Metadata XML parses successfully
- QGIS project uses relative paths
- Output files were created in `output/`
- Same-named outputs were intentionally overwritten

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
- `data/<project>.gpkg` when the project is packaged as a self-contained GeoPackage

## PDF / Print Export Note

This markdown file is intended to be print-friendly.

Rendered PDF artifact:
- `docs/guides/manual-automatic-map-production.pdf`

To generate a PDF version, use your preferred Markdown-to-PDF tool, for example:

```bash
pandoc docs/guides/manual-automatic-map-production.md -o manual-automatic-map-production.pdf
```

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

## Troubleshooting

- If a map looks empty, verify the input coordinates and CRS.
- If the base map is missing, confirm `kabupaten`, `kecamatan`, and `desa` exist in the project GeoPackage or shared shapefiles.
- If the wrong outputs appear, check for same-named files in `projects/<project>/output/`.
- If metadata fails to parse, validate the XML before upload.
- If the project is `faskes-kobar`, the rebuilt GeoPackage should contain 94 villages and 10 faskes points.

## License

This repository is licensed under the **AW Non-Commercial License 1.0**.
Commercial use requires prior written permission.
