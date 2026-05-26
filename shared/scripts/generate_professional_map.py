#!/usr/bin/env python3
"""
Professional Map Generator for Geospatial Projects
Generates publication-quality maps (PNG/PDF/SVG) from QGIS layouts.

Licensed under the AW Non-Commercial License 1.0.
See LICENSE.md in the repository root for the full legal text.

Usage:
    python3 shared/scripts/generate_professional_map.py \
        --project projects/faskes-kobar \
        --layers admin,roads,faskes \
        --output-format png,pdf,svg \
        --dpi 300
"""

import os
import sys
import json
import argparse
import uuid
import subprocess
import warnings
from pathlib import Path

os.environ['QT_QPA_PLATFORM'] = 'offscreen'
warnings.filterwarnings('ignore', category=FutureWarning)

from qgis.core import *
from qgis.PyQt.QtCore import QRectF
from qgis.PyQt.QtGui import QColor, QFont

# ============================================================
# INITIALIZATION
# ============================================================

QgsApplication.setPrefixPath('/usr', True)
qgs = QgsApplication([], False)
qgs.initQgis()

REPO_ROOT = Path(__file__).resolve().parents[2]
SHARED_ROOT = REPO_ROOT / 'shared'
PROFILE_PATH = SHARED_ROOT / 'config' / 'sector_profiles.json'


def load_layer(path, name=None):
    """Load a vector layer with validation."""
    layer_name = name or Path(path).stem.title()
    layer = QgsVectorLayer(path, layer_name, 'ogr')
    if not layer.isValid():
        print(f"  ⚠ Invalid layer: {path}")
        return None
    return layer


def load_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding='utf-8'))


def gpkg_layer_names(path):
    try:
        from osgeo import ogr
    except Exception:
        return set()
    if not path.exists():
        return set()
    ds = ogr.Open(str(path))
    if ds is None:
        return set()
    names = {ds.GetLayerByIndex(i).GetName() for i in range(ds.GetLayerCount())}
    ds = None
    return names


def resolve_profile(sector=None):
    profiles = load_json(PROFILE_PATH)
    if sector and sector in profiles:
        return profiles[sector]
    return profiles.get('admin', {
        'title': 'Peta Administrasi',
        'subtitle': 'Kabupaten Kotawaringin Barat, Kalimantan Tengah',
        'output_prefix': 'peta_admin_kobar',
        'base_layers': ['kabupaten', 'kecamatan', 'desa'],
        'context_layers': [],
        'thematic_layers': [],
        'base_label_field': 'nama',
        'notes': 'Administrative base map.'
    })


def unique_ordered(items):
    seen = set()
    result = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def style_kabupaten(layer):
    """Apply kabupaten background style."""
    layer.renderer().setSymbol(QgsFillSymbol.createSimple({
        'color': '#f5f5f0',
        'outline_color': '#4d4d4d',
        'outline_width': '0.9'
    }))


def style_kecamatan(layer):
    """Apply kecamatan border style with labels."""
    layer.renderer().setSymbol(QgsFillSymbol.createSimple({
        'color': 'transparent',
        'outline_color': '#707070',
        'outline_width': '0.55'
    }))

    # Labels
    ls = QgsPalLayerSettings()
    ls.fieldName = 'nama'
    ls.enabled = True
    ls.placement = QgsPalLayerSettings.OverPoint
    ls.priority = 3
    ls.dist = 1.5

    fmt = QgsTextFormat()
    fmt.setFont(QFont('Sans Serif', 9, QFont.Bold))
    fmt.setSize(9)
    fmt.setColor(QColor(80, 80, 80))
    ls.setFormat(fmt)

    layer.setLabelsEnabled(True)
    layer.setLabeling(QgsVectorLayerSimpleLabeling(ls))


def style_desa(layer):
    """Apply village boundary style as the cartographic base."""
    layer.renderer().setSymbol(QgsFillSymbol.createSimple({
        'color': 'transparent',
        'outline_color': '#b5b5b5',
        'outline_width': '0.22',
        'outline_style': 'dash'
    }))

    ls = QgsPalLayerSettings()
    ls.fieldName = 'nama'
    ls.enabled = True
    ls.placement = QgsPalLayerSettings.OverPoint
    ls.priority = 1

    fmt = QgsTextFormat()
    fmt.setFont(QFont('Sans Serif', 6))
    fmt.setSize(6)
    fmt.setColor(QColor(110, 110, 110))
    ls.setFormat(fmt)

    layer.setLabelsEnabled(True)
    layer.setLabeling(QgsVectorLayerSimpleLabeling(ls))


def style_roads(layer):
    """Apply road network style."""
    layer.renderer().setSymbol(QgsLineSymbol.createSimple({
        'color': '#cccccc',
        'width': '0.15',
        'cap': 'round',
        'join': 'round'
    }))


def style_waterways(layer):
    """Apply waterway style."""
    layer.renderer().setSymbol(QgsLineSymbol.createSimple({
        'color': '#a6cee3',
        'width': '0.3',
        'cap': 'round',
        'join': 'round'
    }))


def style_buildings(layer):
    """Apply building footprint style."""
    layer.renderer().setSymbol(QgsFillSymbol.createSimple({
        'color': '#e8e8e8',
        'outline_color': '#d0d0d0',
        'outline_width': '0.05'
    }))


def style_faskes(layer):
    """Apply health facility categorized style."""
    cats = {
        'rumah_sakit': ('Rumah Sakit', '#d73027', 8),
        'puskesmas': ('Puskesmas', '#4575b4', 6.5),
        'klinik': ('Klinik', '#1a9850', 5.5),
        'posyandu': ('Posyandu', '#f46d43', 4.5),
        'apotek': ('Apotek', '#91219e', 4.5),
        'pustu': ('Pustu', '#663399', 4),
    }

    renderer = QgsCategorizedSymbolRenderer('kategori')
    for val, (label, color, size) in cats.items():
        sym = QgsMarkerSymbol.createSimple({
            'name': 'circle',
            'color': color,
            'size': str(size),
            'outline_color': '#ffffff',
            'outline_width': '1.0'
        })
        renderer.addCategory(QgsRendererCategory(val, sym, label, True))

    layer.setRenderer(renderer)

    # Labels
    fl = QgsPalLayerSettings()
    fl.fieldName = 'nama'
    fl.enabled = True
    fl.placement = QgsPalLayerSettings.OverPoint
    fl.priority = 5
    fl.dist = 1.0
    fl.yOffset = 2.5

    ff = QgsTextFormat()
    ff.setFont(QFont('Sans Serif', 7))
    ff.setSize(7)
    ff.setColor(QColor(30, 30, 30))
    fl.setFormat(ff)

    layer.setLabelsEnabled(True)
    layer.setLabeling(QgsVectorLayerSimpleLabeling(fl))


def style_generic_point(layer, color='#333333', size=4):
    """Apply generic point style."""
    layer.renderer().setSymbol(QgsMarkerSymbol.createSimple({
        'name': 'circle',
        'color': color,
        'size': str(size),
        'outline_color': '#ffffff',
        'outline_width': '0.5'
    }))


def style_generic_line(layer, color='#666666', width=0.3):
    """Apply generic line style."""
    layer.renderer().setSymbol(QgsLineSymbol.createSimple({
        'color': color,
        'width': str(width),
        'cap': 'round',
        'join': 'round'
    }))


def style_generic_polygon(layer, fill='#f0f0f0', outline='#999999'):
    """Apply generic polygon style."""
    layer.renderer().setSymbol(QgsFillSymbol.createSimple({
        'color': fill,
        'outline_color': outline,
        'outline_width': '0.3'
    }))


# Style registry
STYLE_REGISTRY = {
    'kabupaten': style_kabupaten,
    'kecamatan': style_kecamatan,
    'desa': style_desa,
    'roads': style_roads,
    'waterways': style_waterways,
    'buildings': style_buildings,
    'faskes': style_faskes,
    'poi': lambda l: style_generic_point(l, '#ff7f00', 3),
    'landuse': lambda l: style_generic_polygon(l, '#e8f5e8', '#a0d0a0'),
}


def apply_style(layer, style_name=None):
    """Apply appropriate style based on layer name."""
    name = style_name or layer.name().lower()
    for key, styler in STYLE_REGISTRY.items():
        if key in name:
            styler(layer)
            return
    # Default style based on geometry type
    geom_type = layer.geometryType()
    if geom_type == QgsWkbTypes.PointGeometry:
        style_generic_point(layer)
    elif geom_type == QgsWkbTypes.LineGeometry:
        style_generic_line(layer)
    elif geom_type == QgsWkbTypes.PolygonGeometry:
        style_generic_polygon(layer)


def generate_map(project_dir, sector, layers_config, output_formats, dpi=300):
    """Generate professional map from project directory."""
    project_dir = Path(project_dir)
    output_dir = project_dir / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)

    project = QgsProject.instance()
    profile = resolve_profile(sector)
    base_layers = profile.get('base_layers', ['kabupaten', 'kecamatan', 'desa'])
    context_layers = profile.get('context_layers', [])
    thematic_layers = profile.get('thematic_layers', [])
    wanted_layers = unique_ordered(base_layers + context_layers + thematic_layers + layers_config)

    # ============================================================
    # LOAD LAYERS
    # ============================================================
    loaded_layers = []
    loaded_by_name = {}
    shared_shp = SHARED_ROOT / 'shapefiles'
    project_gpkg = project_dir / 'data' / f"{project_dir.name.replace('-', '_')}.gpkg"
    project_gpkg_layers = gpkg_layer_names(project_gpkg)

    for layer_name in wanted_layers:
        # Try project GeoPackage first so each project can stay self-contained.
        if project_gpkg.exists() and layer_name in project_gpkg_layers:
            gpkg_source = f"{project_gpkg}|layername={layer_name}"
            lyr = load_layer(gpkg_source, layer_name.title())
            if lyr:
                apply_style(lyr, layer_name)
                project.addMapLayer(lyr)
                loaded_layers.append(lyr)
                loaded_by_name[layer_name] = lyr
                continue

        # Try project-specific shapefile first
        proj_shp = project_dir / 'shapefiles' / f'{layer_name}.shp'
        if proj_shp.exists():
            lyr = load_layer(str(proj_shp), layer_name.title())
            if lyr:
                apply_style(lyr, layer_name)
                project.addMapLayer(lyr)
                loaded_layers.append(lyr)
                loaded_by_name[layer_name] = lyr
                continue

        # Try shared shapefile
        shared_path = shared_shp / f'{layer_name}.shp'
        if shared_path.exists():
            lyr = load_layer(str(shared_path), layer_name.title())
            if lyr:
                apply_style(lyr, layer_name)
                project.addMapLayer(lyr)
                loaded_layers.append(lyr)
                loaded_by_name[layer_name] = lyr
                continue

        print(f"  ⚠ Layer not found: {layer_name}")

    if not loaded_layers:
        print("✗ No valid layers loaded. Aborting.")
        return

    print("⚠ Warning: existing output files with the same names will be overwritten.")

    # ============================================================
    # DETERMINE EXTENT
    # ============================================================
    # Use the administrative base map for extent where possible.
    extent_layer = (
        loaded_by_name.get('kabupaten')
        or loaded_by_name.get('desa')
        or loaded_by_name.get('kecamatan')
        or loaded_layers[0]
    )

    ext = extent_layer.extent()
    pad_x = (ext.xMaximum() - ext.xMinimum()) * 0.08
    pad_y = (ext.yMaximum() - ext.yMinimum()) * 0.08
    full_ext = QgsRectangle(
        ext.xMinimum() - pad_x, ext.yMinimum() - pad_y,
        ext.xMaximum() + pad_x, ext.yMaximum() + pad_y
    )

    # ============================================================
    # LAYOUT SETUP
    # ============================================================
    mgr = project.layoutManager()
    for old in list(mgr.layouts()):
        mgr.removeLayout(old)

    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    try:
        layout.setName(f"{profile.get('output_prefix') or project_dir.name}_layout")
    except Exception:
        pass
    page = layout.pageCollection().page(0)
    page.setPageSize(QgsLayoutSize(297, 210, QgsUnitTypes.LayoutMillimeters))

    MARGIN = 8
    MAP_TOP = 32
    MAP_LEFT = MARGIN
    MAP_WIDTH = 195
    MAP_HEIGHT = 160

    # Main map
    main_map = QgsLayoutItemMap(layout)
    main_map.setRect(QRectF(MAP_LEFT, MAP_TOP, MAP_WIDTH, MAP_HEIGHT))
    main_map.setFrameEnabled(True)
    main_map.setFrameStrokeColor(QColor(70, 70, 70))
    main_map.setFrameStrokeWidth(QgsLayoutMeasurement(0.5, QgsUnitTypes.LayoutMillimeters))
    main_map.setExtent(full_ext)
    main_map.setKeepLayerSet(True)
    main_map.setLayers(loaded_layers)
    layout.addLayoutItem(main_map)

    # Title
    title_text = (
        '<div style="font-family: Sans Serif, sans-serif;">'
        f'<b style="font-size: 18pt; color: #1a1a1a;">{profile.get("title", "PETA").upper()}</b><br>'
        f'<span style="font-size: 12pt; color: #555555;">{profile.get("subtitle", "Kabupaten Kotawaringin Barat, Kalimantan Tengah")}</span>'
        '</div>'
    )
    title = QgsLayoutItemLabel(layout)
    title.setText(title_text)
    title.adjustSizeToText()
    title.attemptMove(QgsLayoutPoint(MARGIN, 6, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(title)

    # Sector / standards note.
    note = QgsLayoutItemLabel(layout)
    note.setText(
        '<div style="font-family: Sans Serif, sans-serif; font-size: 6.5pt; color: #666;">'
        'BIG-compliant base map: kabupaten, kecamatan, desa | EPSG:4326 | Geoportal-ready'
        '</div>'
    )
    note.adjustSizeToText()
    note.attemptMove(QgsLayoutPoint(MARGIN, 18, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(note)

    # North arrow
    north = QgsLayoutItemPicture(layout)
    north.setPicturePath('/usr/share/qgis/svg/north_arrows/default.svg')
    north.attemptResize(QgsLayoutSize(15, 20, QgsUnitTypes.LayoutMillimeters))
    north.attemptMove(QgsLayoutPoint(MAP_LEFT + MAP_WIDTH - 22, MAP_TOP + 8, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(north)

    # Scale bar
    scalebar = QgsLayoutItemScaleBar(layout)
    scalebar.setStyle('Line Ticks Up')
    scalebar.setLinkedMap(main_map)
    scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
    scalebar.setNumberOfSegments(2)
    scalebar.setNumberOfSegmentsLeft(0)
    scalebar.setUnitLabel('km')
    scalebar.attemptMove(QgsLayoutPoint(MAP_LEFT + 5, MAP_TOP + MAP_HEIGHT + 5, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(scalebar)

    # Legend
    legend = QgsLayoutItemLegend(layout)
    legend.setTitle('Legenda')
    legend.setLinkedMap(main_map)
    legend.setFrameEnabled(True)
    legend.setFrameStrokeColor(QColor(100, 100, 100))
    legend.setFrameStrokeWidth(QgsLayoutMeasurement(0.3, QgsUnitTypes.LayoutMillimeters))
    legend.setBackgroundColor(QColor(255, 255, 255, 245))
    legend.setSymbolHeight(4)
    legend.setSymbolWidth(5)
    legend.setColumnSpace(3)

    root = QgsLayerTree()
    admin_group = root.addGroup('Administrative Base Map')
    for layer_name in ['kabupaten', 'desa', 'kecamatan']:
        lyr = loaded_by_name.get(layer_name)
        if lyr:
            admin_group.addLayer(lyr)

    context_group = root.addGroup('Context Layers')
    for layer_name in context_layers:
        lyr = loaded_by_name.get(layer_name)
        if lyr:
            context_group.addLayer(lyr)

    thematic_group = root.addGroup('Thematic Layers')
    for layer_name in thematic_layers + [l for l in layers_config if l not in base_layers + context_layers + thematic_layers]:
        lyr = loaded_by_name.get(layer_name)
        if lyr:
            thematic_group.addLayer(lyr)

    legend.model().setRootGroup(root)
    legend.adjustBoxSize()

    leg_w = legend.sizeWithUnits().width()
    leg_h = legend.sizeWithUnits().height()
    legend.attemptMove(QgsLayoutPoint(
        MAP_LEFT + MAP_WIDTH - leg_w - 5,
        MAP_TOP + MAP_HEIGHT - leg_h - 5,
        QgsUnitTypes.LayoutMillimeters
    ))
    layout.addLayoutItem(legend)

    # Footer
    footer = QgsLayoutItemLabel(layout)
    footer.setText(
        '<div style="font-family: Sans Serif, sans-serif; font-size: 6pt; color: #888888;">'
        'Sumber Data: Kotawaringin Barat Geospatial Community &nbsp;|&nbsp; '
        'Standar: SNI ISO 19115-3:2019 / BIG &nbsp;|&nbsp; '
        'Proyeksi: EPSG:4326 (WGS 84) &nbsp;|&nbsp; '
        'Dibuat: 2026'
        '</div>'
    )
    footer.adjustSizeToText()
    footer.attemptMove(QgsLayoutPoint(MARGIN, MAP_TOP + MAP_HEIGHT + 5, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(footer)

    if layout not in mgr.layouts():
        mgr.addLayout(layout)

    # ============================================================
    # EXPORT
    # ============================================================
    exp = QgsLayoutExporter(layout)
    base_name = profile.get('output_prefix') or f'peta_{project_dir.name}'
    temp_dir = Path('/tmp/opencode/geospatial_exports')
    temp_dir.mkdir(parents=True, exist_ok=True)

    for fmt in output_formats:
        fmt = fmt.lower().strip()
        out_path = output_dir / f'{base_name}.{fmt}'
        tmp_path = temp_dir / f'{base_name}.{uuid.uuid4().hex}.{fmt}'

        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass
        if out_path.exists():
            try:
                out_path.unlink()
            except Exception:
                pass
        for extra_suffix in ('.aux.xml', '.ovr', '.wld'):
            extra_path = Path(str(out_path) + extra_suffix)
            if extra_path.exists():
                try:
                    extra_path.unlink()
                except Exception:
                    pass

        if fmt == 'png':
            tmp_pdf = temp_dir / f'{base_name}.{uuid.uuid4().hex}.pdf'
            pdf_settings = QgsLayoutExporter.PdfExportSettings()
            pdf_result = exp.exportToPdf(str(tmp_pdf), pdf_settings)
            if pdf_result == QgsLayoutExporter.Success:
                tmp_png_base = temp_dir / f'{base_name}.{uuid.uuid4().hex}'
                cmd = ['pdftoppm', '-png', '-singlefile', '-r', str(dpi), str(tmp_pdf), str(tmp_png_base)]
                proc = subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result = QgsLayoutExporter.Success if proc.returncode == 0 else proc.returncode
                tmp_path = Path(str(tmp_png_base) + '.png')
            else:
                result = pdf_result
        elif fmt == 'pdf':
            settings = QgsLayoutExporter.PdfExportSettings()
            result = exp.exportToPdf(str(tmp_path), settings)
        elif fmt == 'svg':
            settings = QgsLayoutExporter.SvgExportSettings()
            result = exp.exportToSvg(str(tmp_path), settings)
        else:
            print(f"  ⚠ Unsupported format: {fmt}")
            continue

        if result == QgsLayoutExporter.Success:
            if tmp_path.exists():
                tmp_path.replace(out_path)
            if fmt == 'png':
                try:
                    tmp_pdf.unlink(missing_ok=True)
                except Exception:
                    pass
            size_kb = out_path.stat().st_size / 1024
            print(f'  ✓ {fmt.upper()}: {size_kb:.0f} KB → {out_path}')
        else:
            print(f'  ✗ Export failed: {fmt}')

    qgis_dir = project_dir / 'qgis'
    qgis_dir.mkdir(parents=True, exist_ok=True)
    qgs_path = qgis_dir / f'{base_name}.qgs'
    if project.write(str(qgs_path)):
        qgs_text = qgs_path.read_text(encoding='utf-8')
        rel_shared = os.path.relpath((SHARED_ROOT / 'shapefiles').resolve(), qgis_dir.resolve())
        rel_project_gpkg = os.path.relpath(project_gpkg.resolve(), qgis_dir.resolve()) if project_gpkg.exists() else ''
        rel_project = os.path.relpath((project_dir / 'shapefiles').resolve(), qgis_dir.resolve())
        qgs_text = qgs_text.replace(str((SHARED_ROOT / 'shapefiles').resolve()), rel_shared)
        if rel_project_gpkg:
            qgs_text = qgs_text.replace(str(project_gpkg.resolve()), rel_project_gpkg)
        qgs_text = qgs_text.replace(str((project_dir / 'shapefiles').resolve()), rel_project)
        qgs_text = qgs_text.replace(f'{project_dir.as_posix()}/shapefiles', '../shapefiles')
        qgs_path.write_text(qgs_text, encoding='utf-8')
        print(f'  ✓ QGIS project: {qgs_path}')
    else:
        print(f'  ⚠ Failed to write QGIS project: {qgs_path}')


def main():
    parser = argparse.ArgumentParser(description='Generate professional geospatial maps')
    parser.add_argument('--project', required=True, help='Project directory path')
    parser.add_argument('--sector', default='admin', help='Sector profile name (admin, health, infrastructure, education, public_works, agriculture)')
    parser.add_argument('--layers', default='', help='Comma-separated extra layer names')
    parser.add_argument('--output-format', default='png,pdf,svg', help='Output formats (comma-separated)')
    parser.add_argument('--dpi', type=int, default=300, help='DPI for PNG export')

    args = parser.parse_args()

    layers = [l.strip() for l in args.layers.split(',') if l.strip()]
    formats = [f.strip() for f in args.output_format.split(',')]

    print(f"Generating map for: {args.project}")
    print(f"Sector profile: {args.sector}")
    print(f"Layers: {', '.join(layers)}")
    print(f"Formats: {', '.join(formats)}")
    print(f"DPI: {args.dpi}")
    print()

    generate_map(args.project, args.sector, layers, formats, args.dpi)

    qgs.exitQgis()
    print('\n✓ Map generation complete.')


if __name__ == '__main__':
    main()
