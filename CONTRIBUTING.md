# Contributing Guide

This project is a community initiative for public geospatial data. Data sources are open and official (OpenStreetMap, BIG/Kemendagri, BPS), not sensitive government data. Contributions are open to anyone.

## License

This repository is licensed under the **AW Non-Commercial License 1.0**.
See [LICENSE.md](LICENSE.md) for the full legal text.

All contributions are subject to the same license. By contributing, you agree that your contributions will be licensed under these terms.

For commercial licensing inquiries, contact: [commercial@ahliweb.com](mailto:commercial@ahliweb.com)

## Current Datasets

| Theme | Location | Layers | Features | Source |
|-------|----------|--------|----------|--------|
| Infrastructure | `shared/data/kobar.gpkg` | roads, waterways, buildings, landuse, poi | 14,015 | OSM |
| Admin Boundaries | `shared/data/batas_admin.gpkg` | kabupaten, kecamatan, desa, pusat_kecamatan | 107 | Kemendagri 2020 |

## Prerequisites

1. Clone the repo: `git clone <repo-url>`
2. Ensure GDAL is installed: `ogrinfo --version`
3. QGIS 3.x for map preview
4. Python 3 + `osgeo` for scripting

## Workflow

### 1. Create a Branch

```bash
git checkout -b feat/add-<map-name>
```

### 2. Add Data

- Place shapefiles in `projects/<name>/shapefiles/<name>.shp`
- Format: EPSG:4326, UTF-8 encoding
- If from GeoPackage/GeoJSON, convert with `ogr2ogr`

### 3. Update QGIS Project

- Open the relevant `.qgs` project in QGIS, add new layers, configure styles
- Or create a new project in the project directory
- Save the project, ensure datasource paths are relative (`../../shared/shapefiles/...`)
- Validate XML: `python3 -c "import xml.etree.ElementTree as ET; ET.parse('project.qgs')"`

### 4. Metadata (PALAPA/SIMPADU BIG)

- Standard: **SNI ISO 19115-3:2019** (SNI 8843-1:2019)
- Copy template from `shared/metadata/batas_admin_metadata.xml` or `shared/metadata/kobar_infrastruktur_metadata.xml`
- Required:
  - FileIdentifier in **UUID** format
  - Language uses `gmd:LanguageCode` (NOT `gco:CharacterString`)
  - Include `gmd:metadataExtensionInfo`
  - Title, abstract, date, keywords, extent, contact, license
  - Purpose, credit, lineage, source description
  - Clearly state data source (OSM, Kemendagri, etc.)
- Validate: `python3 -c "import xml.etree.ElementTree as ET; ET.parse('metadata/file.xml')"`

### 5. Versioning

- Update `VERSION` (follow [SemVer](https://semver.org/)):
  - `MAJOR` — breaking changes (restructure)
  - `MINOR` — new themes/layers
  - `PATCH` — data/style/metadata fixes
- Update `CHANGELOG.md` under `[Unreleased]`
- Before merge, move to release version
- Git tag: `git tag -a vX.Y.Z -m "description"`

### 6. Commit & Pull Request

```bash
git add projects/<name>/ VERSION CHANGELOG.md projects/<name>/metadata/<name>_metadata.xml
git commit -m "feat: add <name> map — <brief description>"
git push origin feat/add-<name>
```

Create a Pull Request to `main`.

## Data Standards

- **Projection**: EPSG:4326 (WGS 84)
- **Encoding**: UTF-8
- **Geometry**: valid (no self-intersection, no duplicates)
- **Attributes**: minimum `nama` and `kategori`/`kode` fields
- **Source**: cited in layer and metadata

## Recommended Data Sources

| Source | URL | Data |
|--------|-----|------|
| OpenStreetMap | [openstreetmap.org](https://www.openstreetmap.org) | Infrastructure, roads, buildings, POI |
| BIG / Ina-Geoportal | [tanahair.indonesia.go.id](https://tanahair.indonesia.go.id) | Administrative boundaries, RBI |
| Kemendagri (via Alf-Anas) | [GitHub](https://github.com/Alf-Anas/batas-administrasi-indonesia) | Admin boundaries 2020 (SHP/GPKG) |
| BPS | [bps.go.id](https://www.bps.go.id) | Statistics, demographics |
| INARISK BNPB | [inarisk.bnpb.go.id](https://inarisk.bnpb.go.id) | Disaster risk |
| ESDM One Map | [geoportal.esdm.go.id](https://geoportal.esdm.go.id) | Geology, mining |

## Source Data Licensing

Added data must have a license that allows republication. Cite the license in metadata:
- OSM → **ODbL 1.0** (attribution required)
- Kemendagri → Public government data (cite source)
- BPS → Public data (cite year and source)

## Contact

- Email: geospatial@ahliweb.id
- Discussions: [GitHub Issues](https://github.com/ahliweb/geo-first/issues)
