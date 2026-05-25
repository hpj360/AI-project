# -*- coding: utf-8 -*-
import json
import shutil
import ssl
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

from skillhub.config import CLI_USER_AGENT, MAX_HTTP_REDIRECTS, die, parse_path_like_uri


def _make_ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.check_hostname = True
    return ctx


class _RedirectLimitHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not hasattr(self, "_redirect_count"):
            self._redirect_count = 0
        self._redirect_count += 1
        if self._redirect_count > MAX_HTTP_REDIRECTS:
            raise urllib.error.HTTPError(
                req.full_url, code,
                f"Too many redirects (>{MAX_HTTP_REDIRECTS})",
                headers, fp,
            )
        parsed = urllib.parse.urlparse(newurl)
        if parsed.scheme not in ("http", "https"):
            raise urllib.error.HTTPError(
                req.full_url, code,
                f"Unsafe redirect target scheme: {parsed.scheme}",
                headers, fp,
            )
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _safe_urlopen(req: urllib.request.Request, timeout: int = 30) -> Any:
    opener = urllib.request.build_opener(
        _RedirectLimitHandler,
        urllib.request.HTTPSHandler(context=_make_ssl_context()),
    )
    return opener.open(req, timeout=timeout)


def read_json_from_uri(uri_or_path: str, timeout: int = 20) -> Dict[str, Any]:
    parsed = urllib.parse.urlparse(uri_or_path)
    if parsed.scheme in ("", "file"):
        path = parse_path_like_uri(uri_or_path)
        if not path.exists():
            raise RuntimeError(f"JSON source not found: {path}")
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid JSON in {path}: {exc}") from exc
    elif parsed.scheme in ("http", "https"):
        req = urllib.request.Request(
            uri_or_path,
            headers={
                "User-Agent": CLI_USER_AGENT,
                "Accept": "application/json",
            },
        )
        try:
            with _safe_urlopen(req, timeout=timeout) as response:
                payload = response.read().decode("utf-8")
                raw = json.loads(payload)
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"Failed to fetch JSON ({exc.code}) from {uri_or_path}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Failed to fetch JSON from {uri_or_path}: {exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid JSON from {uri_or_path}: {exc}") from exc
    else:
        raise RuntimeError(f"Unsupported URI scheme for JSON source: {uri_or_path}")

    if not isinstance(raw, dict):
        raise RuntimeError(f"JSON source must be an object: {uri_or_path}")
    return raw


def download_file_or_raise(url: str, dest: Path) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme == "file":
        source_path = parse_path_like_uri(url)
        if not source_path.exists():
            raise RuntimeError(f"Download failed: local file not found: {source_path}")
        shutil.copyfile(source_path, dest)
        return
    if parsed.scheme == "":
        source_path = Path(url).expanduser().resolve()
        if source_path.exists():
            shutil.copyfile(source_path, dest)
            return

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": CLI_USER_AGENT,
            "Accept": "application/zip,application/octet-stream,*/*",
        },
    )
    try:
        with _safe_urlopen(req, timeout=30) as response:
            if response.status and response.status >= 400:
                raise RuntimeError(f"Download failed ({response.status}) for {url}")
            with dest.open("wb") as out:
                shutil.copyfileobj(response, out)
    except urllib.error.HTTPError as exc:
        detail = f"HTTP {exc.code}"
        if exc.code == 429:
            detail += " (rate limited)"
        raise RuntimeError(f"Download failed: {detail} for {url}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Download failed: {exc.reason} for {url}") from exc


def download_file(url: str, dest: Path) -> None:
    try:
        download_file_or_raise(url, dest)
    except Exception as exc:
        die(str(exc))


def fetch_remote_search_results(
    search_url: str,
    query: str,
    limit: int,
    timeout: int,
) -> Optional[List[Dict[str, Any]]]:
    base = str(search_url or "").strip()
    q = str(query or "").strip()
    if not base or not q:
        return None
    try:
        parsed = urllib.parse.urlparse(base)
        if parsed.scheme not in ("http", "https"):
            return None
        params = urllib.parse.urlencode({"q": q, "limit": max(1, int(limit))})
        full_url = urllib.parse.urlunparse(
            (parsed.scheme, parsed.netloc, parsed.path, parsed.params, params, parsed.fragment)
        )
        req = urllib.request.Request(
            full_url,
            headers={
                "User-Agent": CLI_USER_AGENT,
                "Accept": "application/json",
            },
        )
        with _safe_urlopen(req, timeout=max(1, int(timeout))) as response:
            payload = response.read().decode("utf-8")
        raw = json.loads(payload)
        if not isinstance(raw, dict):
            return None
        results = raw.get("results")
        if not isinstance(results, list):
            return None
        out: List[Dict[str, Any]] = []
        for item in results:
            if not isinstance(item, dict):
                continue
            slug = str(item.get("slug", "")).strip()
            if not slug:
                continue
            out.append(
                {
                    "slug": slug,
                    "name": str(item.get("displayName") or item.get("name") or slug).strip() or slug,
                    "description": str(item.get("summary") or item.get("description") or "").strip(),
                    "summary": str(item.get("summary") or "").strip(),
                    "version": str(item.get("version") or "").strip(),
                }
            )
        return out
    except Exception:
        return None
