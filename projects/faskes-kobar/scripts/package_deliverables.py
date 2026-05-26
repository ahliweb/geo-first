#!/usr/bin/env python3
"""
Package Deliverables for QGIS Desktop and Geoportal Publication.
Creates:
1. qgis_desktop_package.zip: Portable QGIS project and datasets with relative structure.
2. geoportal_metadata_package.zip: ISO 19139 XML metadata and Shapefiles for geoportal upload.

Licensed under the AW Non-Commercial License 1.0.
See LICENSE.md in the repository root for the full legal text.
"""

import os
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
PROJECT_DIR = REPO_ROOT / 'projects' / 'faskes-kobar'
OUTPUT_DIR = PROJECT_DIR / 'output'
LICENSE_PATH = REPO_ROOT / 'LICENSE.md'

def create_qgis_desktop_package():
    zip_path = OUTPUT_DIR / 'qgis_desktop_package.zip'
    if zip_path.exists():
        zip_path.unlink()

    print(f"Creating QGIS Desktop Package at {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 1. Include LICENSE.md
        if LICENSE_PATH.exists():
            zipf.write(LICENSE_PATH, 'LICENSE.md')
            print("  + LICENSE.md")

        # 2. Include QGIS Project File
        qgs_file = PROJECT_DIR / 'qgis' / 'peta_faskes_kobar.qgs'
        if qgs_file.exists():
            arcname = 'projects/faskes-kobar/qgis/peta_faskes_kobar.qgs'
            zipf.write(qgs_file, arcname)
            print(f"  + {arcname}")

        # 3. Include GeoPackage Data
        gpkg_file = PROJECT_DIR / 'data' / 'faskes_kobar.gpkg'
        if gpkg_file.exists():
            arcname = 'projects/faskes-kobar/data/faskes_kobar.gpkg'
            zipf.write(gpkg_file, arcname)
            print(f"  + {arcname}")

        # 4. Include Shared Shapefiles (roads & waterways)
        shared_shp_dir = REPO_ROOT / 'shared' / 'shapefiles'
        for layer in ['roads', 'waterways']:
            for ext in ['.shp', '.shx', '.dbf', '.prj', '.cpg']:
                file_path = shared_shp_dir / f"{layer}{ext}"
                if file_path.exists():
                    arcname = f"shared/shapefiles/{layer}{ext}"
                    zipf.write(file_path, arcname)
                    print(f"  + {arcname}")

    print(f"✓ QGIS Desktop Package successfully created ({zip_path.stat().st_size / 1024:.1f} KB)")


def create_geoportal_metadata_package():
    zip_path = OUTPUT_DIR / 'geoportal_metadata_package.zip'
    if zip_path.exists():
        zip_path.unlink()

    print(f"Creating Geoportal Metadata Package at {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 1. Include LICENSE.md
        if LICENSE_PATH.exists():
            zipf.write(LICENSE_PATH, 'LICENSE.md')
            print("  + LICENSE.md")

        # 2. Include Shapefiles of thematic data
        shp_dir = PROJECT_DIR / 'shapefiles'
        for ext in ['.shp', '.shx', '.dbf', '.prj', '.cpg']:
            file_path = shp_dir / f"faskes{ext}"
            if file_path.exists():
                zipf.write(file_path, f"faskes{ext}")
                print(f"  + faskes{ext}")

        # 3. Include ISO 19139 XML metadata (renamed to faskes.xml to match shapefile)
        xml_file = PROJECT_DIR / 'metadata' / 'faskes_metadata.xml'
        if xml_file.exists():
            zipf.write(xml_file, 'faskes.xml')
            print("  + faskes.xml (from faskes_metadata.xml)")

    print(f"✓ Geoportal Metadata Package successfully created ({zip_path.stat().st_size / 1024:.1f} KB)")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    create_qgis_desktop_package()
    print()
    create_geoportal_metadata_package()
    print("\n✓ Deliverables packaging complete.")

if __name__ == '__main__':
    main()
