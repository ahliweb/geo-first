# Panduan — Menambah Titik Fasilitas Kesehatan

Panduan langkah-demi-langkah menambahkan data titik fasilitas kesehatan (puskesmas, rumah sakit, klinik, posyandu, apotek) ke repositori ini, siap upload ke geoportal PALAPA, dan siap diolah dengan PyQGIS.

---

## 1. Struktur Data

### Format
Proyeksi **EPSG:4326** (WGS 84), encoding **UTF-8**.

### Field / Kolom Wajib
| Field | Tipe | Keterangan | Contoh |
|-------|------|------------|--------|
| `osm_id` | String | ID unik (pakai kode faskes jika ada) | `PUSK_KUMAI_01` |
| `nama` | String | Nama fasilitas | `Puskesmas Kumai` |
| `kategori` | String | Jenis fasilitas | `puskesmas` / `rumah_sakit` |
| `sub_kategori` | String | Sub jenis | `puskesmas_rawat_inap` |
| `operator` | String | Pengelola | `Dinas Kesehatan Kobar` |
| `alamat` | String | Alamat lengkap | `Jl. HM Idris No.10, Kumai` |
| `kecamatan` | String | Nama kecamatan | `Kumai` |
| `desa` | String | Nama desa/kelurahan | `Kumai Hulu` |
| `telepon` | String | Nomor telepon | `0532-xxxxx` |
| `sumber` | String | Sumber data | `Dinkes Kobar` / `OSM` / `BPS` |

### Kategori standar
| `kategori` | `sub_kategori` | Deskripsi |
|-----------|----------------|-----------|
| `rumah_sakit` | `rs_umum` | RSU tipe A/B/C/D |
| `rumah_sakit` | `rs_khusus` | RS Ibu Anak, RS Jiwa, dll |
| `puskesmas` | `puskesmas_rawat_inap` | Puskesmas dengan rawat inap |
| `puskesmas` | `puskesmas_non_rawat_inap` | Puskesmas tanpa rawat inap |
| `klinik` | `klinik_pratama` | Klinik pratama |
| `klinik` | `klinik_utama` | Klinik utama |
| `posyandu` | `posyandu` | Pos Pelayanan Terpadu |
| `apotek` | `apotek` | Apotek / toko obat |
| `pustu` | `pustu` | Puskesmas Pembantu |
| `polindes` | `polindes` | Pondok Bersalin Desa |

---

## 2. Membuat Data

### A. Manual (CSV → Shapefile)

Buat file CSV dengan koordinat:

```csv
osm_id,nama,kategori,sub_kategori,operator,alamat,kecamatan,desa,telepon,sumber,longitude,latitude
RS_PBUN_01,RSUD Sultan Imanuddin,rumah_sakit,rs_umum,Pemkab Kobar,"Jl. Sutan Syahrir No.17, Pangkalan Bun",Arut Selatan,Sidorejo,0532-21118,Dinkes Kobar,111.6250,-2.6720
PUSK_KUMAI_01,Puskesmas Kumai,puskesmas,puskesmas_rawat_inap,Dinkes Kobar,"Jl. HM Idris No.10, Kumai",Kumai,Kumai Hulu,0532-61234,Dinkes Kobar,111.7320,-2.7430
PUSK_ARSEL_01,Puskesmas Arut Selatan,puskesmas,puskesmas_non_rawat_inap,Dinkes Kobar,"Jl. Pangkalan Bun - Kumai KM 5",Arut Selatan,Raja,0532-21200,Dinkes Kobar,111.6550,-2.6800
```

Konversi ke Shapefile:

```bash
# CSV → VRT (Virtual Format)
cat > faskes.vrt << 'VRTEOF'
<OGRVRTDataSource>
  <OGRVRTLayer name="faskes">
    <SrcDataSource>faskes.csv</SrcDataSource>
    <GeometryType>wkbPoint</GeometryType>
    <LayerSRS>EPSG:4326</LayerSRS>
    <GeometryField encoding="PointFromColumns" x="longitude" y="latitude"/>
  </OGRVRTLayer>
</OGRVRTDataSource>
VRTEOF

# VRT → Shapefile
ogr2ogr -f "ESRI Shapefile" shapefiles/faskes.shp faskes.vrt -lco ENCODING=UTF-8
```

### B. Python (GDAL/osgeo)

```python
from osgeo import ogr, osr

sr = osr.SpatialReference()
sr.ImportFromEPSG(4326)

driver = ogr.GetDriverByName('ESRI Shapefile')
ds = driver.CreateDataSource('shapefiles/faskes.shp')
layer = ds.CreateLayer('faskes', sr, ogr.wkbPoint)

# Buat field
fields = [
    ('osm_id', ogr.OFTString), ('nama', ogr.OFTString),
    ('kategori', ogr.OFTString), ('sub_kategori', ogr.OFTString),
    ('operator', ogr.OFTString), ('alamat', ogr.OFTString),
    ('kecamatan', ogr.OFTString), ('desa', ogr.OFTString),
    ('telepon', ogr.OFTString), ('sumber', ogr.OFTString),
]
for name, typ in fields:
    layer.CreateField(ogr.FieldDefn(name, typ))

# Tambah titik
data = [
    ('RS_PBUN_01','RSUD Sultan Imanuddin','rumah_sakit','rs_umum',
     'Pemkab Kobar','Jl. Sutan Syahrir No.17','Arut Selatan','Sidorejo',
     '0532-21118','Dinkes Kobar',111.6250,-2.6720),
]

for row in data:
    feature = ogr.Feature(layer.GetLayerDefn())
    pt = ogr.Geometry(ogr.wkbPoint)
    pt.AddPoint(row[-2], row[-1])  # lon, lat
    feature.SetGeometry(pt)
    for i, val in enumerate(row[:-2]):
        feature.SetField(i, val)
    layer.CreateFeature(feature)

ds = None
```

### C. Google Sheets → CSV → QGIS

1. Isi data di Google Sheets:
   ```
   nama | kategori | kecamatan | latitude | longitude | alamat
   ```
2. Download sebagai CSV
3. Di QGIS: `Layer > Add Layer > Add Delimited Text Layer`
4. Export: klik kanan layer → Export → Save Features As → ESRI Shapefile

---

## 3. Integrasi ke GeoPackage

```bash
# Dari Shapefile → GeoPackage
ogr2ogr -f GPKG data/kobar.gpkg shapefiles/faskes.shp \
  -nln faskes -nlt POINT -update -lco ENCODING=UTF-8

# Verifikasi
ogrinfo -so data/kobar.gpkg faskes | grep "Feature Count"
```

---

## 4. Metadata (ISO 19139)

Buat file `metadata/faskes_metadata.xml` dengan struktur berikut:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gmd:MD_Metadata xmlns:gmd="http://www.isotc211.org/2005/gmd"
                 xmlns:gco="http://www.isotc211.org/2005/gco">
  <gmd:fileIdentifier>
    <gco:CharacterString>UUID-DI-SINI</gco:CharacterString>
  </gmd:fileIdentifier>
  <gmd:language>
    <gmd:LanguageCode codeList="http://www.loc.gov/standards/iso639-2/"
                      codeListValue="ind">ind</gmd:LanguageCode>
  </gmd:language>
  <gmd:hierarchyLevel>
    <gmd:MD_ScopeCode codeListValue="dataset">dataset</gmd:MD_ScopeCode>
  </gmd:hierarchyLevel>
  <gmd:contact>
    <gmd:CI_ResponsibleParty>
      <gmd:organisationName>
        <gco:CharacterString>Komunitas Pemerhati Data Spasial Publik</gco:CharacterString>
      </gmd:organisationName>
      <gmd:contactInfo>
        <gmd:CI_Contact>
          <gmd:address>
            <gmd:CI_Address>
              <gmd:electronicMailAddress>
                <gco:CharacterString>geospatial@ahliweb.id</gco:CharacterString>
              </gmd:electronicMailAddress>
            </gmd:CI_Address>
          </gmd:address>
        </gmd:CI_Contact>
      </gmd:contactInfo>
      <gmd:role>
        <gmd:CI_RoleCode codeListValue="pointOfContact">pointOfContact</gmd:CI_RoleCode>
      </gmd:role>
    </gmd:CI_ResponsibleParty>
  </gmd:contact>
  <gmd:dateStamp><gco:Date>2026-05-26</gco:Date></gmd:dateStamp>
  <gmd:metadataStandardName>
    <gco:CharacterString>SNI ISO 19115-3:2019</gco:CharacterString>
  </gmd:metadataStandardName>

  <gmd:identificationInfo>
    <gmd:MD_DataIdentification>
      <gmd:citation>
        <gmd:CI_Citation>
          <gmd:title>
            <gco:CharacterString>
              Fasilitas Kesehatan Kabupaten Kotawaringin Barat
            </gco:CharacterString>
          </gmd:title>
          <gmd:date>
            <gmd:CI_Date>
              <gmd:date><gco:Date>2026-05-26</gco:Date></gmd:date>
              <gmd:dateType>
                <gmd:CI_DateTypeCode codeListValue="creation">creation</gmd:CI_DateTypeCode>
              </gmd:dateType>
            </gmd:CI_Date>
          </gmd:date>
        </gmd:CI_Citation>
      </gmd:citation>
      <gmd:abstract>
        <gco:CharacterString>
          Titik lokasi fasilitas kesehatan di Kabupaten Kotawaringin Barat.
          Mencakup rumah sakit, puskesmas, klinik, posyandu, pustu, dan apotek.
        </gco:CharacterString>
      </gmd:abstract>
      <gmd:pointOfContact><!-- Salin dari template --></gmd:pointOfContact>
      <gmd:descriptiveKeywords>
        <gmd:MD_Keywords>
          <gmd:keyword><gco:CharacterString>Fasilitas Kesehatan</gco:CharacterString></gmd:keyword>
          <gmd:keyword><gco:CharacterString>Puskesmas</gco:CharacterString></gmd:keyword>
          <gmd:keyword><gco:CharacterString>Rumah Sakit</gco:CharacterString></gmd:keyword>
        </gmd:MD_Keywords>
      </gmd:descriptiveKeywords>
    </gmd:MD_DataIdentification>
  </gmd:identificationInfo>
</gmd:MD_Metadata>
```

> Pakai template lengkap dari `metadata/batas_admin_metadata.xml` lalu sesuaikan isinya.

---

## 5. QGIS Project

Update project `kobar_infrastruktur.qgs`:

1. **Buka di QGIS**: `kobar_infrastruktur.qgs`
2. **Tambah layer**: `Layer > Add Layer > Add Vector Layer` → pilih `shapefiles/faskes.shp`
3. **Atur style**:
   - Klik kanan layer → Properties → Symbology
   - Pilih **Categorized** → Column: `kategori`
   - Warna:
     ```
     rumah_sakit → #E31A1C (merah)
     puskesmas   → #1F78B4 (biru)
     klinik      → #33A02C (hijau)
     posyandu    → #FF7F00 (oranye)
     apotek      → #6A3D9A (ungu)
     pustu       → #B15928 (coklat)
     ```
4. **Label**: Properties → Labels → Single Labels → Column: `nama`
5. **Simpan project**

---

## 6. PyQGIS — Pengolahan Lanjutan

### Ekspor SVG/PNG per kecamatan

```python
# export_faskes.py
import os
from qgis.core import *

project = QgsProject.instance()
project.read('kobar_infrastruktur.qgs')

layer = project.mapLayersByName('faskes')[0]
kec_layer = project.mapLayersByName('kecamatan')[0]

os.makedirs('output/faskes', exist_ok=True)

for kec_feat in kec_layer.getFeatures():
    nama_kec = kec_feat['nama']
    geom_kec = kec_feat.geometry()
    bbox = geom_kec.boundingBox()
    bbox.scale(1.1)

    # Setting renderer
    settings = QgsMapSettings()
    settings.setLayers([kec_layer, layer])
    settings.setExtent(QgsRectangle(bbox))
    settings.setOutputSize(QSize(1600, 1200))
    settings.setBackgroundColor(QColor(255, 255, 255))

    render = QgsMapRendererParallelJob(settings)
    render.start()
    render.waitForFinished()
    image = render.renderedImage()
    image.save(f'output/faskes/kec_{nama_kec}.png')

    print(f'✓ {nama_kec}')

print('Done — check output/faskes/')
```

### Analisis buffer (radius layanan)

```python
from qgis.core import *
from qgis.analysis import QgsGeometryAnalyzer

# Buat buffer 3 km dari setiap puskesmas
QgsGeometryAnalyzer().buffer(
    layer,                    # source
    'output/buffer_pkm.shp',  # output
    0.03,                     # 3 km dalam derajat (~0.03°)
    False, True, -1
)
```

### Join dengan batas desa

```python
# Hitung jumlah faskes per desa
import processing
result = processing.run("qgis:countpointsinpolygon", {
    'POLYGONS': 'shapefiles/desa.shp',
    'POINTS': 'shapefiles/faskes.shp',
    'OUTPUT': 'output/desa_faskes_count.shp'
})
```

---

## 7. Validasi Sebelum Upload

```bash
# 1. Cek jumlah fitur
ogrinfo -so shapefiles/faskes.shp faskes | grep "Feature Count"

# 2. Cek field
ogrinfo -so shapefiles/faskes.shp faskes | grep "String\|Integer\|Real"

# 3. Cek extent (pastikan dalam area Kotawaringin Barat)
ogrinfo -so shapefiles/faskes.shp faskes | grep "Extent"
# Output seharusnya dalam rentang: lon 111.0-112.2, lat -3.5 sampai -1.5

# 4. Validasi kategori tidak kosong
python3 -c "
from osgeo import ogr
ds = ogr.Open('shapefiles/faskes.shp')
l = ds.GetLayer(0)
for f in l:
    kat = f.GetField('kategori')
    nama = f.GetField('nama')
    if not kat:
        print(f'  ⚠️  {nama}: kategori KOSONG')
    if not nama:
        print(f'  ⚠️  kategori={kat}: nama KOSONG')
print('Validasi selesai')
ds = None
"

# 5. Validasi metadata XML
python3 -c "import xml.etree.ElementTree as ET; ET.parse('metadata/faskes_metadata.xml'); print('Metadata valid')"
```

---

## 8. Checklist Upload Geoportal

| Item | Status |
|------|--------|
| Shapefile (`shapefiles/faskes.shp/.shx/.dbf/.prj/.cpg`) | ☐ |
| GeoPackage (`data/kobar.gpkg` layer `faskes`) | ☐ |
| Project QGIS terupdate | ☐ |
| Metadata ISO 19139 (UUID, LanguageCode) | ☐ |
| Semua field `nama` terisi | ☐ |
| Semua field `kategori` terisi | ☐ |
| Koordinat dalam rentang Kotawaringin Barat | ☐ |
| Tidak ada fitur di luar area kabupaten | ☐ |
| VERSION di-bump | ☐ |
| CHANGELOG di-update | ☐ |

---

## 9. Referensi

- Template CSV: `docs/contoh/faskes_contoh.csv`
- Template metadata: `metadata/batas_admin_metadata.xml`
- PyQGIS script: `scripts/export_batas_admin.py`
- Daftar faskes Dinkes: [dinkes.kotawaringinbaratkab.go.id](https://dinkes.kotawaringinbaratkab.go.id)
- Faskes dari OSM: query `amenity=hospital`, `amenity=clinic`, `amenity=doctors`
