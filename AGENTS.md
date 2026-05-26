# AGENTS.md — Panduan untuk AI Agent

Repositori ini berisi data spasial publik Kabupaten Kotawaringin Barat. Saat bekerja di repo ini, ikuti aturan berikut.

## Struktur Direktori

```
shapefiles/        ← Shapefile (.shp/.shx/.dbf/.prj/.cpg), satu folder per tema
data/              ← GeoPackage (.gpkg) alternatif
metadata/          ← XML metadata ISO 19115/19139 (CatMDEdit)
styles/            ← QML style files untuk QGIS
scripts/           ← PyQGIS script export & utilitas
*.qgs              ← Project QGIS di root
VERSION            ← Versi dataset (SemVer)
CHANGELOG.md       ← Riwayat perubahan
CONTRIBUTING.md    ← Panduan kontribusi
README.md          ← Informasi umum
```

## Konvensi Penamaan

- **Shapefile**: `tema.shp` (lowercase, snake_case) — contoh: `batas_admin.shp`, `sekolah.shp`
- **GeoPackage**: `tema.gpkg` — contoh: `batas_admin.gpkg`
- **Layer**: sama dengan nama file, tanpa ekstensi
- **Metadata**: `tema_metadata.xml` dalam folder `metadata/`

## Dataset Saat Ini

### Infrastruktur (`data/kobar.gpkg`, `kobar_infrastruktur.qgs`)
| Layer | Geometri | Fitur | Sumber |
|-------|----------|-------|--------|
| roads | MultiLineString | 1.209 | OSM |
| waterways | MultiLineString | 707 | OSM |
| buildings | MultiPolygon | 12.047 | OSM |
| landuse | MultiPolygon | 14 | OSM |
| poi | Point | 38 | OSM |

### Batas Administrasi (`data/batas_admin.gpkg`, `batas_admin_kobar.qgs`)
| Layer | Geometri | Fitur | Sumber |
|-------|----------|-------|--------|
| kabupaten | MultiPolygon | 1 | Kemendagri 2020 |
| kecamatan | MultiPolygon | 6 | Kemendagri 2020 |
| desa | MultiPolygon | 94 | Kemendagri 2020 |
| pusat_kecamatan | Point | 6 | Koordinat publik |

## Alur Menambah Peta Baru

### 1. Dapatkan Data Sumber

- **OpenStreetMap**: API bbox `https://api.openstreetmap.org/api/0.6/map?bbox=`
- Setiap tile max 50.000 node, gunakan area kecil per request
- Simpan data mentah OSM XML ke `/tmp/`, jangan commit file .osm

- **Kemendagri (BIG)**: Data resmi dari [Ina-Geoportal](https://tanahair.indonesia.go.id)
- Tersedia via [batas-admin.geoit.dev](https://batas-admin.geoit.dev) atau [GitHub Alf-Anas](https://github.com/Alf-Anas/batas-administrasi-indonesia)
- Data 2020: kabupaten, kecamatan, desa/kelurahan (format SHP/GPKG)
- Filter per kabupaten menggunakan `Kode_Kab` atau `nama_kab_siak`

- **BPS**: Data statistik kependudukan, ekonomi
- **INARISK/BNPB**: Data risiko bencana

### 2. Konversi ke Shapefile dan GeoPackage

```bash
# Dari OSM XML → GeoPackage (pakai Python GDAL)
python3 -c "
from osgeo import ogr
# parsing OSM, filter tags, buat layer...
"

# Dari Kemendagri GPKG → ekstrak per kabupaten
ogr2ogr -f GPKG batas_admin.gpkg sumber.gpkg \
  -where "nama_kab_siak='KOTAWARINGIN BARAT'" \
  -nln desa -nlt MULTIPOLYGON

# GeoPackage → Shapefile
mkdir -p shapefiles
for layer in kabupaten kecamatan desa pusat_kecamatan; do
  ogr2ogr -f 'ESRI Shapefile' "shapefiles/${layer}.shp" data/batas_admin.gpkg "$layer" -lco ENCODING=UTF-8
done
```

### 3. Update QGIS Project
- Project `.qgs` di root repo
- Gunakan datasource relatif: `./shapefiles/nama_layer.shp`
- Style kategorikal dengan warna konsisten
- Validasi XML setelah edit: `python3 -c "import xml.etree.ElementTree as ET; ET.parse('project.qgs')"`

### 4. Buat/Update Metadata
- Format ISO 19115/19139 (namespace `http://www.isotc211.org/2005/gmd`)
- Standar: **SNI ISO 19115-3:2019** (kompatibel PALAPA/SIMPADU BIG)
- FileIdentifier wajib format **UUID**
- Sertakan: title, abstract, date, keywords, extent, contact, license, purpose, credit, lineage
- Language element wajib pakai `gmd:LanguageCode` (bukan `gco:CharacterString`)
- Sertakan `gmd:metadataExtensionInfo` untuk PALAPA

### 5. Update Versi & Changelog
- Bump versi di `VERSION` (SemVer)
- Tambah entry di `CHANGELOG.md` format Keep a Changelog
- Git tag: `git tag -a vX.Y.Z -m "deskripsi"`
- Commit message: `feat: tambah peta <nama>`

## Tools yang Tersedia
- `ogr2ogr` (GDAL 3.8.4)
- `ogrinfo` — validasi data
- `python3` + `osgeo` (GDAL bindings)
- `curl` / `wget` — download data

## Proyeksi Standar
- **EPSG:4326** (WGS 84) — gunakan untuk semua peta publik

## Validasi Wajib Sebelum Commit
1. `ogrinfo shapefiles/layer.shp layer` — pastikan Feature Count > 0
2. XML QGS valid (parse test)
3. Metadata XML valid (namespace ISO 19139)
4. Metadata FileIdentifier format UUID
5. Metadata Language pakai `gmd:LanguageCode`, bukan `gco:CharacterString`
6. Path datasource di `.qgs` pakai relative path (`./shapefiles/...`)
7. Tidak ada file temp (.osm, .tmp, .bak) yang tercommit

## Kontak
- Community: geospatial@ahliweb.id
- Diskusi melalui GitHub Issues
