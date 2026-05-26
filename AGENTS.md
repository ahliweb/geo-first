# AGENTS.md — AI Agent Guidelines for Geospatial Project Management

This repository manages geospatial data projects for Kotawaringin Barat Regency, Central Kalimantan. Follow these guidelines when working with this repository.

## Architecture

```
geo-first/
├── projects/                    # Isolated project workspaces
│   ├── <project-name>/         # Each map project gets its own directory
│   │   ├── data/               # Project-specific GeoPackage/CSV sources
│   │   ├── shapefiles/         # Project-specific ESRI Shapefiles
│   │   ├── scripts/            # Project-specific PyQGIS/GDAL scripts
│   │   ├── metadata/           # ISO 19139/19115-3 XML metadata
│   │   ├── qgis/               # QGIS project files (.qgs/.qgz)
│   │   ├── styles/             # QML style definitions
│   │   └── output/             # Exported maps (PNG/SVG/PDF)
│   └── _template/              # Project scaffolding template
├── shared/                      # Cross-project shared resources
│   ├── data/                   # Shared GeoPackage databases
│   ├── shapefiles/             # Shared shapefiles (admin boundaries, OSM)
│   ├── scripts/                # Reusable PyQGIS/GDAL utilities
│   ├── config/                 # Sector profiles and export settings
│   ├── styles/                 # Shared QML style libraries
│   └── templates/              # Map layout templates
├── docs/                        # Documentation
│   ├── examples/               # Sample datasets and VRT templates
│   └── guides/                 # Technical how-to guides
├── AGENTS.md                    # This file — AI agent guidelines
├── README.md                    # Project overview
├── LICENSE.md                   # AW Non-Commercial License 1.0
├── CHANGELOG.md                 # Semantic versioned changelog
├── VERSION                      # Current version (SemVer)
└── .gitignore                   # Git ignore patterns
```

## Project Lifecycle

### 1. Initialize Project

```bash
# Scaffold from template
cp -r projects/_template projects/<project-name>
```

### 2. Acquire Source Data

**OpenStreetMap**
- Overpass API: `https://api.openstreetmap.org/api/0.6/map?bbox=<min_lon>,<min_lat>,<max_lon>,<max_lat>`
- Max 50,000 nodes per tile — use small bounding boxes per request
- Store raw OSM XML in `/tmp/`, never commit `.osm` files

**Kemendagri (BIG Official)**
- Source: [Ina-Geoportal](https://tanahair.indonesia.go.id) or [GitHub Alf-Anas](https://github.com/Alf-Anas/batas-administrasi-indonesia)
- Data 2020: kabupaten, kecamatan, desa/kelurahan (SHP/GPKG)
- Filter by `Kode_Kab` or `nama_kab_siak`

**BPS / INARISK / BNPB**
- Statistical data, disaster risk layers

### 3. Data Processing Pipeline

```bash
# OSM XML → GeoPackage (Python GDAL)
python3 -c "
from osgeo import ogr
# Parse OSM, filter tags, create layers...
"

# Kemendagri GPKG → Extract per kabupaten
ogr2ogr -f GPKG projects/<name>/data/admin.gpkg shared/data/batas_admin.gpkg \
  -where "nama_kab_siak='KOTAWARINGIN BARAT'" \
  -nln desa -nlt MULTIPOLYGON

# GeoPackage → Shapefile (project-specific)
mkdir -p projects/<name>/shapefiles
for layer in kabupaten kecamatan desa; do
  ogr2ogr -f 'ESRI Shapefile' \
    "projects/<name>/shapefiles/${layer}.shp" \
    projects/<name>/data/admin.gpkg "$layer" \
    -lco ENCODING=UTF-8
done
```

### 4. Map Generation

Use the shared professional map generation script:

```bash
python3 shared/scripts/generate_professional_map.py \
  --project projects/<project-name> \
  --sector health \
  --layers faskes \
  --output-format png,pdf,svg \
  --dpi 300
```

Or use PyQGIS directly (see `shared/scripts/` for templates).

For SOPD workflows, prefer the sector profile registry in `shared/config/sector_profiles.json` and keep `kabupaten`, `kecamatan`, and `desa` as the base map.

### 5. Metadata Generation

- Format: ISO 19115-3 / ISO 19139 (CatMDEdit compatible)
- Standard: **SNI ISO 19115-3:2019** (PALAPA/SIMPADU BIG compliant)
- FileIdentifier: **UUID** format required
- Language: `gmd:LanguageCode` (NOT `gco:CharacterString`)
- Include: `gmd:metadataExtensionInfo` for PALAPA
- Required elements: title, abstract, date, keywords, extent, contact, license, purpose, credit, lineage

### 6. Version & Release

- Bump `VERSION` (SemVer: MAJOR.MINOR.PATCH)
- Add entry to `CHANGELOG.md` (Keep a Changelog format)
- Git tag: `git tag -a vX.Y.Z -m "description"`
- Commit message: `feat: add <project-name> map`

## Naming Conventions

- **Shapefiles**: `theme.shp` (lowercase, snake_case) — e.g., `batas_admin.shp`, `sekolah.shp`
- **GeoPackage**: `theme.gpkg` — e.g., `batas_admin.gpkg`
- **Layers**: Match filename without extension
- **Metadata**: `theme_metadata.xml` in `projects/<name>/metadata/`
- **Projects**: `project-name` (kebab-case) — e.g., `faskes-kobar`, `sekolah-kobar`
- **Outputs**: `peta_<theme>_<region>.<ext>` — e.g., `peta_faskes_kobar.png`

## Shared Datasets

### Administrative Boundaries (`shared/data/batas_admin.gpkg`)
| Layer | Geometry | Features | Source |
|-------|----------|----------|--------|
| kabupaten | MultiPolygon | 1 | Kemendagri 2020 |
| kecamatan | MultiPolygon | 6 | Kemendagri 2020 |
| desa | MultiPolygon | 94 | Kemendagri 2020 |
| pusat_kecamatan | Point | 6 | Public coordinates |

### Infrastructure (`shared/data/kobar.gpkg`)
| Layer | Geometry | Features | Source |
|-------|----------|----------|--------|
| roads | MultiLineString | 1,209 | OSM |
| waterways | MultiLineString | 707 | OSM |
| buildings | MultiPolygon | 12,047 | OSM |
| landuse | MultiPolygon | 14 | OSM |
| poi | Point | 38 | OSM |

## Technical Stack

- **GDAL/OGR**: 3.8.4 with Python bindings
- **QGIS**: 3.34.4-Prizren with PyQGIS API
- **Python**: 3.x with `osgeo`, `qgis` modules
- **Tools**: `ogr2ogr`, `ogrinfo`, `curl`, `wget`
- **Projection**: EPSG:4326 (WGS 84) for all public maps

## Pre-Commit Validation Checklist

1. `ogrinfo projects/<name>/shapefiles/layer.shp layer` — Feature Count > 0
2. QGS XML valid (parse test)
3. Metadata XML valid (ISO 19139 namespace)
4. Metadata FileIdentifier is valid UUID
5. Metadata Language uses `gmd:LanguageCode`, NOT `gco:CharacterString`
6. QGS datasource paths use relative paths (`../../shared/shapefiles/...`)
7. No temp files committed (`.osm`, `.tmp`, `.bak`)
8. All outputs in `projects/<name>/output/` directory

## Project Template Structure

When creating a new project, copy `projects/_template/` and populate:

```
projects/<name>/
├── data/              # Source data (CSV, GPKG, etc.)
├── shapefiles/        # Exported shapefiles
├── scripts/           # Project-specific processing scripts
├── metadata/          # ISO 19139 XML metadata
├── qgis/              # QGIS project files
├── styles/            # QML style files
├── output/            # PNG/SVG/PDF exports
└── README.md          # Project-specific documentation
```

## Licensing

This repository is licensed under the **AW Non-Commercial License 1.0** — a source-available license.

### Key Restrictions

- **Non-commercial use only** — no commercial advantage, revenue generation, or paid services
- **Commercial use requires written permission** from [commercial@ahliweb.com](mailto:commercial@ahliweb.com)
- **Attribution required** — copyright notice and license text must accompany all copies
- **No trademark rights granted** — except for describing the software's origin

### What AI Agents Must Do

1. Include `LICENSE.md` in all project outputs and distributions
2. Reference the license in generated metadata (ISO 19139 `<gmd:useLimitation>`)
3. Never suggest commercial use without noting the license restriction
4. When scaffolding new projects, copy the license reference to project README

### License Identifier

- SPDX-style: `LicenseRef-AW-NC-1.0`
- Full name: `AW Non-Commercial License 1.0`

## Contact

- Community: geospatial@ahliweb.id
- Commercial licensing: commercial@ahliweb.com
- Discussions via GitHub Issues
