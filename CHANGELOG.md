# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Population data per village (BPS)
- Spatial planning maps (RTRW)
- AWCMS-Micro plugin refactor assessment and adapter boundary
- Parameterize legacy export scripts for reusable job invocation

---

## [1.4.0] - 2026-05-26

### Added
- AW Non-Commercial License 1.0 (LICENSE.md)
- License references in all documentation files
- Project template with license reference
- Professional map generator script (`shared/scripts/generate_professional_map.py`)

### Changed
- Repository restructured: `projects/`, `shared/`, `docs/` directories
- All documentation updated to technical English
- AGENTS.md rewritten with AI-native language
- CONTRIBUTING.md updated with license requirements
- README.md updated with new structure and license section

---

## [1.3.0] - 2026-05-26

### Added
- Official Kemendagri 2020 Semester 1 village/kelurahan boundaries
- 94 villages/kelurahan across 6 kecamatan in Kotawaringin Barat
- Population data, area per village
- `desa` layer in GeoPackage and Shapefile

### 6 Kecamatan (94 desa/kelurahan)
| Kecamatan | Desa/Kel |
|-----------|----------|
| Arut Selatan | 20 |
| Kumai | 18 |
| Kotawaringin Lama | 17 |
| Pangkalan Banteng | 17 |
| Arut Utara | 11 |
| Pangkalan Lada | 11 |

---

## [1.2.0] - 2026-05-26

### Added
- Official Kemendagri 2020 Semester 1 administrative boundaries (kabupaten + kecamatan)
- Replaced previous community estimation data

---

## [1.1.0] - 2026-05-26

### Added
- Kotawaringin Barat administrative boundaries (Voronoi estimation)
- PyQGIS script `scripts/export_batas_admin.py`

---

## [1.0.0] - 2026-05-26

### Added
- Infrastructure data from OpenStreetMap (roads, waterways, buildings, landuse, poi)
- SNI ISO 19115-3:2019 PALAPA/SIMPADU metadata
- Documentation (AGENTS.md, CONTRIBUTING.md, README.md)
