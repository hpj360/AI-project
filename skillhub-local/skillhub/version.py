# -*- coding: utf-8 -*-
from typing import Any, List, Optional, Tuple


def normalize_version_text(v: str) -> str:
    return v.strip()


def parse_version_key(version: str) -> Optional[Tuple[int, ...]]:
    raw = version.strip().lower()
    if raw.startswith("v"):
        raw = raw[1:]
    if not raw:
        return None
    core = raw.split("-", 1)[0].split("+", 1)[0]
    parts = core.split(".")
    out: List[int] = []
    for part in parts:
        if not part.isdigit():
            return None
        out.append(int(part))
    return tuple(out) if out else None


def version_is_newer(candidate: str, current: str) -> bool:
    candidate = candidate.strip()
    current = current.strip()
    if not candidate:
        return False
    if not current:
        return True
    a = parse_version_key(candidate)
    b = parse_version_key(current)
    if a is not None and b is not None:
        return a > b
    return candidate != current


def version_at_least(version: str, minimum: Tuple[int, ...]) -> bool:
    parsed = parse_version_key(version)
    if parsed is None:
        return False
    return parsed >= minimum


def parse_bool_like(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("1", "true", "yes", "on"):
            return True
        if normalized in ("0", "false", "no", "off"):
            return False
    return None
