# -*- coding: utf-8 -*-
import json
import os
import time
from pathlib import Path
from typing import Any, Dict

from skillhub.config import LOCKFILE_NAME, verbose_log


def load_lockfile(install_root: Path) -> Dict[str, Any]:
    lock_path = install_root / LOCKFILE_NAME
    if not lock_path.exists():
        return {"version": 1, "skills": {}}
    try:
        raw = json.loads(lock_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"version": 1, "skills": {}}
    if not isinstance(raw, dict):
        return {"version": 1, "skills": {}}
    if not isinstance(raw.get("skills"), dict):
        raw["skills"] = {}
    return raw


def save_lockfile(install_root: Path, lock: Dict[str, Any]) -> None:
    install_root.mkdir(parents=True, exist_ok=True)
    lock_path = install_root / LOCKFILE_NAME
    lock_path.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve_clawhub_lock_path() -> Path:
    override = os.environ.get("SKILLHUB_CLAWHUB_LOCK_PATH", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return Path("~/.openclaw/workspace/.clawhub/lock.json").expanduser().resolve()


def update_clawhub_lock_v1(slug: str, version: str) -> None:
    lock_path = resolve_clawhub_lock_path()
    if not lock_path.exists():
        verbose_log(f"clawhub lock not found, skip sync: {lock_path}")
        return
    try:
        raw = json.loads(lock_path.read_text(encoding="utf-8"))
    except Exception:
        verbose_log(f"clawhub lock invalid JSON, skip sync: {lock_path}")
        return
    if not isinstance(raw, dict) or raw.get("version") != 1:
        verbose_log(f"clawhub lock version is not 1, skip sync: {lock_path}")
        return
    skills = raw.get("skills")
    if not isinstance(skills, dict):
        skills = {}
        raw["skills"] = skills
    skills[slug] = {
        "version": version,
        "installedAt": int(time.time() * 1000),
    }
    try:
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path.write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        verbose_log(f"synced clawhub lock entry: {slug} -> {lock_path}")
    except Exception:
        verbose_log(f"failed to write clawhub lock, skip: {lock_path}")
