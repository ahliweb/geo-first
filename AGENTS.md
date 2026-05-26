# AGENTS.md — Panduan untuk AI Agent

Repositori ini berisi data spasial publik Kabupaten Kotawaringin Barat. Saat bekerja di repo ini, ikuti aturan berikut.

## Struktur Direktori

```
shapefiles/        ← Shapefile (.shp/.shx/.dbf/.prj/.cpg), satu folder per tema
data/              ← GeoPackage (.gpkg) alternatif
metadata/          ← XML metadata ISO 19115/19139 (CatMDEdit)
styles/            ← QML style files untuk QGIS
docs/              ← Dokumentasi tambahan
*.qgs              ← Project QGIS di root
VERSION            ← Versi dataset (SemVer)
CHANGELOG.md       ← Riwayat perubahan
```

## Konvensi Penamaan

- **Shapefile**: `tema.shp` (lowercase, snake_case) — contoh: `batas_admin.shp`, `sekolah.shp`
- **GeoPackage**: `tema.gpkg` — contoh: `batas_admin.gpkg`
- **Layer**: sama dengan nama file, tanpa ekstensi
- **Metadata**: `tema_metadata.xml` dalam folder `metadata/`

## Alur Menambah Peta Baru

### 1. Dapatkan Data Sumber
- **OpenStreetMap**: API bbox `https://api.openstreetmap.org/api/0.6/map?bbox=`
- Setiap tile max 50.000 node, gunakan area kecil per request
- Simpan data mentah OSM XML ke `/tmp/`, jangan commit file .osm

### 2. Konversi ke Shapefile dan GeoPackage
```bash
# Dari OSM XML → GeoPackage (pakai Python GDAL)
python3 -c "
from osgeo import ogr
# parsing OSM, filter tags, buat layer...
"

# GeoPackage → Shapefile
mkdir -p shapefiles
for layer in roads waterways buildings landuse poi; do
  ogr2ogr -f 'ESRI Shapefile' "shapefiles/${layer}.shp" data/kobar.gpkg "$layer" -lco ENCODING=UTF-8
done
```

### 3. Update QGIS Project
- Project `.qgs` di root repo
- Gunakan datasource relatif: `./shapefiles/nama_layer.shp`
- Style kategorikal dengan warna konsisten
- Validasi XML setelah edit: `python3 -c "import xml.etree.ElementTree as ET; ET.parse('project.qgs')"`

### 4. Buat/Update Metadata
- Format ISO 19115/19139 (namespace `http://www.isotc211.org/2005/gmd`)
- Bisa dibuka CatMDEdit
- Sertakan: title, abstract, date, keywords, extent, contact, license

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
4. Path datasource di `.qgs` pakai relative path (`./shapefiles/...`)
5. Tidak ada file temp (.osm, .tmp, .bak) yang tercommit
