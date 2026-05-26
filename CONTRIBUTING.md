# Panduan Kontribusi

Terima kasih ingin berkontribusi menambah peta publik Kotawaringin Barat.

Proyek ini adalah inisiatif komunitas pemerhati data spasial publik. Data bersumber dari layanan terbuka (OpenStreetMap, BIG, BPS, dll), bukan data sensitif pemerintah. Kontribusi terbuka untuk siapa saja.

## Persiapan
1. Clone repo: `git clone <repo-url>`
2. Pastikan GDAL terinstal: `ogrinfo --version`
3. QGIS 3.x untuk preview peta

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
- Buka di QGIS, tambah layer baru, atur style
- Simpan project, pastikan datasource relatif (`./shapefiles/...`)
- Validasi XML: `python3 -c "import xml.etree.ElementTree as ET; ET.parse('kobar_infrastruktur.qgs')"`

### 4. Metadata (PALAPA/SIMPADU BIG)
- Standar: **SNI ISO 19115-3:2019** (SNI 8843-1:2019)
- Salin template dari `metadata/kobar_infrastruktur_metadata.xml`
- Wajib:
  - FileIdentifier format **UUID**
  - Language pakai `gmd:LanguageCode` (bukan `gco:CharacterString`)
  - Sertakan `gmd:metadataExtensionInfo`
  - Title, abstract, date, keywords, extent, contact, license
  - Purpose, credit, lineage, source description
- Validasi: `python3 -c "import xml.etree.ElementTree as ET; ET.parse('metadata/file.xml')"`

### 5. Versioning
- Update `VERSION` (ikuti [SemVer](https://semver.org/)):
  - `MAJOR` — perubahan besar (restruktur)
  - `MINOR` — tambah tema baru
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
- **Atribut**: minimal field `name` dan `kategori`
- **Sumber**: disebutkan di layer dan metadata

## Sumber Data yang Direkomendasikan
- [OpenStreetMap](https://www.openstreetmap.org) — infrastruktur, jalan, bangunan
- [BPS](https://www.bps.go.id) — statistik, kependudukan
- [BIG](https://tanahair.indonesia.go.id) — batas administrasi, topografi
- [INARISK](https://inarisk.bnpb.go.id) — risiko bencana
- [ESDM One Map](https://geoportal.esdm.go.id) — geologi, tambang

## Lisensi
Data yang ditambahkan harus memiliki lisensi yang memperbolehkan publikasi ulang. Sebutkan lisensi di metadata.

## Kontak
- Email: geospatial@ahliweb.id
- Diskusi: GitHub Issues
