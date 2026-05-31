#!/usr/bin/env python3
"""Minimal .env loader for repo-local automation."""

from __future__ import annotations

from pathlib import Path
import os


REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = REPO_ROOT / '.env'


def _parse_env_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith('#'):
        return None
    if stripped.startswith('export '):
        stripped = stripped[len('export '):].lstrip()
    if '=' not in stripped:
        return None
    key, value = stripped.split('=', 1)
    key = key.strip()
    value = value.strip()
    if not key:
        return None
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    return key, value


def load_repo_env(path: Path = ENV_PATH) -> None:
    """Load repo-local environment variables without overriding shell values."""
    if not path.exists():
        return

    for raw_line in path.read_text(encoding='utf-8').splitlines():
        parsed = _parse_env_line(raw_line)
        if not parsed:
            continue
        key, value = parsed
        os.environ.setdefault(key, value)
