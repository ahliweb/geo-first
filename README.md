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
├── kobar_infrastruktur.qgs    # Project QGIS
├── shapefiles/          # Data spasial (ESRI Shapefile)
│   ├── roads.*          # Jaringan jalan (1.209 fitur)
│   ├── waterways.*      # Jaringan sungai (707 fitur)
│   ├── buildings.*      # Bangunan (12.047 fitur)
│   ├── landuse.*        # Penggunaan lahan (14 fitur)
│   └── poi.*            # Fasilitas umum (38 fitur)
├── data/               # Data alternatif (GeoPackage)
│   └── kobar.gpkg
└── metadata/           # Metadata SNI ISO 19115-3:2019
    └── kobar_infrastruktur_metadata.xml
```

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
