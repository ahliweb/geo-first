#!/usr/bin/env python3
"""
Generate BIG-ready ISO 19139 metadata from a repository template.

Licensed under the AW Non-Commercial License 1.0.
See LICENSE.md in the repository root for the full legal text.

The script patches an existing template XML instead of building metadata from
scratch, which keeps the output aligned with the project's ISO 19139 structure.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path


NS = {
    "gmd": "http://www.isotc211.org/2005/gmd",
    "gco": "http://www.isotc211.org/2005/gco",
    "gml": "http://www.opengis.net/gml/3.2",
}

for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def qname(prefix: str, tag: str) -> str:
    return f"{{{NS[prefix]}}}{tag}"


def first(node, path: str):
    return node.find(path, NS)


def all_nodes(node, path: str):
    return node.findall(path, NS)


def set_text(node, path: str, text: str) -> None:
    target = first(node, path)
    if target is not None:
        target.text = text


def pretty_xml(root: ET.Element) -> str:
    try:
        import xml.dom.minidom as minidom

        raw = ET.tostring(root, encoding="utf-8")
        return minidom.parseString(raw).toprettyxml(indent="  ")
    except Exception:
        return ET.tostring(root, encoding="unicode")


def parse_bbox(value: str):
    parts = [p.strip() for p in value.split(",")]
    if len(parts) != 4:
        raise ValueError("bbox must be xmin,ymin,xmax,ymax")
    return tuple(float(p) for p in parts)


def update_extent(root: ET.Element, bbox: tuple[float, float, float, float]) -> None:
    xmin, ymin, xmax, ymax = bbox
    east_bound = str(xmax)
    west_bound = str(xmin)
    north_bound = str(ymax)
    south_bound = str(ymin)

    for path, value in [
        (".//gmd:westBoundLongitude/gco:Decimal", west_bound),
        (".//gmd:eastBoundLongitude/gco:Decimal", east_bound),
        (".//gmd:southBoundLatitude/gco:Decimal", south_bound),
        (".//gmd:northBoundLatitude/gco:Decimal", north_bound),
    ]:
        set_text(root, path, value)


def update_keywords(root: ET.Element, keywords: list[str]) -> None:
    keyword_nodes = all_nodes(root, ".//gmd:keyword/gco:CharacterString")
    if not keyword_nodes:
        return

    for idx, keyword in enumerate(keywords):
        if idx < len(keyword_nodes):
            keyword_nodes[idx].text = keyword


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate BIG-ready ISO 19139 metadata")
    parser.add_argument("--template", required=True, help="Path to ISO 19139 XML template")
    parser.add_argument("--output", required=True, help="Path to write metadata XML")
    parser.add_argument("--title", required=True, help="Dataset title")
    parser.add_argument("--abstract", required=True, help="Dataset abstract")
    parser.add_argument("--source", required=True, help="Source description")
    parser.add_argument("--lineage", default="Derived and validated using the repository processing pipeline.", help="Lineage statement")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="Metadata and publication date")
    parser.add_argument("--uuid", default=str(uuid.uuid4()), help="Metadata file identifier")
    parser.add_argument("--bbox", help="Bounding box xmin,ymin,xmax,ymax in EPSG:4326")
    parser.add_argument("--keywords", default="geospatial,big,palapa,geoportal", help="Comma-separated keyword list")
    parser.add_argument("--contact-name", default="Komunitas Pemerhati Data Spasial Publik", help="Point of contact name")
    parser.add_argument("--contact-email", default="geospatial@ahliweb.id", help="Contact email")
    parser.add_argument("--license-text", default="AW Non-Commercial License 1.0. Commercial use requires prior written permission.", help="Use limitation text")
    parser.add_argument("--license-contact", default="commercial@ahliweb.com", help="Commercial licensing contact")

    args = parser.parse_args()

    template_path = Path(args.template)
    output_path = Path(args.output)

    if not template_path.exists():
        print(f"Template not found: {template_path}")
        return 1

    tree = ET.parse(template_path)
    root = tree.getroot()

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]

    # Core metadata.
    set_text(root, ".//gmd:fileIdentifier/gco:CharacterString", args.uuid)
    set_text(root, ".//gmd:dateStamp/gco:Date", args.date)
    set_text(root, ".//gmd:metadataStandardName/gco:CharacterString", "SNI ISO 19115-3:2019")
    set_text(root, ".//gmd:metadataStandardVersion/gco:CharacterString", "SNI 8843-1:2019")
    set_text(root, ".//gmd:title/gco:CharacterString", args.title)
    set_text(root, ".//gmd:abstract/gco:CharacterString", args.abstract)
    set_text(root, ".//gmd:source/gco:CharacterString", args.source)
    set_text(root, ".//gmd:statement/gco:CharacterString", args.lineage)

    # Use limitation text.
    for use_limitation in all_nodes(root, ".//gmd:useLimitation/gco:CharacterString"):
        use_limitation.text = f"{args.license_text} Contact: {args.license_contact}."

    # Contact information.
    set_text(root, ".//gmd:individualName/gco:CharacterString", args.contact_name)
    set_text(root, ".//gmd:organisationName/gco:CharacterString", args.contact_name)
    set_text(root, ".//gmd:electronicMailAddress/gco:CharacterString", args.contact_email)

    # Keywords.
    update_keywords(root, keywords)

    # Extent.
    if args.bbox:
        update_extent(root, parse_bbox(args.bbox))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(pretty_xml(root), encoding="utf-8")
    print(f"✓ Metadata written: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
