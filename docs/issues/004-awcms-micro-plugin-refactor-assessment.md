# Issue 004: AWCMS-Micro plugin refactor assessment

## Goal
Assess whether `geo-first` can be refactored into an `awcms-micro` plugin, and define the smallest safe path toward a plugin-compatible architecture.

## Assessment
- This repository is currently a geospatial project workspace, not a CMS extension package.
- Core value here lives in QGIS/PyQGIS/GDAL scripts, project data, shared styles, metadata templates, and exported deliverables.
- The current scripts are tightly coupled to local repo paths and Kotawaringin Barat project assumptions.
- A direct in-place conversion into a CMS plugin is not realistic without a host-side plugin contract, lifecycle hooks, and storage model.

## Constraints
- Public docs for `ahliweb/awcms-micro` were not discoverable during analysis.
- Public EmDash plugin documentation is the closest architectural reference available, but it is not a drop-in match for this repository.
- Large geospatial assets should not be bundled inside a CMS plugin artifact.

## Recommended Target State
- Keep `geo-first` as the geospatial source/workflow repo.
- Extract a thin, reusable geospatial core interface.
- Let `awcms-micro` own UX, auth, job orchestration, and content publishing.
- Treat map generation as a callable job/service, not as CMS-internal business logic.

## Atomic Phases
1. Parameterize hard-coded paths and project names in shared scripts.
2. Define a stable input/output contract for map jobs.
3. Move reusable generation logic into a small library or CLI boundary.
4. Add a host-side adapter/plugin in `awcms-micro` that calls the boundary.
5. Move large datasets and exports to external storage or mounted volumes.

## Acceptance Criteria
- The geospatial pipeline can be triggered without editing script constants.
- Map generation accepts project path, sector, layer list, and output format as inputs.
- The CMS plugin layer remains thin and does not embed data processing logic.
- Existing `geo-first` workflows keep working during the transition.

## Notes
- This work remains under the AW Non-Commercial License 1.0.
- Commercial use still requires written permission.
