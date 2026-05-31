# AWCMS-Micro Compatibility Guide

This repository stays geospatial-first. It does not replace protected AWCMS-Micro scripts.

## Compatibility Rules

- Treat `geo-first` as a job boundary and data workspace.
- Keep plugin-host logic thin in AWCMS-Micro.
- Do not copy or rewrite protected AWCMS-Micro internals into this repo.
- Use local path overrides and env-based configuration when the host provides them.
- Keep project outputs in `projects/<name>/output/` unless the host redirects them.

## Safe Extension Areas

- `shared/scripts/` for parameterized job runners
- `shared/config/` for host-facing environment examples and profiles
- `docs/` for compatibility notes and migration guidance
- `projects/<name>/` for project-specific data, metadata, QGIS, and exports

## Not Allowed Here

- Reimplementing AWCMS-Micro protected internals
- Embedding CMS auth, content, or plugin lifecycle logic into geospatial scripts
- Storing secrets in the repository

## Environment Strategy

If a root `.env` exists, prefer it for local overrides.
If not, use `shared/config/awcms-micro.env.example` as the reference template.

## Migration Goal

The eventual host integration should call the geospatial scripts as jobs, not vendor them as CMS internals.
