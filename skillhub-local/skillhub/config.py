# -*- coding: utf-8 -*-
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_INSTALL_ROOT = "./skills"
LOCKFILE_NAME = ".skills_store_lock.json"
SKILL_CONFIG_NAME = "config.json"
SKILL_META_NAME = "_meta.json"
CLI_CONFIG_NAME = "config.json"
CLI_VERSION_FILE_NAME = "version.json"
CLI_METADATA_FILE_NAME = "metadata.json"
CLI_VERSION_FALLBACK = "2026.3.3"
DEFAULT_INDEX_URI_FALLBACK = "https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/skills.json"
DEFAULT_SEARCH_URL_FALLBACK = "https://lightmake.site/api/v1/search"
SELF_UPGRADE_CHECK_TIMEOUT_SECONDS = 2
DEFAULT_CLI_HOME = "~/.skillhub"
SELF_UPGRADE_REEXEC_ENV = "SKILLHUB_SELF_UPGRADE_REEXEC"
SKIP_SELF_UPGRADE_ENV = "SKILLHUB_SKIP_SELF_UPGRADE"
SKIP_WORKSPACE_SKILLS_ENV = "SKILLHUB_SKIP_WORKSPACE_SKILLS"
DEFAULT_SELF_UPDATE_MANIFEST_URL_FALLBACK = "https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/version.json"
DEFAULT_SKILLS_DOWNLOAD_URL_TEMPLATE_FALLBACK = (
    "https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/skills/{slug}.zip"
)
DEFAULT_PRIMARY_DOWNLOAD_URL_TEMPLATE_FALLBACK = (
    "https://lightmake.site/api/v1/download?slug={slug}"
)
DEFAULT_OPENCLAW_CONFIG_PATH = "~/.openclaw/openclaw.json"
DEFAULT_OPENCLAW_WORKSPACE_PATH = "~/.openclaw/workspace"
DEFAULT_OPENCLAW_PLUGIN_DIR = "~/.openclaw/extensions/skillhub"
POST_UPGRADE_SKILL_MIGRATION_MIN_VERSION = (3, 13)
FIND_SKILLS_SLUG = "find-skills"
SKILLHUB_PREFERENCE_SLUG = "skillhub-preference"


def load_cli_version(base_dir: Path) -> str:
    version_path = base_dir / CLI_VERSION_FILE_NAME
    if not version_path.exists():
        return CLI_VERSION_FALLBACK
    try:
        raw = json.loads(version_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return CLI_VERSION_FALLBACK
    if not isinstance(raw, dict):
        return CLI_VERSION_FALLBACK
    value = raw.get("version")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return CLI_VERSION_FALLBACK


def load_cli_metadata(base_dir: Path) -> Dict[str, str]:
    metadata_path = base_dir / CLI_METADATA_FILE_NAME
    if not metadata_path.exists():
        return {}
    try:
        raw = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if not isinstance(raw, dict):
        return {}
    out: Dict[str, str] = {}
    for key in (
        "skills_index_url",
        "skills_download_url_template",
        "self_update_manifest_url",
        "skills_search_url",
        "skills_primary_download_url_template",
    ):
        value = raw.get(key)
        if isinstance(value, str) and value.strip():
            out[key] = value.strip()
    return out


_CLI_BASE_DIR = Path(__file__).resolve().parent.parent
CLI_VERSION = load_cli_version(_CLI_BASE_DIR)
CLI_METADATA = load_cli_metadata(_CLI_BASE_DIR)
DEFAULT_INDEX_URI = CLI_METADATA.get("skills_index_url", DEFAULT_INDEX_URI_FALLBACK)
DEFAULT_SELF_UPDATE_MANIFEST_URL = CLI_METADATA.get(
    "self_update_manifest_url",
    DEFAULT_SELF_UPDATE_MANIFEST_URL_FALLBACK,
)
DEFAULT_SKILLS_DOWNLOAD_URL_TEMPLATE = CLI_METADATA.get(
    "skills_download_url_template",
    DEFAULT_SKILLS_DOWNLOAD_URL_TEMPLATE_FALLBACK,
)
DEFAULT_SEARCH_URL = os.environ.get("SKILLHUB_SEARCH_URL", "").strip() or CLI_METADATA.get(
    "skills_search_url",
    DEFAULT_SEARCH_URL_FALLBACK,
)
DEFAULT_PRIMARY_DOWNLOAD_URL_TEMPLATE = (
    os.environ.get("SKILLHUB_PRIMARY_DOWNLOAD_URL_TEMPLATE", "").strip()
    or CLI_METADATA.get(
        "skills_primary_download_url_template",
        DEFAULT_PRIMARY_DOWNLOAD_URL_TEMPLATE_FALLBACK,
    )
)
CLI_USER_AGENT = f"skills-store-cli/{CLI_VERSION}"
MAX_HTTP_REDIRECTS = 5
CLI_SCRIPT_PATH = _CLI_BASE_DIR / "skills_store_cli.py"


def verbose_enabled() -> bool:
    return os.environ.get("LOG", "") == "VERBOSE"


def verbose_log(message: str) -> None:
    if verbose_enabled():
        print(f"[self-upgrade][verbose] {message}")


def die(message: str, code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def normalize_file_uri(uri_or_path: str) -> Path:
    parsed = urllib.parse.urlparse(uri_or_path)
    if parsed.scheme == "file":
        if parsed.netloc in ("", "localhost"):
            combined = parsed.path
        else:
            combined = f"{parsed.netloc}{parsed.path}"

        raw_path = urllib.request.url2pathname(combined)
        if not raw_path.strip():
            die(f"Invalid file URI: {uri_or_path}")
        candidate = Path(raw_path).expanduser()
        if not candidate.is_absolute():
            candidate = Path.cwd() / candidate
        return candidate.resolve()
    if parsed.scheme:
        die(f"Only file:// is supported for --index. Got: {uri_or_path}")
    return Path(uri_or_path).expanduser().resolve()


def parse_path_like_uri(uri_or_path: str) -> Path:
    parsed = urllib.parse.urlparse(uri_or_path)
    if parsed.scheme == "file":
        return normalize_file_uri(uri_or_path)
    if parsed.scheme:
        die(f"Only file:// or local paths are supported here. Got: {uri_or_path}")
    return Path(uri_or_path).expanduser().resolve()


def append_slug_zip(base_uri_or_path: str, slug: str) -> str:
    base = base_uri_or_path.strip()
    if not base:
        return ""
    if "{slug}" in base:
        return base.replace("{slug}", urllib.parse.quote(slug))
    parsed = urllib.parse.urlparse(base)
    suffix = f"{urllib.parse.quote(slug)}.zip"
    if parsed.scheme in ("http", "https"):
        return urllib.parse.urljoin(base.rstrip("/") + "/", suffix)
    base_path = parse_path_like_uri(base)
    return (base_path / f"{slug}.zip").resolve().as_uri()


def fill_slug_template(url_template: str, slug: str) -> str:
    raw = str(url_template or "").strip()
    if not raw:
        return ""
    if "{slug}" not in raw:
        return raw
    return raw.replace("{slug}", urllib.parse.quote(slug))
