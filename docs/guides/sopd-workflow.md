# SOPD Workflow Guide

This guide defines a consistent workflow for SOPDs that need to produce sector maps while staying aligned with BIG / PALAPA expectations.

For a fast operator-facing version, see `docs/guides/sopd-quick-start.md`.
For the master manual, see `docs/guides/manual-automatic-map-production.md`.

## Core Rules

- Use `kabupaten`, `kecamatan`, and `desa` as the base map.
- Keep thematic data in separate layers.
- Generate PNG, PDF, and SVG for every publication map.
- Write metadata before publication.
- Keep all outputs in `projects/<project-name>/output/`.
- If an output filename already exists, the generator will overwrite it.
- Keep the project GeoPackage in `projects/<project-name>/data/<project-name>.gpkg` when possible.

The generator prefers the project GeoPackage over shapefiles when both exist.

## Sector Profiles

Use `shared/config/sector_profiles.json` to select a sector profile:
- `admin`
- `health`
- `infrastructure`
- `education`
- `public_works`
- `agriculture`

## Typical Flow

1. Create a new project from `projects/_template/`.
2. Add sector data into `projects/<project>/data/` and `shapefiles/` if needed, but prefer the GeoPackage workflow.
3. Generate metadata with `shared/scripts/generate_big_metadata.py`.
4. Render maps with `shared/scripts/generate_professional_map.py`.
5. Export PNG, PDF, and SVG.
6. Validate XML and file paths before upload.

## Example

```bash
python3 shared/scripts/generate_professional_map.py \
  --project projects/faskes-kobar \
  --sector health \
  --layers faskes \
  --output-format png,pdf,svg \
  --dpi 300
```

## License

This repository is licensed under the **AW Non-Commercial License 1.0**.
Commercial use requires prior written permission.
