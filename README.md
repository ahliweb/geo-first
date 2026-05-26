# Peta Publik Kabupaten Kotawaringin Barat

Repositori data spasial publik untuk Kabupaten Kotawaringin Barat, Kalimantan Tengah. Proyek komunitas pemerhati data geospasial publik — berisi peta dari sumber terbuka (OpenStreetMap, BIG, BPS) dalam format shapefile dan GeoPackage yang siap digunakan di QGIS maupun geoportal daerah.

Metadata mengikuti standar **SNI ISO 19115-3:2019 (SNI 8843-1:2019)** — kompatibel dengan PALAPA/SIMPADU BIG dan CatMDEdit.

## Struktur

```
├── VERSION              # Versi dataset (SemVer)
├── CHANGELOG.md         # Riwayat perubahan
├── AGENTS.md            # Panduan AI Agent
├── CONTRIBUTING.md      # Panduan kontribusi
├── README.md            # File ini
├── kobar_infrastruktur.qgs   # Project QGIS (infrastruktur)
├── batas_admin_kobar.qgs     # Project QGIS (batas admin)
├── shapefiles/          # Data spasial (ESRI Shapefile)
│   ├── roads.*          # Jaringan jalan
│   ├── waterways.*      # Jaringan sungai
│   ├── buildings.*      # Bangunan
│   ├── landuse.*        # Penggunaan lahan
│   ├── poi.*            # Fasilitas umum
│   ├── kabupaten.*      # Batas kabupaten
│   ├── kecamatan.*      # Batas kecamatan (estimasi)
│   └── pusat_kecamatan.* # Titik ibukota kecamatan
├── data/               # GeoPackage
│   ├── kobar.gpkg       # Infrastruktur
│   └── batas_admin.gpkg # Batas administrasi
├── metadata/           # Metadata SNI ISO 19115-3:2019
│   ├── kobar_infrastruktur_metadata.xml
│   └── Batas Administrasi (`batas_admin_metadata.xml`)
└── scripts/            # PyQGIS & utilitas
    └── export_batas_admin.py  # Ekspor SVG/PNG
```


## Dataset

### Infrastruktur (`kobar_infrastruktur.qgs`)
| Layer | Geometri | Fitur | Sumber |
|-------|----------|-------|--------|
| roads | Line | 1.209 | OSM |
| waterways | Line | 707 | OSM |
| buildings | Polygon | 12.047 | OSM |
| landuse | Polygon | 14 | OSM |
| poi | Point | 38 | OSM |

### Batas Administrasi (`batas_admin_kobar.qgs`)
| Layer | Geometri | Fitur | Sumber |
|-------|----------|-------|--------|
| kabupaten | Polygon | 1 | Kemendagri 2020 |
| kecamatan | Polygon | 6 | Kemendagri 2020 |
| desa | Polygon | 94 | Kemendagri 2020 |
| pusat_kecamatan | Point | 6 | Koordinat publik |

> ✅ Data batas administrasi **RESMI** dari Kemendagri 2020 Semester 1.
> 94 desa/kelurahan di 6 kecamatan, lengkap dengan data populasi per desa.
> Sumber: [Ina-Geoportal BIG](https://tanahair.indonesia.go.id) via [batas-admin.geoit.dev](https://batas-admin.geoit.dev)

## Cara Menggunakan

### QGIS
1. Buka `kobar_infrastruktur.qgs` dengan QGIS 3.x
2. Atau drag file `.shp` dari folder `shapefiles/` langsung ke QGIS

### CatMDEdit
1. Buka file `metadata/kobar_infrastruktur_metadata.xml`

### Geoportal PALAPA/SIMPADU
1. File metadata sudah sesuai standar BIG (SNI ISO 19115-3:2019)
2. Upload file `.shp` dari folder `shapefiles/` beserta metadata XML

## Lisensi
Data OpenStreetMap: © OpenStreetMap contributors, [ODbL 1.0](https://opendatacommons.org/licenses/odbl/)

## Kontak
- Email: geospatial@ahliweb.id
- Diskusi: [GitHub Issues](https://github.com/ahliweb/geo-first/issues)
