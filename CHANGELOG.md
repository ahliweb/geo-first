# Changelog

Semua perubahan yang signifikan pada repositori ini akan dicatat dalam file ini.

Format berdasarkan [Keep a Changelog](https://keepachangelog.com/id/1.0.0/),
dan proyek ini mengikuti [Semantic Versioning](https://semver.org/lang/id/).

---

## [1.0.0] - 2026-05-26

### Added
- Data infrastruktur Kabupaten Kotawaringin Barat dari OpenStreetMap
- 5 layer shapefile (.shp/.shx/.dbf/.prj/.cpg): roads, waterways, buildings, landuse, poi
- GeoPackage (.gpkg) sebagai format alternatif
- Project QGIS (.qgs) dengan style kategorikal untuk setiap layer
- Metadata ISO 19115/19139 (CatMDEdit-compatible)
- Paket ZIP distribusi siap upload ke Geoportal Palapa

### Layer
| Layer | Geometri | Fitur | Sumber |
|-------|----------|-------|--------|
| roads | Line | 1.209 | OSM |
| waterways | Line | 707 | OSM |
| buildings | Polygon | 12.047 | OSM |
| landuse | Polygon | 14 | OSM |
| poi | Point | 38 | OSM |

---

## [Unreleased]
### Planned
- Batas administrasi desa/kelurahan
- Data kependudukan (BPS)
- Peta rawan bencana
- Peta tata ruang (RTRW)
