#!/usr/bin/env python3
"""
PyQGIS / GDAL script for exporting health facility maps of Kotawaringin Barat.
Output: SVG, PNG per kecamatan, PDF, and CSV summary statistics.

Licensed under the AW Non-Commercial License 1.0.
See LICENSE.md in the repository root for the full legal text.

Requirements:
    QGIS 3.x (for standardized PNG/PDF/SVG export via shared generator)
    GDAL (for CSV statistics and optional legacy utilities)
    python3

Usage:
    python3 shared/scripts/export_faskes.py

Output:
    projects/faskes-kobar/output/peta_faskes_kobar.png
    projects/faskes-kobar/output/peta_faskes_kobar.pdf
    projects/faskes-kobar/output/peta_faskes_kobar.svg
    projects/faskes-kobar/output/faskes_summary.csv
"""

import os, sys, csv, subprocess, warnings, argparse
from pathlib import Path
from collections import Counter, defaultdict
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_DIR = REPO_ROOT / 'projects' / 'faskes-kobar'
warnings.filterwarnings('ignore', category=FutureWarning)

# --- CONFIG ---
SHAPEFILE_PATH = PROJECT_DIR / 'shapefiles' / 'faskes.shp'
KECAMATAN_SHP = REPO_ROOT / 'shared' / 'shapefiles' / 'kecamatan.shp'
DESA_SHP = REPO_ROOT / 'shared' / 'shapefiles' / 'desa.shp'
OUTPUT_DIR = PROJECT_DIR / 'output'


def configure_paths(project_dir: Optional[Path] = None, shapefile_path: Optional[Path] = None,
                    kecamatan_shp: Optional[Path] = None, desa_shp: Optional[Path] = None,
                    output_dir: Optional[Path] = None) -> None:
    """Override default paths without changing legacy behavior."""
    global PROJECT_DIR, SHAPEFILE_PATH, KECAMATAN_SHP, DESA_SHP, OUTPUT_DIR

    env_project_dir = os.getenv('AWCMS_GEOSPATIAL_PROJECT_DIR') or os.getenv('GEOFIRST_PROJECT_DIR')
    env_shapefile_path = os.getenv('AWCMS_GEOSPATIAL_SHAPEFILE_PATH') or os.getenv('GEOFIRST_SHAPEFILE_PATH')
    env_kecamatan_shp = os.getenv('AWCMS_GEOSPATIAL_KECAMATAN_SHP') or os.getenv('GEOFIRST_KECAMATAN_SHP')
    env_desa_shp = os.getenv('AWCMS_GEOSPATIAL_DESA_SHP') or os.getenv('GEOFIRST_DESA_SHP')
    env_output_dir = os.getenv('AWCMS_GEOSPATIAL_OUTPUT_DIR') or os.getenv('GEOFIRST_OUTPUT_DIR')

    if project_dir is not None:
        PROJECT_DIR = project_dir
    elif env_project_dir:
        PROJECT_DIR = Path(env_project_dir)

    if shapefile_path is not None:
        SHAPEFILE_PATH = shapefile_path
    elif env_shapefile_path:
        SHAPEFILE_PATH = Path(env_shapefile_path)
    else:
        SHAPEFILE_PATH = PROJECT_DIR / 'shapefiles' / 'faskes.shp'

    if kecamatan_shp is not None:
        KECAMATAN_SHP = kecamatan_shp
    elif env_kecamatan_shp:
        KECAMATAN_SHP = Path(env_kecamatan_shp)
    else:
        KECAMATAN_SHP = REPO_ROOT / 'shared' / 'shapefiles' / 'kecamatan.shp'

    if desa_shp is not None:
        DESA_SHP = desa_shp
    elif env_desa_shp:
        DESA_SHP = Path(env_desa_shp)
    else:
        DESA_SHP = REPO_ROOT / 'shared' / 'shapefiles' / 'desa.shp'

    if output_dir is not None:
        OUTPUT_DIR = output_dir
    elif env_output_dir:
        OUTPUT_DIR = Path(env_output_dir)
    else:
        OUTPUT_DIR = PROJECT_DIR / 'output'

# --- GDAL-based SVG export (no QGIS required) ---
def export_svg_gdal():
    """Export SVG map using GDAL only — works without QGIS"""
    try:
        from osgeo import ogr
        ogr.DontUseExceptions()
    except ImportError:
        print("⚠️  GDAL not available. Install: apt install python3-gdal")
        return

    if not SHAPEFILE_PATH.exists():
        print(f"⚠️  {SHAPEFILE_PATH} not found. Create the faskes data first.")
        print("   See docs/guides/adding-health-facilities.md for instructions.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    color_map = {
        'rumah_sakit': '#E31A1C',
        'puskesmas': '#1F78B4',
        'klinik': '#33A02C',
        'posyandu': '#FF7F00',
        'apotek': '#6A3D9A',
        'pustu': '#B15928',
        'polindes': '#FDBF6F',
    }

    ds = ogr.Open(str(SHAPEFILE_PATH))
    layer = ds.GetLayer(0)

    # Hitung extent dari data faskes (fallback ke extent kecamatan)
    ext = layer.GetExtent()
    if ext[0] == 0 and ext[1] == 0:
        if KECAMATAN_SHP.exists():
            kds = ogr.Open(str(KECAMATAN_SHP))
            ext = kds.GetLayer(0).GetExtent()
            kds = None

    def geo_to_svg(lon, lat, w=1000, h=800, margin=40):
        x = margin + (lon - ext[0]) / (ext[1] - ext[0]) * (w - 2*margin)
        y = margin + (ext[3] - lat) / (ext[3] - ext[2]) * (h - 2*margin)
        return x, y

    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 800">')
    svg.append('<style>')
    svg.append('  .bg { fill: #f0f0f0; stroke: #ccc; stroke-width: 0.5; }')
    svg.append('  .point { stroke: white; stroke-width: 1; }')
    svg.append('  .label { font-family: sans-serif; font-size: 8px; fill: #333; text-anchor: middle; }')
    svg.append('  .title { font-family: sans-serif; font-size: 16px; font-weight: bold; text-anchor: middle; }')
    svg.append('</style>')
    svg.append('<text x="500" y="25" class="title">Fasilitas Kesehatan — Kotawaringin Barat</text>')

    # Background: kecamatan boundaries
    if os.path.exists(KECAMATAN_SHP):
        kds = ogr.Open(KECAMATAN_SHP)
        kl = kds.GetLayer(0)
        for feat in kl:
            geom = feat.GetGeometryRef()
            if geom:
                for i in range(geom.GetGeometryCount()):
                    poly = geom.GetGeometryRef(i)
                    ring = poly.GetGeometryRef(0) if poly else None
                    if ring:
                        pts = [f'{geo_to_svg(p[0],p[1])[0]:.1f},{geo_to_svg(p[0],p[1])[1]:.1f}' for p in ring.GetPoints()]
                        svg.append(f'<polygon class="bg" points="{" ".join(pts)}"/>')
        kds = None

    # Kategori → points
    kategori_points = defaultdict(list)
    for feat in layer:
        kat = feat.GetField('kategori') or 'lainnya'
        nama = feat.GetField('nama') or ''
        geom = feat.GetGeometryRef()
        if geom:
            px, py = geo_to_svg(geom.GetX(), geom.GetY())
            color = color_map.get(kat, '#999999')
            kategori_points[kat].append((px, py, nama))

    # Render points
    radius = {'rumah_sakit': 6, 'puskesmas': 5, 'klinik': 4}
    for kat, pts in sorted(kategori_points.items()):
        r = radius.get(kat, 3)
        color = color_map.get(kat, '#999999')
        for px, py, nama in pts:
            svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="{color}" class="point"/>')
            svg.append(f'<text x="{px:.1f}" y="{py-5:.1f}" class="label">{nama}</text>')

    # Legend
    ly = 780
    svg.append(f'<text x="15" y="{ly}" style="font-family:sans-serif;font-size:10px;font-weight:bold">Legenda:</text>')
    for i, (kat, color) in enumerate(sorted(color_map.items())):
        by = ly + 15 + i*15
        svg.append(f'<rect x="15" y="{by-8}" width="10" height="10" fill="{color}"/>')
        svg.append(f'<text x="30" y="{by}" style="font-family:sans-serif;font-size:9px">{kat.replace("_"," ").title()}</text>')

    svg.append('</svg>')

    svg_path = os.path.join(OUTPUT_DIR, 'faskes_kobar.svg')
    with open(svg_path, 'w') as f:
        f.write('\n'.join(svg))
    print(f'✓ SVG: {svg_path}')

    ds = None


# --- CSV Statistics export ---
def export_statistics():
    """Generate CSV summary of facilities per kecamatan/desa"""
    try:
        from osgeo import ogr
    except ImportError:
        return

    if not SHAPEFILE_PATH.exists():
        return

    ds = ogr.Open(str(SHAPEFILE_PATH))
    layer = ds.GetLayer(0)

    per_kec = Counter()
    per_kec_kat = defaultdict(Counter)
    per_desa = Counter()

    for feat in layer:
        kec = feat.GetField('kecamatan') or 'Tidak Diketahui'
        desa = feat.GetField('desa') or 'Tidak Diketahui'
        kat = feat.GetField('kategori') or 'lainnya'
        per_kec[kec] += 1
        per_kec_kat[kec][kat] += 1
        per_desa[f'{kec}|{desa}'] += 1

    ds = None

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    csv_path = os.path.join(OUTPUT_DIR, 'faskes_summary.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Kecamatan', 'Jumlah Faskes', 'Kategori'])
        for kec, n in sorted(per_kec.items()):
            kat_str = '; '.join(f'{k}={v}' for k, v in sorted(per_kec_kat[kec].items()))
            writer.writerow([kec, n, kat_str])

    print(f'✓ CSV summary: {csv_path}')


# --- QGIS-based full export (requires QGIS) ---
def export_qgis():
    """Full export using the shared professional generator."""
    generator = REPO_ROOT / 'shared' / 'scripts' / 'generate_professional_map.py'
    if not generator.exists():
        print(f'❌ Generator not found: {generator}')
        return

    cmd = [
        sys.executable,
        str(generator),
        '--project',
        str(PROJECT_DIR),
        '--sector',
        'health',
        '--layers',
        'faskes',
        '--output-format',
        'png,pdf,svg',
        '--dpi',
        '300',
    ]
    result = subprocess.run(cmd, check=False)
    if result.returncode == 0:
        print('✓ Professional PNG/PDF/SVG exports generated via shared generator')
    else:
        print(f'❌ Professional export failed with code {result.returncode}')


def main(argv=None):
    parser = argparse.ArgumentParser(description='Export health facility maps for Kotawaringin Barat')
    parser.add_argument('--project-dir', type=Path, default=PROJECT_DIR,
                        help='Project directory (default: projects/faskes-kobar)')
    parser.add_argument('--shapefile-path', type=Path, default=None,
                        help='Path to thematic shapefile (default: <project-dir>/shapefiles/faskes.shp)')
    parser.add_argument('--kecamatan-shp', type=Path, default=None,
                        help='Path to kecamatan boundary shapefile')
    parser.add_argument('--desa-shp', type=Path, default=None,
                        help='Path to desa boundary shapefile')
    parser.add_argument('--output-dir', type=Path, default=None,
                        help='Output directory (default: <project-dir>/output)')
    args = parser.parse_args(argv)

    configure_paths(
        project_dir=args.project_dir,
        shapefile_path=args.shapefile_path,
        kecamatan_shp=args.kecamatan_shp,
        desa_shp=args.desa_shp,
        output_dir=args.output_dir,
    )

    print('=' * 55)
    print('  Export Peta Fasilitas Kesehatan')
    print('  Kabupaten Kotawaringin Barat')
    print('=' * 55)

    if SHAPEFILE_PATH.exists():
        export_statistics()
        export_qgis()
    else:
        print(f'\n⚠️  {SHAPEFILE_PATH} belum ada.')
        print('   Ikuti panduan: docs/guides/adding-health-facilities.md')
        print('   untuk membuat data fasilitas kesehatan.')

    print(f'\n✓ Output: {OUTPUT_DIR}/')
    print('  Buka faskes_kobar.svg di browser untuk preview.')


if __name__ == '__main__':
    main()
