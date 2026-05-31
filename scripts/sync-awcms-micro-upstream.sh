#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
TARGET_DIR="$REPO_ROOT/upstream/awcms-micro"
TMP_ROOT="${TMPDIR:-/tmp}"
UPSTREAM_URL="https://github.com/ahliweb/awcms-micro.git"

TMP_CLONE="$(mktemp -d "$TMP_ROOT/awcms-micro-upstream-clone.XXXXXX")"
TMP_TARGET="$(mktemp -d "$TMP_ROOT/awcms-micro-upstream-target.XXXXXX")"

cleanup() {
  rm -rf "$TMP_CLONE" "$TMP_TARGET"
}
trap cleanup EXIT

git clone --depth 1 "$UPSTREAM_URL" "$TMP_CLONE"
git -C "$TMP_CLONE" archive --format=tar HEAD | tar -x -C "$TMP_TARGET"
git -C "$TMP_CLONE" rev-parse HEAD > "$TMP_TARGET/.upstream-commit"

mkdir -p "$(dirname "$TARGET_DIR")"
rm -rf "$TARGET_DIR"
mv "$TMP_TARGET" "$TARGET_DIR"

printf 'Refreshed %s from %s\n' "$TARGET_DIR" "$UPSTREAM_URL"
