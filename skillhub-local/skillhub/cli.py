# -*- coding: utf-8 -*-
import argparse
import os
import sys
from pathlib import Path

from skillhub.config import (
    CLI_VERSION,
    DEFAULT_INDEX_URI,
    DEFAULT_INSTALL_ROOT,
    DEFAULT_CLI_HOME,
    CLI_CONFIG_NAME,
    DEFAULT_SEARCH_URL,
    DEFAULT_SKILLS_DOWNLOAD_URL_TEMPLATE,
    DEFAULT_PRIMARY_DOWNLOAD_URL_TEMPLATE,
    SELF_UPGRADE_REEXEC_ENV,
)
from skillhub.lockfile import load_lockfile
from skillhub.search import cmd_search
from skillhub.install import cmd_install
from skillhub.upgrade import cmd_upgrade, cmd_self_upgrade, should_run_startup_self_upgrade, startup_self_upgrade_check


def cmd_list(args: argparse.Namespace) -> None:
    install_root = Path(args.dir).expanduser().resolve()
    lock = load_lockfile(install_root)
    skills = lock.get("skills", {})
    if not skills:
        print("No installed skills.")
        return
    for slug, meta in sorted(skills.items()):
        if isinstance(meta, dict):
            version = str(meta.get("version", "")).strip()
            print(f"{slug}  {version}")
        else:
            print(f"{slug}  ")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Minimal local skills store CLI")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"skillhub {CLI_VERSION}",
        help="Show skillhub CLI version and exit",
    )
    parser.add_argument(
        "--index",
        default=DEFAULT_INDEX_URI,
        help=(
            "Skills index JSON path/URI. Supports http://, https://, file://, or local paths "
            '(default from metadata.json, e.g. "https://.../skills.json").'
        ),
    )
    parser.add_argument(
        "--dir",
        default=DEFAULT_INSTALL_ROOT,
        help='Install root directory (default: "./skills")',
    )
    parser.add_argument(
        "--skip-self-upgrade",
        action="store_true",
        help="Skip startup self-upgrade check for this run",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Search skills")
    search.add_argument("query", nargs="*", help="Search query words")
    search.add_argument(
        "--search-url",
        default=DEFAULT_SEARCH_URL,
        help=(
            "Remote search API URL (default from SKILLHUB_SEARCH_URL / metadata / built-in). "
            'Example: "http://.../api/v1/search".'
        ),
    )
    search.add_argument(
        "--search-limit",
        type=int,
        default=20,
        help="Remote search limit (default: 20)",
    )
    search.add_argument(
        "--search-timeout",
        type=int,
        default=6,
        help="Remote search timeout seconds (default: 6)",
    )
    search.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        help="Print search results as JSON",
    )
    search.set_defaults(func=cmd_search)

    install = subparsers.add_parser("install", help="Install a skill by slug")
    install.add_argument("slug", help="Skill slug")
    install.add_argument(
        "--files-base-uri",
        default="",
        help=(
            "Base URI/path for local archives. Supports file://, local paths, or "
            "URL template with {slug} (examples: file://./cli/files, ./cli/files, "
            "https://example.com/files/{slug}.zip)."
        ),
    )
    install.add_argument(
        "--download-url-template",
        default=DEFAULT_SKILLS_DOWNLOAD_URL_TEMPLATE,
        help=(
            "Fallback download URL template when zip_url/local file is missing "
            '(default from metadata.json, e.g. "https://.../skills/{slug}.zip").'
        ),
    )
    install.add_argument(
        "--primary-download-url-template",
        default=DEFAULT_PRIMARY_DOWNLOAD_URL_TEMPLATE,
        help=(
            "Primary download URL template for install (supports {slug}). "
            "This is the only remote source used by install."
        ),
    )
    install.add_argument(
        "--search-url",
        default=DEFAULT_SEARCH_URL,
        help="Remote search API URL used when slug is not found in index.",
    )
    install.add_argument(
        "--search-limit",
        type=int,
        default=20,
        help="Remote search limit for install fallback (default: 20)",
    )
    install.add_argument(
        "--search-timeout",
        type=int,
        default=6,
        help="Remote search timeout for install fallback in seconds (default: 6)",
    )
    install.add_argument("--force", action="store_true", help="Overwrite existing target directory")
    install.set_defaults(func=cmd_install)

    upgrade = subparsers.add_parser(
        "upgrade",
        help="Upgrade installed skills based on each skill's config.json update URL",
    )
    upgrade.add_argument(
        "slug",
        nargs="?",
        default="",
        help="Optional skill slug. If omitted, upgrade all skills in lockfile.",
    )
    upgrade.add_argument(
        "--check-only",
        action="store_true",
        help="Only check and print available upgrades without installing",
    )
    upgrade.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="Timeout in seconds for manifest fetch (default: 20)",
    )
    upgrade.set_defaults(func=cmd_upgrade)

    list_cmd = subparsers.add_parser("list", help="List locally installed skills")
    list_cmd.set_defaults(func=cmd_list)

    self_upgrade = subparsers.add_parser(
        "self-upgrade",
        help="Self-upgrade this CLI from update manifest URL in config.json",
    )
    self_upgrade.add_argument(
        "--config",
        default=f"{DEFAULT_CLI_HOME}/config.json",
        help=(
            'Self-upgrade config path (default: "~/.skillhub/config.json"). '
            "If missing or no URL configured, falls back to the built-in manifest URL."
        ),
    )
    self_upgrade.add_argument(
        "--target",
        default="",
        help="CLI script target path to replace (default: current running script path)",
    )
    self_upgrade.add_argument(
        "--current-version",
        default=CLI_VERSION,
        help=f'Current CLI version for comparison (default: "{CLI_VERSION}")',
    )
    self_upgrade.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="Timeout in seconds for manifest fetch/download requests (default: 20)",
    )
    self_upgrade.add_argument(
        "--check-only",
        action="store_true",
        help="Only check and print available CLI upgrade without replacing files",
    )
    self_upgrade.set_defaults(func=cmd_self_upgrade)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    config_path = Path(f"{DEFAULT_CLI_HOME}/{CLI_CONFIG_NAME}").expanduser().resolve()
    command = str(getattr(args, "command", "")).strip()
    should_check_startup_upgrade = (
        command != "self-upgrade"
        and os.environ.get(SELF_UPGRADE_REEXEC_ENV, "") != "1"
        and not bool(getattr(args, "skip_self_upgrade", False))
        and should_run_startup_self_upgrade(config_path)
    )
    if should_check_startup_upgrade:
        upgraded = startup_self_upgrade_check(config_path=config_path)
        if upgraded:
            env = os.environ.copy()
            env[SELF_UPGRADE_REEXEC_ENV] = "1"
            os.execve(sys.executable, [sys.executable, *sys.argv], env)
    args.func(args)
