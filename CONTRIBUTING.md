# Panduan Kontribusi

Proyek ini adalah inisiatif komunitas pemerhati data spasial publik. Data bersumber dari layanan terbuka dan resmi (OpenStreetMap, BIG/Kemendagri, BPS), bukan data sensitif pemerintah. Kontribusi terbuka untuk siapa saja.

## Dataset Saat Ini

| Tema | File | Layer | Fitur | Sumber |
|------|------|-------|-------|--------|
| Infrastruktur | `kobar_infrastruktur.qgs` | roads, waterways, buildings, landuse, poi | 14.015 | OSM |
| Batas Admin | `batas_admin_kobar.qgs` | kabupaten, kecamatan, desa, pusat_kecamatan | 107 | Kemendagri 2020 |

## Persiapan
1. Clone repo: `git clone <repo-url>`
2. Pastikan GDAL terinstal: `ogrinfo --version`
3. QGIS 3.x untuk preview peta
4. Python 3 + `osgeo` untuk scripting

## Workflow

### 1. Buat Branch
```bash
git checkout -b feat/tambah-peta-<nama>
```

### 2. Tambah Data
- Tempatkan shapefile di `shapefiles/<nama>.shp`
- Format: EPSG:4326, encoding UTF-8
- Jika dari GeoPackage/GeoJSON, konversi dengan `ogr2ogr`

### 3. Update Project QGIS
- Buka project `.qgs` yang relevan di QGIS, tambah layer baru, atur style
- Atau buat project baru di root repo
- Simpan project, pastikan datasource relatif (`./shapefiles/...`)
- Validasi XML: `python3 -c "import xml.etree.ElementTree as ET; ET.parse('project.qgs')"`

### 4. Metadata (PALAPA/SIMPADU BIG)
- Standar: **SNI ISO 19115-3:2019** (SNI 8843-1:2019)
- Salin template dari `metadata/batas_admin_metadata.xml` atau `metadata/kobar_infrastruktur_metadata.xml`
- Wajib:
  - FileIdentifier format **UUID**
  - Language pakai `gmd:LanguageCode` (bukan `gco:CharacterString`)
  - Sertakan `gmd:metadataExtensionInfo`
  - Title, abstract, date, keywords, extent, contact, license
  - Purpose, credit, lineage, source description
  - Sebutkan sumber data dengan jelas (OSM, Kemendagri, dll)
- Validasi: `python3 -c "import xml.etree.ElementTree as ET; ET.parse('metadata/file.xml')"`

### 5. Versioning
- Update `VERSION` (ikuti [SemVer](https://semver.org/)):
  - `MAJOR` — perubahan besar (restruktur)
  - `MINOR` — tambah tema/layer baru
  - `PATCH` — perbaikan data/style/metadata
- Update `CHANGELOG.md` di bawah `[Unreleased]`
- Sebelum merge, pindahkan ke versi release
- Git tag: `git tag -a vX.Y.Z -m "deskripsi"`

### 6. Commit & Pull Request
```bash
git add shapefiles/<nama>.* VERSION CHANGELOG.md metadata/<nama>_metadata.xml
git commit -m "feat: tambah peta <nama> — <deskripsi singkat>"
git push origin feat/tambah-peta-<nama>
```
Buat Pull Request ke `main`.

## Standar Data
- **Proyeksi**: EPSG:4326 (WGS 84)
- **Encoding**: UTF-8
- **Geometri**: valid (tanpa self-intersection, tanpa duplikat)
- **Atribut**: minimal field `nama` dan `kategori`/`kode`
- **Sumber**: disebutkan di layer dan metadata

## Sumber Data yang Direkomendasikan

| Sumber | URL | Data |
|--------|-----|------|
| OpenStreetMap | [openstreetmap.org](https://www.openstreetmap.org) | Infrastruktur, jalan, bangunan, POI |
| BIG / Ina-Geoportal | [tanahair.indonesia.go.id](https://tanahair.indonesia.go.id) | Batas administrasi, RBI |
| Kemendagri (via Alf-Anas) | [GitHub](https://github.com/Alf-Anas/batas-administrasi-indonesia) | Batas admin 2020 (SHP/GPKG) |
| BPS | [bps.go.id](https://www.bps.go.id) | Statistik, kependudukan |
| INARISK BNPB | [inarisk.bnpb.go.id](https://inarisk.bnpb.go.id) | Risiko bencana |
| ESDM One Map | [geoportal.esdm.go.id](https://geoportal.esdm.go.id) | Geologi, tambang |

## Lisensi
Data yang ditambahkan harus memiliki lisensi yang memperbolehkan publikasi ulang. Sebutkan lisensi di metadata:
- OSM → **ODbL 1.0** (wajib atribusi)
- Kemendagri → Data publik pemerintah (sebutkan sumber)
- BPS → Data publik (sebutkan tahun dan sumber)

## Kontak
- Email: geospatial@ahliweb.id
- Diskusi: [GitHub Issues](https://github.com/ahliweb/geo-first/issues)
