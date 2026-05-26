# Peta Publik Kabupaten Kotawaringin Barat

Repositori data spasial publik untuk Kabupaten Kotawaringin Barat, Kalimantan Tengah. Berisi kumpulan peta dalam format shapefile dan GeoPackage yang siap digunakan di QGIS atau diunggah ke [Geoportal Daerah](https://geoportal.kotawaringinbaratkab.go.id/main/).

## Struktur

```
├── VERSION              # Versi dataset
├── CHANGELOG.md         # Riwayat perubahan
├── README.md            # File ini
├── kobar_infrastruktur.qgs    # Project QGIS
├── shapefiles/          # Data spasial (ESRI Shapefile)
│   ├── roads.*          # Jaringan jalan
│   ├── waterways.*      # Jaringan sungai
│   ├── buildings.*     # Bangunan
│   ├── landuse.*       # Penggunaan lahan
│   └── poi.*           # Fasilitas umum
├── data/               # Data alternatif (GeoPackage)
│   └── kobar.gpkg
└── metadata/           # Metadata ISO 19139
    └── kobar_infrastruktur_metadata.xml
```

## Cara Menggunakan

### QGIS
1. Buka `kobar_infrastruktur.qgs` dengan QGIS 3.x
2. Atau drag file `.shp` dari folder `shapefiles/` langsung ke QGIS

### CatMDEdit
1. Buka file `metadata/kobar_infrastruktur_metadata.xml`

### Geoportal
1. Upload file `.shp` dari folder `shapefiles/` beserta metadata XML

## Lisensi
Data OpenStreetMap: © OpenStreetMap contributors, [ODbL 1.0](https://opendatacommons.org/licenses/odbl/)

## Kontak
Dinas Komunikasi dan Informatika Kab. Kotawaringin Barat
diskominfo@kotawaringinbaratkab.go.id
