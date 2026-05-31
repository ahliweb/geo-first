#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
ENV_FILE="$REPO_ROOT/.env"
ENV_TEMPLATE="$REPO_ROOT/shared/config/awcms-geospatial.env.example"

if [[ ! -f "$ENV_TEMPLATE" ]]; then
  printf 'Missing env template: %s\n' "$ENV_TEMPLATE"
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  cp "$ENV_TEMPLATE" "$ENV_FILE"
  printf 'Created %s from %s\n' "$ENV_FILE" "$ENV_TEMPLATE"
else
  printf 'Using existing %s\n' "$ENV_FILE"
fi

mkdir -p \
  "$REPO_ROOT/projects/faskes-kobar/output" \
  "$REPO_ROOT/projects/faskes-kobar/metadata" \
  "$REPO_ROOT/projects/faskes-kobar/qgis"

printf 'Setup complete.\n'
printf 'Next: python3 shared/scripts/generate_professional_map.py\n'
