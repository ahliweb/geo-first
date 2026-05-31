# AWCMS Geospatial Plugin Guide

This repository is the independent geospatial workspace for the `awcms-geospatial` plugin and the `awcms-geospatialTemplate` template.

## Canonical Identity

- Plugin: `awcms-geospatial`
- Template: `awcms-geospatialTemplate`
- Primary geospatial domain: Kotawaringin Barat Regency, Central Kalimantan

## Compatibility Boundary

- Use AWCMS-Micro and EmDash as external references only.
- Keep protected host scripts untouched.
- Treat this repo as the geospatial execution layer and template source.

## Safe Areas for Change

- `shared/scripts/` for job runners and exporters
- `shared/config/` for manifests, env examples, and sector profiles
- `projects/_template/` for reusable project scaffolding
- `docs/` for compatibility and update notes

## Naming Rules

- Environment variables use the `AWCMS_GEOSPATIAL_*` prefix first.
- Legacy `GEOFIRST_*` variables remain accepted as fallback only.
- Canonical config files use the plugin/template names.
- Output paths stay project-scoped unless the host explicitly overrides them.

## Update Strategy

1. Add new plugin/template config alongside existing legacy support.
2. Keep scripts backward compatible.
3. Prefer declarative config over hard-coded paths.
4. Avoid copying protected AWCMS-Micro internals into this repo.

## Local Setup 

- Run `bash scripts/setup-awcms-geospatial.sh` after clone to create `.env` when it does not exist.
- The Python automation scripts auto-load `.env` from the repository root.
- Default map generation targets `projects/faskes-kobar/` with the `health` sector and `faskes` layer unless overridden.
- Plugin and template manifests are marked enabled by default in repo metadata so the workspace is ready for the host-side adapter work.

## License

This repository is licensed under the AW Non-Commercial License 1.0.
