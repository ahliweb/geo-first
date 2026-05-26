# Changelog

Format berdasarkan [Keep a Changelog](https://keepachangelog.com/id/1.0.0/),
dan proyek ini mengikuti [Semantic Versioning](https://semver.org/lang/id/).

---

## [1.1.0] - 2026-05-26

### Added
- Batas administrasi Kabupaten Kotawaringin Barat dari OSM (relation 16179711)
- Batas 6 kecamatan (estimasi Voronoi/Thiessen dari pusat kecamatan)
- Titik pusat kecamatan (6 ibukota kecamatan)
- Shapefile + GeoPackage untuk semua layer admin
- Project QGIS `batas_admin_kobar.qgs` dengan style per kecamatan
- Script PyQGIS `scripts/export_batas_admin.py` untuk ekspor SVG/PNG
- Metadata SNI ISO 19115-3:2019 untuk batas admin
- Ekspor SVG mandiri via GDAL (tanpa QGIS)

### Layer
| Layer | Geometri | Fitur | Sumber |
|-------|----------|-------|--------|
| kabupaten | Polygon | 1 | OSM |
| kecamatan | Polygon | 6 | Estimasi Voronoi |
| pusat_kecamatan | Point | 6 | Koordinat publik |

### ⚠️ Disclaimer
Batas kecamatan adalah ESTIMASI komunitas, BUKAN data resmi BIG/Mendagri.

---

## [1.0.0] - 2026-05-26

### Added
- Data infrastruktur Kabupaten Kotawaringin Barat dari OpenStreetMap (OSM)
- 5 layer shapefile (.shp/.shx/.dbf/.prj/.cpg): roads, waterways, buildings, landuse, poi
- GeoPackage (.gpkg) sebagai format alternatif
- Project QGIS (.qgs) dengan style kategorikal untuk setiap layer
- Metadata SNI ISO 19115-3:2019 (SNI 8843-1:2019) — kompatibel PALAPA/SIMPADU BIG
- UUID FileIdentifier pada metadata
- `gmd:metadataExtensionInfo` untuk PALAPA
- Paket ZIP distribusi
- Sistem dokumentasi: AGENTS.md, CONTRIBUTING.md, README.md

### Layer
| Layer | Geometri | Fitur | Sumber |
|-------|----------|-------|--------|
| roads | Line | 1.209 | OSM |
| waterways | Line | 707 | OSM |
| buildings | Polygon | 12.047 | OSM |
| landuse | Polygon | 14 | OSM |
| poi | Point | 38 | OSM |

### Technical
- Proyeksi: EPSG:4326 (WGS 84)
- GDAL 3.8.4 + Python osgeo
- Language element: `gmd:LanguageCode` (ISO 639-2)
- Metadata validasi 26 item checklist BIG/SIMPADU

---

## [Unreleased]
### Planned
- Batas administrasi desa/kelurahan (resmi)
- Data kependudukan (BPS)
- Peta rawan bencana
- Peta tata ruang (RTRW)
