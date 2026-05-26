# Peta Publik Kabupaten Kotawaringin Barat

Repositori data spasial publik untuk Kabupaten Kotawaringin Barat, Kalimantan Tengah. Proyek komunitas pemerhati data geospasial publik — berisi peta dari sumber terbuka (OpenStreetMap) dan resmi (Kemendagri/BIG) dalam format Shapefile dan GeoPackage, siap digunakan di QGIS maupun geoportal daerah.

Metadata mengikuti standar **SNI ISO 19115-3:2019 (SNI 8843-1:2019)** — kompatibel dengan PALAPA/SIMPADU BIG dan CatMDEdit.

## Struktur

```
├── VERSION                   # Versi dataset (SemVer)
├── CHANGELOG.md              # Riwayat perubahan
├── AGENTS.md                 # Panduan AI Agent
├── CONTRIBUTING.md           # Panduan kontribusi
├── README.md                 # File ini
├── kobar_infrastruktur.qgs   # Project QGIS — Infrastruktur
├── batas_admin_kobar.qgs     # Project QGIS — Batas Administrasi
├── shapefiles/               # Data spasial (ESRI Shapefile)
│   ├── roads.*               # Jaringan jalan
│   ├── waterways.*           # Jaringan sungai
│   ├── buildings.*           # Bangunan
│   ├── landuse.*             # Penggunaan lahan
│   ├── poi.*                 # Fasilitas umum
│   ├── kabupaten.*           # Batas kabupaten
│   ├── kecamatan.*           # Batas kecamatan
│   ├── desa.*                # Batas desa/kelurahan
│   └── pusat_kecamatan.*     # Titik ibukota kecamatan
├── data/                     # GeoPackage
│   ├── kobar.gpkg            # Infrastruktur (5 layer)
│   └── batas_admin.gpkg      # Batas administrasi (4 layer)
├── metadata/                 # Metadata SNI ISO 19115-3:2019
│   ├── kobar_infrastruktur_metadata.xml
│   └── batas_admin_metadata.xml
├── docs/                     # Panduan & contoh
    │   ├── panduan-faskes.md  # Panduan tambah faskes
    │   └── contoh/
    └── scripts/                  # PyQGIS & utilitas
    ├── export_batas_admin.py # Ekspor SVG/PNG batas admin
    └── export_faskes.py     # Ekspor SVG/PNG fasilitas kesehatan
```

## Dataset

### Infrastruktur — `kobar_infrastruktur.qgs`
| Layer | Geometri | Fitur | Sumber |
|-------|----------|-------|--------|
| roads | Line | 1.209 | OpenStreetMap |
| waterways | Line | 707 | OpenStreetMap |
| buildings | Polygon | 12.047 | OpenStreetMap |
| landuse | Polygon | 14 | OpenStreetMap |
| poi | Point | 38 | OpenStreetMap |

### Batas Administrasi — `batas_admin_kobar.qgs`
| Layer | Geometri | Fitur | Sumber |
|-------|----------|-------|--------|
| kabupaten | Polygon | 1 | Kemendagri 2020 |
| kecamatan | Polygon | 6 | Kemendagri 2020 |
| desa | Polygon | 94 | Kemendagri 2020 |
| pusat_kecamatan | Point | 6 | Koordinat publik |

| Kecamatan | Desa/Kel |
|-----------|----------|
| Arut Selatan | 20 |
| Kumai | 18 |
| Kotawaringin Lama | 17 |
| Pangkalan Banteng | 17 |
| Arut Utara | 11 |
| Pangkalan Lada | 11 |
| **Total** | **94** |

> ✅ Data batas administrasi **RESMI** Kemendagri 2020 Semester 1 dari [Ina-Geoportal BIG](https://tanahair.indonesia.go.id).

## Cara Menggunakan

### QGIS
1. Buka `kobar_infrastruktur.qgs` atau `batas_admin_kobar.qgs` dengan QGIS 3.x
2. Atau drag file `.shp` dari folder `shapefiles/` langsung ke QGIS

### CatMDEdit
1. Buka file `metadata/kobar_infrastruktur_metadata.xml` atau `metadata/batas_admin_metadata.xml`

### Geoportal PALAPA/SIMPADU
1. Metadata sudah sesuai standar BIG (SNI ISO 19115-3:2019)
2. Upload file `.shp` dari folder `shapefiles/` beserta metadata XML

### PyQGIS — Ekspor SVG/PNG
```bash
# Dari QGIS Python Console:
exec(open('scripts/export_batas_admin.py').read())

# Atau gunakan GDAL standalone:
python3 scripts/export_batas_admin.py
```
Output di folder `output/` — SVG dan PNG siap pakai.

## Lisensi
- Data OpenStreetMap: © OpenStreetMap contributors, [ODbL 1.0](https://opendatacommons.org/licenses/odbl/)
- Data Kemendagri: Data publik pemerintah Indonesia

## Kontak
- Email: geospatial@ahliweb.id
- Diskusi: [GitHub Issues](https://github.com/ahliweb/geo-first/issues)
