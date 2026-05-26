#!/usr/bin/env python3
"""
PyQGIS script for exporting administrative boundary maps of Kotawaringin Barat
to SVG and PNG formats.

Licensed under the AW Non-Commercial License 1.0.
See LICENSE.md in the repository root for the full legal text.

Requirements:
    QGIS 3.x with Python bindings (PyQGIS)
    qgis_process or python3 + osgeo

Usage:
    # From QGIS Python Console:
    exec(open('shared/scripts/export_batas_admin.py').read())

    # From command line (requires QGIS environment):
    python3 shared/scripts/export_batas_admin.py

    # Tanpa QGIS GUI (pakai qgis_process):
    qgis_process run export:printlayouttopdf ...

Output:
    projects/faskes-kobar/output/batas_admin_kobar.png
    projects/faskes-kobar/output/batas_admin_kobar.svg
    projects/faskes-kobar/output/batas_admin_per_kecamatan.png (satu PNG per kecamatan)
"""

import os, sys, subprocess, warnings
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
warnings.filterwarnings('ignore', category=FutureWarning)

# --- CONFIG ---
PROJECT_FILE = REPO_ROOT / 'shared' / 'qgis' / 'batas_admin_kobar.qgs'
OUTPUT_DIR = REPO_ROOT / 'projects' / 'faskes-kobar' / 'output'
EXPORT_DPI = 300
EXPORT_SIZE_MM = (210, 297)  # A4

# --- Setup QGIS environment ---
try:
    from qgis.core import (
        QgsApplication, QgsProject, QgsLayout, QgsLayoutExporter,
        QgsLayoutItemMap, QgsLayoutItemLabel, QgsRectangle,
        QgsUnitTypes, QgsLayoutSize, QgsLayoutPoint,
        QgsLayoutItemLegend, QgsMapSettings, QgsMapRendererCustomPainterJob
    )
    from qgis.PyQt.QtCore import QSize, QRectF
    from qgis.PyQt.QtGui import QPainter, QImage
    QGIS_AVAILABLE = True
except ImportError:
    print("⚠️  PyQGIS not available. Install QGIS 3.x with Python bindings.")
    print("   This script can also run inside QGIS Python Console.")
    QGIS_AVAILABLE = False


def init_qgis(project_path):
    """Initialize QGIS and load project"""
    if not QGIS_AVAILABLE:
        return None, None
    
    qgs = QgsApplication([], False)
    qgs.initQgis()
    
    project = QgsProject.instance()
    if not project.read(project_path):
        print(f"❌ Failed to load project: {project_path}")
        qgs.exitQgis()
        return None, None
    
    print(f"✓ Project loaded: {project.count()} layers")
    return qgs, project


def export_full_map(project, output_base, dpi=300):
    """Export the full administrative map as PNG and SVG"""
    if not QGIS_AVAILABLE:
        return
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Create layout
    manager = project.layoutManager()
    layout_name = 'batas_admin'
    
    # Remove existing layout with same name
    for l in manager.layouts():
        if l.name() == layout_name:
            manager.removeLayout(l)
            break
    
    layout = QgsLayout(project)
    layout.initializeDefaults()
    layout.setName(layout_name)
    
    page = layout.pageCollection().page(0)
    page.setPageSize('A4', QgsLayoutSize.Millimeters)
    
    # Title
    title = QgsLayoutItemLabel(layout)
    title.setText('Batas Administrasi Kabupaten Kotawaringin Barat')
    title.setFont(QgsFontUtils.getStandardTestFont('Bold', 16))
    title.adjustSizeToText()
    title.attemptMove(QgsLayoutPoint(10, 10, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(title)
    
    # Map
    map_item = QgsLayoutItemMap(layout)
    map_item.setRect(QRectF(10, 30, 190, 240))
    
    # Set extent to all layers
    extent = QgsRectangle()
    for layer in project.mapLayers().values():
        if extent.isEmpty():
            extent = layer.extent()
        else:
            extent.combineExtentWith(layer.extent())
    extent.scale(1.05)  # 5% padding
    map_item.setExtent(extent)
    
    layout.addLayoutItem(map_item)
    
    # Legend
    legend = QgsLayoutItemLegend(layout)
    legend.setTitle('Legenda')
    legend.setLinkedMap(map_item)
    legend.attemptMove(QgsLayoutPoint(10, 275, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(legend)
    
    # Export PNG via temp PDF + pdftoppm to avoid PNG driver overwrite issues
    png_path = os.path.join(OUTPUT_DIR, f'{output_base}.png')
    tmp_pdf = os.path.join(OUTPUT_DIR, f'.{output_base}.tmp.pdf')
    exporter = QgsLayoutExporter(layout)
    pdf_result = exporter.exportToPdf(tmp_pdf, QgsLayoutExporter.PdfExportSettings())
    if pdf_result == QgsLayoutExporter.Success:
        tmp_png_base = os.path.join(OUTPUT_DIR, f'.{output_base}.tmp')
        proc = subprocess.run(['pdftoppm', '-png', '-singlefile', '-r', str(dpi), tmp_pdf, tmp_png_base], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode == 0 and os.path.exists(tmp_png_base + '.png'):
            os.replace(tmp_png_base + '.png', png_path)
            print(f'✓ PNG exported: {png_path}')
        else:
            print(f'❌ PNG export failed: pdftoppm returned {proc.returncode}')
    else:
        print(f'❌ PNG export failed: {pdf_result}')
    for path in [tmp_pdf, tmp_png_base + '.png' if "tmp_png_base" in locals() else None]:
        if path and os.path.exists(path):
            os.remove(path)
    
    # Export SVG
    svg_path = os.path.join(OUTPUT_DIR, f'{output_base}.svg')
    svg_settings = QgsLayoutExporter.SvgExportSettings()
    svg_settings.dpi = dpi
    result = exporter.exportToSvg(svg_path, svg_settings)
    if result == QgsLayoutExporter.Success:
        print(f'✓ SVG exported: {svg_path}')
    else:
        print(f'❌ SVG export failed: {result}')
    
    manager.addLayout(layout)
    return layout


def export_per_kecamatan(project, dpi=150):
    """Export one PNG map per kecamatan"""
    if not QGIS_AVAILABLE:
        return
    
    kecamatan_layer = project.mapLayersByName('Kecamatan')
    if not kecamatan_layer:
        print('❌ Kecamatan layer not found')
        return
    
    layer = kecamatan_layer[0]
    
    for feature in layer.getFeatures():
        nama = feature['nama']
        geom = feature.geometry()
        bbox = geom.boundingBox()
        bbox.scale(1.1)
        
        ext = QgsRectangle(bbox)
        
        # Create temp map renderer
        settings = QgsMapSettings()
        settings.setLayers([layer])
        settings.setExtent(ext)
        settings.setOutputSize(QSize(1200, 800))
        settings.setBackgroundColor(Qt.white)
        
        # Render to image
        image = QImage(QSize(1200, 800), QImage.Format_ARGB32)
        image.fill(Qt.white)
        painter = QPainter(image)
        renderer = QgsMapRendererCustomPainterJob(settings, painter)
        renderer.start()
        renderer.waitForFinished()
        painter.end()
        
        filename = os.path.join(OUTPUT_DIR, f'kecamatan_{nama.lower().replace(" ", "_")}.png')
        image.save(filename)
        print(f'  ✓ {nama}: {filename}')


def export_standalone_no_qgis():
    """
    Alternative: export using only GDAL/osgeo (no QGIS required)
    Suitable for headless servers and CI/CD pipelines.
    """
    try:
        from osgeo import ogr, osr, gdal
    except ImportError:
        print('❌ GDAL not available. Install: pip install gdal')
        return
    
    print('\nExporting using GDAL (no QGIS)...')
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Open GeoPackage
    gpkg_path = str(REPO_ROOT / 'shared' / 'data' / 'batas_admin.gpkg')
    ds = ogr.Open(gpkg_path)
    
    svg_header = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1000" width="1200" height="1000">
<style>
  .kabupaten { fill: #e5e6e8; stroke: #464646; stroke-width: 1.5; }
  .kecamatan { fill: none; stroke: #333; stroke-width: 0.8; }
  .kec-label { font-family: sans-serif; font-size: 12px; fill: #333; text-anchor: middle; }
  .title { font-family: sans-serif; font-size: 18px; font-weight: bold; fill: #333; text-anchor: middle; }
</style>
<text x="600" y="30" class="title">Batas Administrasi Kotawaringin Barat</text>
'''
    
    # Transform coordinates to SVG viewport
    layer = ds.GetLayerByName('kabupaten')
    ext = layer.GetExtent()
    
    def geo_to_svg(lon, lat, margin=50):
        x = margin + (lon - ext[0]) / (ext[1] - ext[0]) * (1200 - 2*margin)
        y = margin + (ext[3] - lat) / (ext[3] - ext[2]) * (1000 - 2*margin)
        return x, y
    
    # Build SVG
    svg_lines = [svg_header]
    
    # Kabupaten polygons
    for feat in layer:
        geom = feat.GetGeometryRef()
        for i in range(geom.GetGeometryCount()):
            poly = geom.GetGeometryRef(i)
            ring = poly.GetGeometryRef(0)
            pts = ', '.join(f'{geo_to_svg(pt[0], pt[1])[0]:.1f},{geo_to_svg(pt[0], pt[1])[1]:.1f}' 
                          for pt in ring.GetPoints())
            svg_lines.append(f'<polygon class="kabupaten" points="{pts}"/>')
    
    # Kecamatan polygons with labels
    kec_colors = {
        'Kumai': '#1f78b4', 'Arut Selatan': '#fdbf6f', 
        'Kotawaringin Lama': '#a6cee3', 'Arut Utara': '#dfc27d',
        'Pangkalan Lada': '#fb9a99', 'Pangkalan Banteng': '#b2df8a'
    }
    
    kec_layer = ds.GetLayerByName('kecamatan')
    for feat in kec_layer:
        nama = feat.GetField('nama')
        color = kec_colors.get(nama, '#cccccc')
        geom = feat.GetGeometryRef()
        
        for i in range(geom.GetGeometryCount()):
            poly = geom.GetGeometryRef(i)
            ring = poly.GetGeometryRef(0)
            pts = ', '.join(f'{geo_to_svg(pt[0], pt[1])[0]:.1f},{geo_to_svg(pt[0], pt[1])[1]:.1f}' 
                          for pt in ring.GetPoints())
            svg_lines.append(f'<polygon fill="{color}" fill-opacity="0.3" stroke="#666" stroke-width="0.8" points="{pts}"/>')
        
        # Label at centroid
        centroid = geom.Centroid()
        cx, cy = geo_to_svg(centroid.GetX(), centroid.GetY())
        svg_lines.append(f'<text x="{cx:.1f}" y="{cy:.1f}" class="kec-label">{nama}</text>')
    
    # Pusat kecamatan
    pusat_layer = ds.GetLayerByName('pusat_kecamatan')
    for feat in pusat_layer:
        geom = feat.GetGeometryRef()
        px, py = geo_to_svg(geom.GetX(), geom.GetY())
        svg_lines.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="red" stroke="white" stroke-width="1"/>')
    
    # Add note
    svg_lines.append('<text x="600" y="980" style="font-family:sans-serif;font-size:10px;fill:#999;text-anchor:middle">⚠ Bts Kecmtn: Estimasi komunitas (bukan data resmi BIG/Mendagri)</text>')
    svg_lines.append('</svg>')
    
    svg_path = os.path.join(OUTPUT_DIR, 'batas_admin_kobar.svg')
    with open(svg_path, 'w') as f:
        f.write('\n'.join(svg_lines))
    print(f'✓ SVG exported (GDAL): {svg_path}')
    
    ds = None


# --- MAIN ---
if __name__ == '__main__':
    print('='*60)
    print('  Peta Batas Administrasi - Kotawaringin Barat')
    print('='*60)
    
    if QGIS_AVAILABLE:
        # Full QGIS export
        project_path = str(PROJECT_FILE)
        
        qgs, project = init_qgis(project_path)
        
        if project:
            export_full_map(project, 'batas_admin_kobar')
            export_per_kecamatan(project)
            qgs.exitQgis()
            print(f'\n✓ Done. Check {OUTPUT_DIR}/ directory.')
    else:
        # Fallback: use GDAL only
        export_standalone_no_qgis()
        print('\n✓ Done. For full QGIS export, run inside QGIS Python Console.')
        print('  QGIS Console: Plugins → Python Console → exec(open("shared/scripts/export_batas_admin.py").read())')
