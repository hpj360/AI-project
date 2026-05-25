# -*- coding: utf-8 -*-
import argparse
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.parse
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from skills_upgrade import cmd_upgrade as run_skills_upgrade

from skillhub.config import (
    CLI_VERSION,
    CLI_VERSION_FILE_NAME,
    CLI_METADATA_FILE_NAME,
    CLI_SCRIPT_PATH,
    DEFAULT_CLI_HOME,
    CLI_CONFIG_NAME,
    DEFAULT_SELF_UPDATE_MANIFEST_URL,
    SELF_UPGRADE_CHECK_TIMEOUT_SECONDS,
    SKIP_SELF_UPGRADE_ENV,
    SKIP_WORKSPACE_SKILLS_ENV,
    DEFAULT_OPENCLAW_CONFIG_PATH,
    DEFAULT_OPENCLAW_WORKSPACE_PATH,
    DEFAULT_OPENCLAW_PLUGIN_DIR,
    POST_UPGRADE_SKILL_MIGRATION_MIN_VERSION,
    FIND_SKILLS_SLUG,
    SKILLHUB_PREFERENCE_SLUG,
    SKILL_CONFIG_NAME,
    SKILL_META_NAME,
    verbose_log,
    die,
    parse_path_like_uri,
)
from skillhub.version import normalize_version_text, version_is_newer, version_at_least, parse_bool_like
from skillhub.http import read_json_from_uri, download_file_or_raise
from skillhub.archive import safe_extract_zip, safe_extract_tar, sha256_file, install_zip_to_target
from skillhub.lockfile import load_lockfile, save_lockfile


def as_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def first_non_empty_string(obj: Dict[str, Any], keys: List[str]) -> str:
    for key in keys:
        value = obj.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def self_update_url_from_config(config: Dict[str, Any]) -> str:
    direct = first_non_empty_string(
        config,
        ["self_update_url", "selfUpdateUrl", "update_url", "updateUrl", "manifest_url", "manifestUrl"],
    )
    if direct:
        return direct

    for key in ("self_update", "selfUpdate", "update", "upgrade"):
        nested = as_dict(config.get(key))
        url_value = first_non_empty_string(nested, ["url", "uri", "manifest", "manifest_url", "manifestUrl"])
        if url_value:
            return url_value
    return ""


def self_update_enabled_from_config(config: Dict[str, Any]) -> Optional[bool]:
    for key in ("auto_self_upgrade", "autoSelfUpgrade", "self_update_auto", "selfUpdateAuto"):
        parsed = parse_bool_like(config.get(key))
        if parsed is not None:
            return parsed

    for key in ("self_update", "selfUpdate", "update", "upgrade"):
        nested = as_dict(config.get(key))
        for nested_key in ("auto", "enabled", "auto_upgrade", "autoUpgrade", "enabled_auto_upgrade"):
            parsed = parse_bool_like(nested.get(nested_key))
            if parsed is not None:
                return parsed
    return None


def resolve_uri_with_base(raw: str, base_dir: Path) -> str:
    value = raw.strip()
    if not value:
        return ""
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme in ("http", "https"):
        return value
    if parsed.scheme == "file":
        return parse_path_like_uri(value).as_uri()
    if parsed.scheme != "":
        die(f"Unsupported URI scheme: {value}")
    return (base_dir / value).resolve().as_uri()


def resolve_openclaw_config_path() -> Path:
    override = os.environ.get("OPENCLAW_CONFIG_PATH", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return Path(DEFAULT_OPENCLAW_CONFIG_PATH).expanduser().resolve()


def resolve_skillhub_config_path() -> Path:
    override = os.environ.get("SKILLHUB_CONFIG_PATH", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return Path(f"{DEFAULT_CLI_HOME}/{CLI_CONFIG_NAME}").expanduser().resolve()


def read_json_object(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(raw, dict):
        return {}
    return raw


def should_install_workspace_skills() -> bool:
    env_override = parse_bool_like(os.environ.get(SKIP_WORKSPACE_SKILLS_ENV, ""))
    if env_override is True:
        verbose_log(f"workspace skills install skipped by env {SKIP_WORKSPACE_SKILLS_ENV}=true")
        return False
    if env_override is False:
        return True

    config = read_json_object(resolve_skillhub_config_path())
    configured = parse_bool_like(config.get("install_workspace_skills"))
    if configured is not None:
        return configured
    return True


def openclaw_config_has_skillhub_entry(config: Dict[str, Any]) -> bool:
    plugins = as_dict(config.get("plugins"))
    entries = as_dict(plugins.get("entries"))
    return "skillhub" in entries


def skillhub_plugin_dir_present() -> bool:
    plugin_dir = Path(DEFAULT_OPENCLAW_PLUGIN_DIR).expanduser().resolve()
    if not plugin_dir.exists() or not plugin_dir.is_dir():
        return False
    try:
        next(plugin_dir.iterdir())
        return True
    except StopIteration:
        return False
    except Exception:
        return False


def detect_skillhub_plugin_behavior(config_path: Path) -> Tuple[bool, Dict[str, Any]]:
    config = read_json_object(config_path)
    config_has_entry = openclaw_config_has_skillhub_entry(config)
    plugin_dir_exists = skillhub_plugin_dir_present()
    return plugin_dir_exists or config_has_entry, config


def resolve_openclaw_bin() -> str:
    from_path = shutil.which("openclaw")
    if from_path:
        return from_path
    fallback = Path("~/.local/share/pnpm/openclaw").expanduser().resolve()
    if fallback.exists() and os.access(fallback, os.X_OK):
        return str(fallback)
    return ""


def disable_skillhub_plugin_via_openclaw(openclaw_bin: str) -> bool:
    if not openclaw_bin:
        return False
    try:
        result = subprocess.run(
            [openclaw_bin, "config", "unset", "plugins.entries.skillhub"],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception as exc:
        verbose_log(f"disable plugin by openclaw failed: {exc}")
        return False
    if result.returncode == 0:
        verbose_log("removed skillhub plugin config via openclaw config unset")
        return True
    err = (result.stderr or result.stdout or "").strip()
    if "config path not found" in err.lower():
        verbose_log("skillhub plugin config already absent")
        return True
    if err:
        verbose_log(f"openclaw config unset failed: {err}")
    return False


def resolve_openclaw_workspace_path(config: Dict[str, Any]) -> Path:
    env_workspace = os.environ.get("OPENCLAW_WORKSPACE", "").strip()
    if env_workspace:
        return Path(env_workspace).expanduser().resolve()

    for key in ("workspace", "workspace_dir", "workspaceDir", "workspace_path", "workspacePath"):
        value = config.get(key)
        if isinstance(value, str) and value.strip():
            return Path(value.strip()).expanduser().resolve()

    paths = as_dict(config.get("paths"))
    for key in ("workspace", "workspaceDir", "workspace_path", "workspacePath"):
        value = paths.get(key)
        if isinstance(value, str) and value.strip():
            return Path(value.strip()).expanduser().resolve()

    return Path(DEFAULT_OPENCLAW_WORKSPACE_PATH).expanduser().resolve()


def read_skill_template(template_path: Optional[Path]) -> str:
    if template_path and template_path.exists():
        try:
            content = template_path.read_text(encoding="utf-8").strip()
            if content:
                return content
        except Exception:
            pass
    return ""


def install_workspace_skill(workspace_path: Path, slug: str, content: str) -> Path:
    target = workspace_path / "skills" / slug / "SKILL.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = content if content.endswith("\n") else (content + "\n")
    target.write_text(payload, encoding="utf-8")
    return target


def find_cli_script_in_extracted(root: Path) -> Optional[Path]:
    direct = root / "skills_store_cli.py"
    if direct.exists():
        return direct
    nested = root / "cli" / "skills_store_cli.py"
    if nested.exists():
        return nested
    matches = list(root.rglob("skills_store_cli.py"))
    return matches[0] if matches else None


def find_peer_file_in_extracted(root: Path, filename: str) -> Optional[Path]:
    direct = root / filename
    if direct.exists():
        return direct
    nested = root / "cli" / filename
    if nested.exists():
        return nested
    matches = list(root.rglob(filename))
    return matches[0] if matches else None


def find_skill_file_in_extracted(root: Path, filename: str) -> Optional[Path]:
    direct = root / "skill" / filename
    if direct.exists():
        return direct
    nested = root / "cli" / "skill" / filename
    if nested.exists():
        return nested
    for match in root.rglob(filename):
        if match.parent.name == "skill":
            return match
    return None


def resolve_self_update_manifest_url(config_path: Path) -> str:
    if config_path.exists():
        verbose_log(f"reading config: {config_path}")
        try:
            raw = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            verbose_log("config JSON invalid; fallback to default manifest URL")
            raw = {}
        if isinstance(raw, dict):
            manifest_url_raw = self_update_url_from_config(raw)
            if manifest_url_raw:
                verbose_log(f"manifest URL from config: {manifest_url_raw}")
                return resolve_uri_with_base(manifest_url_raw, config_path.parent)
    else:
        verbose_log(f"config not found: {config_path}; use default manifest URL")
    verbose_log(f"using default manifest URL: {DEFAULT_SELF_UPDATE_MANIFEST_URL}")
    return DEFAULT_SELF_UPDATE_MANIFEST_URL


def should_run_startup_self_upgrade(config_path: Path) -> bool:
    env_override = parse_bool_like(os.environ.get(SKIP_SELF_UPGRADE_ENV, ""))
    if env_override is True:
        verbose_log(f"startup check skipped by env {SKIP_SELF_UPGRADE_ENV}=true")
        return False
    if not config_path.exists():
        return True
    try:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        verbose_log("startup check: config JSON invalid; keep default auto upgrade")
        return True
    if isinstance(raw, dict):
        enabled = self_update_enabled_from_config(raw)
        if enabled is False:
            verbose_log("startup check skipped by config auto_self_upgrade=false")
            return False
    return True


def extract_update_manifest_info(manifest: Dict[str, Any]) -> Tuple[str, str, str]:
    candidates = [manifest]
    for key in ("latest", "release", "data", "skill", "package"):
        nested = manifest.get(key)
        if isinstance(nested, dict):
            candidates.append(nested)

    latest_version = ""
    package_uri = ""
    sha256 = ""
    for item in candidates:
        if not latest_version:
            latest_version = first_non_empty_string(item, ["version", "latest_version", "latestVersion"])
        if not package_uri:
            package_uri = first_non_empty_string(
                item,
                ["zip_url", "zipUrl", "download_url", "downloadUrl", "package_url", "packageUrl", "url"],
            )
        if not sha256:
            sha256 = first_non_empty_string(item, ["sha256", "sha_256", "checksum"])
    return latest_version, package_uri, sha256.lower()


def run_post_upgrade_plugin_migration(
    latest_version: str,
    find_skill_template: Optional[Path],
    preference_skill_template: Optional[Path],
) -> None:
    if not version_at_least(latest_version, POST_UPGRADE_SKILL_MIGRATION_MIN_VERSION):
        verbose_log(f"post-upgrade migration skipped; version<{POST_UPGRADE_SKILL_MIGRATION_MIN_VERSION}")
        return

    config_path = resolve_openclaw_config_path()
    has_plugin_behavior, config = detect_skillhub_plugin_behavior(config_path)
    if not has_plugin_behavior:
        verbose_log("post-upgrade migration skipped; no skillhub plugin behavior detected")
        return

    verbose_log("skillhub plugin behavior detected; run migration to workspace skills")
    openclaw_bin = resolve_openclaw_bin()
    disabled = disable_skillhub_plugin_via_openclaw(openclaw_bin) if openclaw_bin else False

    if not disabled:
        verbose_log("skip plugin-disable fallback; openclaw command unavailable or failed")

    if not should_install_workspace_skills():
        verbose_log("workspace skills install disabled by config/env; skip install")
        return

    config_after = read_json_object(config_path)
    workspace_path = resolve_openclaw_workspace_path(config_after if config_after else config)
    find_skill_text = read_skill_template(find_skill_template)
    preference_skill_text = read_skill_template(preference_skill_template)

    if find_skill_text:
        find_target = install_workspace_skill(workspace_path, FIND_SKILLS_SLUG, find_skill_text)
        verbose_log(f"installed migrated skill: {find_target}")
    else:
        verbose_log("find-skills template missing in package; skip install")

    if preference_skill_text:
        preference_target = install_workspace_skill(
            workspace_path,
            SKILLHUB_PREFERENCE_SLUG,
            preference_skill_text,
        )
        verbose_log(f"installed migrated skill: {preference_target}")
    else:
        verbose_log("skillhub-preference template missing in package; skip install")


def cmd_upgrade(args: argparse.Namespace) -> None:
    code = run_skills_upgrade(
        args,
        {
            "load_lockfile": load_lockfile,
            "save_lockfile": save_lockfile,
            "read_json_from_uri": read_json_from_uri,
            "extract_update_manifest_info": extract_update_manifest_info,
            "resolve_uri_with_base": resolve_uri_with_base,
            "version_is_newer": version_is_newer,
            "install_zip_to_target": install_zip_to_target,
            "skill_config_name": SKILL_CONFIG_NAME,
            "skill_meta_name": SKILL_META_NAME,
        },
    )
    if code != 0:
        raise SystemExit(code)


def cmd_self_upgrade(args: argparse.Namespace) -> None:
    config_path = Path(args.config).expanduser().resolve()
    target_path = Path(args.target).expanduser().resolve() if args.target else CLI_SCRIPT_PATH
    try:
        upgraded, current_version, latest_version = run_self_upgrade_flow(
            config_path=config_path,
            target_path=target_path,
            current_version=args.current_version or CLI_VERSION,
            timeout=args.timeout,
            check_only=args.check_only,
            quiet=False,
        )
    except Exception as exc:
        die(str(exc))

    if not upgraded and not args.check_only:
        print(f"CLI is up-to-date: current={current_version} latest={latest_version}")


def run_self_upgrade_flow(
    config_path: Path,
    target_path: Path,
    current_version: str,
    timeout: int,
    check_only: bool,
    quiet: bool,
) -> Tuple[bool, str, str]:
    manifest_url = resolve_self_update_manifest_url(config_path)
    verbose_log(f"fetching manifest: {manifest_url} (timeout={timeout}s)")
    manifest = read_json_from_uri(manifest_url, timeout=timeout)
    latest_version, package_uri_raw, expected_sha = extract_update_manifest_info(manifest)
    if not latest_version:
        raise RuntimeError(f"Self-update manifest missing version: {manifest_url}")
    if not package_uri_raw:
        raise RuntimeError(f"Self-update manifest missing package URL: {manifest_url}")

    current = normalize_version_text(current_version or CLI_VERSION)
    latest = normalize_version_text(latest_version)
    verbose_log(f"version compare: current={current} latest={latest}")
    if not version_is_newer(latest, current):
        verbose_log("no upgrade needed")
        return False, current, latest

    package_uri = resolve_uri_with_base(package_uri_raw, config_path.parent)
    verbose_log(f"resolved package URI: {package_uri}")
    if not quiet:
        print(
            f"Self-upgrade available: current={current} latest={latest}\n"
            f"Manifest: {manifest_url}\n"
            f"Package:  {package_uri}\n"
            f"Target:   {target_path}"
        )
    if check_only:
        verbose_log("check-only mode; skip install")
        return False, current, latest

    with tempfile.TemporaryDirectory(prefix="skillhub-self-upgrade-") as tmp:
        package_path = Path(tmp) / "package.bin"
        verbose_log(f"downloading package to temp: {package_path}")
        download_file_or_raise(package_uri, package_path)

        if expected_sha:
            verbose_log("sha256 present; verifying package checksum")
            actual_sha = sha256_file(package_path).lower()
            if actual_sha != expected_sha:
                raise RuntimeError(f"Self-upgrade SHA256 mismatch: expected {expected_sha}, got {actual_sha}")
        else:
            verbose_log("sha256 empty/missing; skip checksum verification")

        source_script: Path
        source_upgrade_module = None
        source_version_file = None
        source_metadata_file = None
        source_find_skill_template = None
        source_preference_skill_template = None
        if zipfile.is_zipfile(package_path):
            extract_dir = Path(tmp) / "extract"
            extract_dir.mkdir(parents=True, exist_ok=True)
            safe_extract_zip(package_path, extract_dir)
            found = find_cli_script_in_extracted(extract_dir)
            if not found:
                raise RuntimeError("Self-upgrade zip does not contain skills_store_cli.py")
            source_script = found
            source_upgrade_module = find_peer_file_in_extracted(extract_dir, "skills_upgrade.py")
            source_version_file = find_peer_file_in_extracted(extract_dir, CLI_VERSION_FILE_NAME)
            source_metadata_file = find_peer_file_in_extracted(extract_dir, CLI_METADATA_FILE_NAME)
            source_find_skill_template = find_skill_file_in_extracted(extract_dir, "SKILL.md")
            source_preference_skill_template = find_skill_file_in_extracted(
                extract_dir,
                "SKILL.skillhub-preference.md",
            )
        elif tarfile.is_tarfile(package_path):
            extract_dir = Path(tmp) / "extract"
            extract_dir.mkdir(parents=True, exist_ok=True)
            safe_extract_tar(package_path, extract_dir)
            found = find_cli_script_in_extracted(extract_dir)
            if not found:
                raise RuntimeError("Self-upgrade tar package does not contain skills_store_cli.py")
            source_script = found
            source_upgrade_module = find_peer_file_in_extracted(extract_dir, "skills_upgrade.py")
            source_version_file = find_peer_file_in_extracted(extract_dir, CLI_VERSION_FILE_NAME)
            source_metadata_file = find_peer_file_in_extracted(extract_dir, CLI_METADATA_FILE_NAME)
            source_find_skill_template = find_skill_file_in_extracted(extract_dir, "SKILL.md")
            source_preference_skill_template = find_skill_file_in_extracted(
                extract_dir,
                "SKILL.skillhub-preference.md",
            )
        else:
            source_script = package_path

        try:
            raw = source_script.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise RuntimeError(f"Self-upgrade package is not a text python script: {exc}") from exc
        if "def main()" not in raw:
            raise RuntimeError("Self-upgrade package content check failed (missing def main())")

        backup_path = target_path.with_suffix(target_path.suffix + ".bak")
        if target_path.exists():
            verbose_log(f"writing backup: {backup_path}")
            shutil.copyfile(target_path, backup_path)
        verbose_log(f"replacing target script: {target_path}")
        shutil.copyfile(source_script, target_path)
        target_path.chmod(0o755)

        target_upgrade_module = target_path.parent / "skills_upgrade.py"
        if source_upgrade_module and source_upgrade_module.exists():
            verbose_log(f"updating companion module: {target_upgrade_module}")
            shutil.copyfile(source_upgrade_module, target_upgrade_module)

        target_metadata_file = target_path.parent / CLI_METADATA_FILE_NAME
        if source_metadata_file and source_metadata_file.exists():
            verbose_log(f"updating metadata file from package: {target_metadata_file}")
            shutil.copyfile(source_metadata_file, target_metadata_file)

        version_file_path = target_path.parent / CLI_VERSION_FILE_NAME
        if source_version_file and source_version_file.exists():
            verbose_log(f"updating version file from package: {version_file_path}")
            shutil.copyfile(source_version_file, version_file_path)
        else:
            verbose_log(f"updating version file: {version_file_path} -> {latest}")
            version_file_path.write_text(
                json.dumps({"version": latest}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        try:
            run_post_upgrade_plugin_migration(
                latest_version=latest,
                find_skill_template=source_find_skill_template,
                preference_skill_template=source_preference_skill_template,
            )
        except Exception as exc:
            verbose_log(f"post-upgrade migration failed; continue: {exc}")
        if not quiet:
            print(f"Self-upgrade complete: {target_path} -> version {latest}")
            print(f"Backup saved at: {backup_path}")
    return True, current, latest


def startup_self_upgrade_check(config_path: Optional[Path] = None) -> bool:
    if config_path is None:
        config_path = Path(f"{DEFAULT_CLI_HOME}/{CLI_CONFIG_NAME}").expanduser().resolve()
    if not config_path.exists():
        verbose_log(f"startup check: config not found at {config_path}; will use default manifest")
    try:
        upgraded, _, _ = run_self_upgrade_flow(
            config_path=config_path,
            target_path=CLI_SCRIPT_PATH,
            current_version=CLI_VERSION,
            timeout=SELF_UPGRADE_CHECK_TIMEOUT_SECONDS,
            check_only=False,
            quiet=True,
        )
        verbose_log(f"startup check result: upgraded={upgraded}")
        return upgraded
    except BaseException:
        verbose_log("startup check failed; continue without upgrade")
        return False
