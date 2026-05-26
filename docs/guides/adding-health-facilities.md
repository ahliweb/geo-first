# Guide — Adding Health Facility Points

Step-by-step guide for adding health facility data (puskesmas, hospitals, clinics, posyandu, pharmacies) to this repository, ready for PALAPA geoportal upload and PyQGIS processing.

The map generator prefers the project GeoPackage when available and uses the village/sub-district base map (`kabupaten`, `kecamatan`, `desa`) by default.

---

## 1. Data Structure

### Format
Projection **EPSG:4326** (WGS 84), encoding **UTF-8**.

### Required Fields
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `osm_id` | String | Unique ID (use facility code if available) | `PUSK_KUMAI_01` |
| `nama` | String | Facility name | `Puskesmas Kumai` |
| `kategori` | String | Facility type | `puskesmas` / `rumah_sakit` |
| `sub_kategori` | String | Sub-type | `puskesmas_rawat_inap` |
| `operator` | String | Operator/manager | `Dinas Kesehatan Kobar` |
| `alamat` | String | Full address | `Jl. HM Idris No.10, Kumai` |
| `kecamatan` | String | Kecamatan name | `Kumai` |
| `desa` | String | Village/kelurahan name | `Kumai Hulu` |
| `telepon` | String | Phone number | `0532-xxxxx` |
| `sumber` | String | Data source | `Dinkes Kobar` / `OSM` / `BPS` |

### Standard Categories
| `kategori` | `sub_kategori` | Description |
|-----------|----------------|-------------|
| `rumah_sakit` | `rs_umum` | General hospital type A/B/C/D |
| `rumah_sakit` | `rs_khusus` | Specialized hospital (maternity, psychiatric, etc.) |
| `puskesmas` | `puskesmas_rawat_inap` | Puskesmas with inpatient care |
| `puskesmas` | `puskesmas_non_rawat` | Puskesmas without inpatient care |
| `klinik` | `klinik_umum` | General clinic |
| `klinik` | `klinik_gigi` | Dental clinic |
| `klinik` | `praktek_dokter` | Doctor practice |
| `posyandu` | `posyandu` | Integrated healthcare post |
| `apotek` | `apotek` | Pharmacy |
| `pustu` | `pustu` | Village health post |

---

## 2. Add Data

### Option A: CSV → Shapefile

1. Create CSV file at `projects/<name>/data/faskes.csv` (or reuse the project GeoPackage when the project is already built):

```csv
osm_id,nama,kategori,sub_kategori,operator,alamat,kecamatan,desa,telepon,sumber,lon,lat
PUSK_KUMAI_01,Puskesmas Kumai,puskesmas,puskesmas_rawat_inap,Dinkes Kobar,Jl. HM Idris No.10,Kumai,Kumai Hulu,0532-xxxxx,Dinkes Kobar,111.7345,-2.7567
```

2. Create VRT file at `projects/<name>/data/faskes.vrt`:

```xml
<OGRVRTDataSource>
    <OGRVRTLayer name="faskes">
        <SrcDataSource>./faskes.csv</SrcDataSource>
        <GeometryType>wkbPoint</GeometryType>
        <LayerSRS>EPSG:4326</LayerSRS>
        <GeometryField encoding="PointFromColumns" x="lon" y="lat"/>
    </OGRVRTLayer>
</OGRVRTDataSource>
```

3. Convert to Shapefile:

```bash
ogr2ogr -f "ESRI Shapefile" \
  projects/<name>/shapefiles/faskes.shp \
  projects/<name>/data/faskes.vrt \
  -lco ENCODING=UTF-8
```

### Option B: GeoJSON → Shapefile

```bash
ogr2ogr -f "ESRI Shapefile" \
  projects/<name>/shapefiles/faskes.shp \
  projects/<name>/data/faskes.geojson \
  -lco ENCODING=UTF-8
```

---

## 3. Generate Map

```bash
python3 shared/scripts/generate_professional_map.py \
  --project projects/<name> \
  --sector health \
  --layers faskes \
  --output-format png,pdf,svg \
  --dpi 300
```

The map base uses `kabupaten`, `kecamatan`, and `desa` as the administrative reference.
The generator will overwrite files with matching names in `output/`.

Output files will be placed in `projects/<name>/output/`.

---

## 4. Create Metadata

Copy and adapt the template:

```bash
python3 shared/scripts/generate_big_metadata.py \
  --template shared/metadata/batas_admin_metadata.xml \
  --output projects/<name>/metadata/faskes_metadata.xml \
  --title "Peta Fasilitas Kesehatan Kabupaten Kotawaringin Barat" \
  --abstract "Dataset fasilitas kesehatan Kabupaten Kotawaringin Barat untuk peta tematik dan Geoportal BIG/PALAPA." \
  --source "Community dataset prepared for SOPD and BIG-ready workflows." \
  --bbox "111.2648,-3.53397,112.0905,-1.56283"
```

Required updates:
- **FileIdentifier**: Generate new UUID
- **Title**: Facility map title
- **Abstract**: Description of the dataset
- **Keywords**: health, facilities, puskesmas, hospital
- **Extent**: Update coordinates
- **Date**: Current date
- **Source**: Cite data source (Dinkes, OSM, etc.)

Validate:

```bash
python3 -c "import xml.etree.ElementTree as ET; ET.parse('projects/<name>/metadata/faskes_metadata.xml')"
```

---

## 5. Verify Data

```bash
# Check feature count
ogrinfo projects/<name>/shapefiles/faskes.shp faskes

# Check fields
ogrinfo -so projects/<name>/shapefiles/faskes.shp faskes

# Validate geometry
ogr2ogr -f "ESRI Shapefile" /dev/null projects/<name>/shapefiles/faskes.shp -nln faskes
```

---

## 6. Commit & Push

```bash
git add projects/<name>/
git commit -m "feat: add health facilities for <project-name>"
git push
```

---

## License

This project is licensed under the **AW Non-Commercial License 1.0**.
See [../../LICENSE.md](../../LICENSE.md) for the full legal text.

For commercial licensing inquiries, contact: [commercial@ahliweb.com](mailto:commercial@ahliweb.com)
