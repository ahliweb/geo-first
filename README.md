# AWCMS Geospatial (`awcms-geospatial` / `awcms-geospatialTemplate`)

Independent geospatial plugin/template workspace for Kotawaringin Barat Regency, Central Kalimantan.

This repo stays independent while using AWCMS-Micro and EmDash as compatibility references.
See `docs/guides/awcms-geospatial-plugin.md` for the plugin/template rules.

For the quick start, see `docs/guides/sopd-quick-start.md`.
For the master manual, see `docs/guides/manual-automatic-map-production.md`.
PDF copy: `docs/guides/manual-automatic-map-production.pdf`

## Quick Start

### Bootstrap the Repository

```bash
bash scripts/setup-awcms-geospatial.sh
```

The setup script creates a local `.env` from `shared/config/awcms-geospatial.env.example` when needed.
The core scripts automatically load `.env` if it exists.

### Generate a Professional Map

```bash
# Using the shared script (recommended)
python3 shared/scripts/generate_professional_map.py
```

Warning: if output filenames already exist, they will be overwritten.

## Plugin Identity

- Plugin name: `awcms-geospatial`
- Template name: `awcms-geospatialTemplate`
- Use `shared/config/awcms-geospatial.env.example` as the canonical plugin config template.
- Use `shared/config/awcms-geospatialTemplate.env.example` for template-specific overrides.
- Legacy `GEOFIRST_*` env vars remain supported as fallback only.

## Upstream Snapshot

- Read-only upstream reference: `upstream/awcms-micro/`
- Refresh script: `scripts/sync-awcms-micro-upstream.sh`
- Snapshot sync marker: `upstream/awcms-micro/.upstream-commit`
- Treat the snapshot as vendor/reference material, not active geospatial source.

Typical inputs:
- CSV / GeoJSON / VRT / GeoPackage point data
- Base map layers: `kabupaten`, `kecamatan`, `desa`
- Sector profile from `shared/config/sector_profiles.json`

Typical outputs:
- PNG, PDF, SVG
- QGIS project file with relative paths
- ISO 19139 metadata XML
- Project GeoPackage when available (`projects/<name>/data/<name>.gpkg`)

### Create a New Project

```bash
# 1. Scaffold from template
cp -r projects/_template projects/my-new-project

# 2. Add your data to projects/my-new-project/data/

# 3. Generate maps
python3 shared/scripts/generate_professional_map.py \
  --project projects/my-new-project \
  --sector admin \
  --layers my-layer \
  --output-format png,pdf
```

Use the project GeoPackage when available. The generator will prefer `projects/<name>/data/<name>.gpkg` before shapefiles.

## Repository Structure

```
awcms-geospatial/
├── projects/                    # Isolated project workspaces
│   ├── faskes-kobar/           # Health facilities map project
│   │   └── output/             # Generated maps (PNG/PDF/SVG)
│   └── _template/              # Template for new projects
├── shared/                      # Cross-project shared resources
│   ├── data/                   # GeoPackage databases
│   ├── shapefiles/             # ESRI Shapefiles
│   ├── scripts/                # PyQGIS/GDAL utilities
│   ├── config/                 # Sector profiles and export settings
│   └── qgis/                   # Shared QGIS projects
├── docs/                        # Documentation
│   ├── examples/               # Sample datasets
│   └── guides/                 # Technical guides
├── AGENTS.md                    # AI agent guidelines
├── README.md                    # This file
├── LICENSE.md                   # AW Non-Commercial License 1.0
├── CHANGELOG.md                 # Version history
└── VERSION                      # Current version
```

## Technical Stack

- **GDAL/OGR**: 3.8.4
- **QGIS**: 3.34.4-Prizren
- **Python**: 3.x with `osgeo`, `qgis` modules
- **Projection**: EPSG:4326 (WGS 84)

## Standards Compliance

- **Metadata**: SNI ISO 19115-3:2019 (PALAPA/SIMPADU BIG)
- **Admin Boundaries**: Kemendagri 2020
- **Coordinate System**: EPSG:4326
- **Base Map**: kabupaten + kecamatan + desa/kelurahan
- **Overwrite Behavior**: same-named outputs are replaced by the next export

## License

This project is licensed under the **AW Non-Commercial License 1.0** — a source-available license that permits non-commercial use, modification, and distribution. Commercial use requires prior written permission.

See [LICENSE.md](LICENSE.md) for the full legal text.

For commercial licensing inquiries, contact: [commercial@ahliweb.com](mailto:commercial@ahliweb.com)

## Contact

- Community: geospatial@ahliweb.id
- Issues: GitHub Issues
