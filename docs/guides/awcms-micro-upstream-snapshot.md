# AWCMS-Micro Upstream Snapshot

This repository vendors a read-only upstream snapshot at `upstream/awcms-micro/`.

## Purpose

- Keep a local copy of the current `awcms-micro` state for reference.
- Make future upstream comparisons and sync work easier.
- Keep this geospatial repository independent from the upstream workspace layout.

## Rules

- Do not edit files under `upstream/awcms-micro/` directly unless you are refreshing the snapshot.
- Treat the snapshot as reference material only.
- Keep all geospatial product work in the active `awcms-geospatial` areas.
- Do not move protected AWCMS-Micro internals from the snapshot into active geospatial scripts.

## Sync Marker

- Upstream commit: `b703362759c17da2a889d9a44b3904670cc848f6`

## Update Path

Use `scripts/sync-awcms-micro-upstream.sh` to refresh the snapshot from GitHub.

## License

The upstream snapshot inherits the licensing of `ahliweb/awcms-micro`.
