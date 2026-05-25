# -*- coding: utf-8 -*-
import argparse
import sys
from pathlib import Path
from typing import Any, Dict

from skillhub.config import die, fill_slug_template
from skillhub.http import fetch_remote_search_results
from skillhub.archive import install_zip_to_target_with_fallback
from skillhub.lockfile import load_lockfile, save_lockfile, update_clawhub_lock_v1
from skillhub.search import load_index, find_skill, normalize_source_label


def cmd_install(args: argparse.Namespace) -> None:
    data: Dict[str, Any] = {"skills": []}
    try:
        data = load_index(args.index)
    except SystemExit:
        print(f"warn: failed to load index ({args.index}), continue with remote/direct install", file=sys.stderr)
    skill = find_skill(data, args.slug)
    if not skill:
        remote = fetch_remote_search_results(
            search_url=args.search_url,
            query=args.slug,
            limit=args.search_limit,
            timeout=args.search_timeout,
        )
        if remote:
            exact = next((x for x in remote if str(x.get("slug", "")).strip() == args.slug), None)
            if exact:
                skill = exact
                print(f'info: "{args.slug}" not in index, using remote registry exact match', file=sys.stderr)
            else:
                print(
                    f'info: "{args.slug}" not in index, and remote search has no exact slug match; '
                    "try direct download by slug",
                    file=sys.stderr,
                )

    if not skill:
        skill = {"slug": args.slug, "name": args.slug, "version": "", "source": "skillhub"}
        print(f'info: "{args.slug}" not in index/remote search, try direct download by slug', file=sys.stderr)

    primary_zip_url = fill_slug_template(args.primary_download_url_template, args.slug)
    if not primary_zip_url:
        die("Primary download URL template resolved empty URL")

    install_root = Path(args.dir).expanduser().resolve()
    target_dir = install_root / args.slug
    expected_sha256 = str(skill.get("sha256", "")).strip().lower()
    install_zip_to_target_with_fallback(
        slug=args.slug,
        zip_uris=[primary_zip_url],
        target_dir=target_dir,
        force=args.force,
        expected_sha256=expected_sha256,
    )

    lock = load_lockfile(install_root)
    skills_lock = lock.setdefault("skills", {})
    skills_lock[args.slug] = {
        "name": skill.get("name", args.slug),
        "zip_url": primary_zip_url,
        "source": normalize_source_label(skill.get("source")),
        "version": str(skill.get("version", "")).strip(),
    }
    save_lockfile(install_root, lock)
    update_clawhub_lock_v1(args.slug, str(skill.get("version", "")).strip())
    print(f"Installed: {args.slug} -> {target_dir}")
