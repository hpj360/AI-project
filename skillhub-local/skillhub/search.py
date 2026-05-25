# -*- coding: utf-8 -*-
import argparse
import json
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from skillhub.config import die, parse_path_like_uri, append_slug_zip
from skillhub.http import read_json_from_uri, fetch_remote_search_results


def skill_text(skill: Dict[str, Any]) -> str:
    tags = skill.get("tags") or []
    if not isinstance(tags, list):
        tags = []
    categories = skill.get("categories") or []
    if not isinstance(categories, list):
        categories = []
    text = " ".join(
        [
            str(skill.get("slug", "")),
            str(skill.get("name", "")),
            str(skill.get("description", "")),
            str(skill.get("summary", "")),
            str(skill.get("version", "")),
            " ".join(str(tag) for tag in tags),
            " ".join(str(category) for category in categories),
        ]
    )
    return text.lower()


def normalize_source_label(value: Any) -> str:
    source = str(value or "").strip()
    if not source or source.lower() == "unknown":
        return "skillhub"
    return source


def is_clawhub_url(value: str) -> bool:
    try:
        host = urllib.parse.urlparse(value).netloc.lower()
    except Exception:
        return False
    return host == "clawhub.ai" or host.endswith(".clawhub.ai")


def normalize_skills_payload(data: Any) -> Dict[str, Any]:
    if isinstance(data, dict):
        skills = data.get("skills")
        if isinstance(skills, list):
            return data
        die('Index JSON must include a "skills" array.')
    if isinstance(data, list):
        return {"skills": data}
    die("Index JSON must be an object or array.")
    return {"skills": []}


def load_index(index_uri: str) -> Dict[str, Any]:
    try:
        data = read_json_from_uri(index_uri, timeout=20)
    except Exception as exc:
        die(str(exc))
    return normalize_skills_payload(data)


def index_local_path_or_none(index_uri: str) -> Optional[Path]:
    parsed = urllib.parse.urlparse(index_uri)
    if parsed.scheme in ("", "file"):
        return parse_path_like_uri(index_uri)
    return None


def skill_zip_uri(
    skill: Dict[str, Any],
    slug: str,
    index_path: Optional[Path],
    files_base_uri: str,
    download_url_template: str,
) -> str:
    if files_base_uri.strip():
        from_base = append_slug_zip(files_base_uri, slug)
        if from_base:
            return from_base

    if index_path is not None:
        sibling_files = (index_path.parent / "files" / f"{slug}.zip").resolve()
        if sibling_files.exists():
            return sibling_files.as_uri()

    for key in ("zip_url", "zipUrl", "archive_url", "archiveUrl", "file_url", "fileUrl"):
        raw = str(skill.get(key, "")).strip()
        if raw:
            if urllib.parse.urlparse(raw).scheme:
                return raw
            return Path(raw).expanduser().resolve().as_uri()

    if download_url_template.strip():
        return append_slug_zip(download_url_template, slug)

    die(
        f'Skill "{slug}" has no zip_url and no local archive found. '
        "Use --files-base-uri or --download-url-template."
    )
    return ""


def find_skill(data: Dict[str, Any], slug: str) -> Optional[Dict[str, Any]]:
    for item in data["skills"]:
        if isinstance(item, dict) and str(item.get("slug", "")).strip() == slug:
            return item
    return None


def cmd_search(args: argparse.Namespace) -> None:
    query_parts = args.query if isinstance(args.query, list) else [args.query]
    query = " ".join(str(part) for part in query_parts).lower().strip()
    json_out = bool(getattr(args, "json_output", False))
    if query:
        remote = fetch_remote_search_results(
            search_url=args.search_url,
            query=query,
            limit=args.search_limit,
            timeout=args.search_timeout,
        )
        if remote is not None:
            if json_out:
                print(
                    json.dumps(
                        {
                            "query": query,
                            "source": "remote",
                            "count": len(remote),
                            "results": remote,
                        },
                        ensure_ascii=False,
                    )
                )
                return
            print('You can use "skillhub install [skill]" to install.')
            for skill in remote:
                slug = skill.get("slug", "<unknown>")
                name = skill.get("name", slug)
                description = skill.get("description", "")
                version = skill.get("version", "")
                print(f"{slug}  {name}")
                if description:
                    print(f"  - {description}")
                if version:
                    print(f"  - version: {version}")
            return

    data = load_index(args.index)
    matches: List[Dict[str, Any]] = []
    for item in data["skills"]:
        if not isinstance(item, dict):
            continue
        matches.append(item)

    if not matches:
        print("No skills found.")
        return

    if query:
        def rank(skill: Dict[str, Any]) -> Tuple[int, str]:
            text = skill_text(skill)
            score = text.count(query)
            slug = str(skill.get("slug", ""))
            return (score, slug)

        matches.sort(key=rank, reverse=True)

    if json_out:
        results: List[Dict[str, Any]] = []
        for skill in matches:
            if not isinstance(skill, dict):
                continue
            slug = str(skill.get("slug") or "").strip()
            if not slug:
                continue
            name = str(skill.get("name") or skill.get("displayName") or slug).strip() or slug
            description = str(skill.get("description") or skill.get("summary") or "").strip()
            version = str(skill.get("version") or "").strip()
            results.append(
                {
                    "slug": slug,
                    "name": name,
                    "description": description,
                    "summary": str(skill.get("summary") or "").strip(),
                    "version": version,
                }
            )
        print(
            json.dumps(
                {
                    "query": query,
                    "source": "index",
                    "count": len(results),
                    "results": results,
                },
                ensure_ascii=False,
            )
        )
        return

    print('You can use "skillhub install [skill]" to install.')

    for skill in matches:
        slug = skill.get("slug", "<unknown>")
        name = skill.get("name", slug)
        description = skill.get("description", "")
        if not description:
            description = skill.get("summary", "")
        zip_url = skill.get("zip_url", "")
        homepage = skill.get("homepage", "")
        version = skill.get("version", "")
        print(f"{slug}  {name}")
        if description:
            print(f"  - {description}")
        if version:
            print(f"  - version: {version}")
        if zip_url:
            print(f"  - {zip_url}")
        if homepage and not is_clawhub_url(homepage):
            print(f"  - {homepage}")
