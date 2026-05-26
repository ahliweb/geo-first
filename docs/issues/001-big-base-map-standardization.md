# Issue 001: BIG-compliant base map standardization

## Goal
Standardize all map generation on the village/sub-district administrative base map so every export follows BIG/PALAPA expectations and remains reusable across sectors.

## Scope
- Make `kabupaten`, `kecamatan`, and `desa` the canonical base layers.
- Use `desa` and `kecamatan` as the default visual reference for all outputs.
- Keep thematic layers secondary and clearly separated from the base map.
- Preserve relative paths and headless export support.

## Acceptance Criteria
- Every professional map export loads the admin boundary base map first.
- The base map is visually clear at print scale.
- Outputs remain exportable as PNG, PDF, and SVG.
- Existing projects keep working without manual file path edits.

## Notes
- This work stays within the AW Non-Commercial License 1.0.
- Commercial use requires separate written permission.
- Follow `docs/guides/manual-automatic-map-production.md` as the implementation reference.
