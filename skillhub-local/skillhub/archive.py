# -*- coding: utf-8 -*-
import hashlib
import shutil
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path
from typing import List

from skillhub.config import die
from skillhub.http import download_file, download_file_or_raise


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_extract_zip(zip_path: Path, target_dir: Path) -> None:
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.infolist():
            member_path = Path(member.filename)
            if member_path.is_absolute() or ".." in member_path.parts:
                die(f"Unsafe zip path entry detected: {member.filename}")
        zf.extractall(target_dir)


def safe_extract_tar(tar_path: Path, target_dir: Path) -> None:
    with tarfile.open(tar_path, "r:*") as tf:
        for member in tf.getmembers():
            member_path = Path(member.name)
            if member_path.is_absolute() or ".." in member_path.parts:
                die(f"Unsafe tar path entry detected: {member.name}")
        try:
            tf.extractall(target_dir, filter="data")
        except TypeError:
            tf.extractall(target_dir)


def install_zip_to_target(
    slug: str,
    zip_uri: str,
    target_dir: Path,
    force: bool,
    expected_sha256: str = "",
) -> None:
    if target_dir.exists() and not force:
        die(f"Target exists: {target_dir} (use --force to overwrite)")

    with tempfile.TemporaryDirectory(prefix="skills-store-cli-") as tmp:
        zip_path = Path(tmp) / f"{slug}.zip"
        stage_dir = Path(tmp) / "stage"
        stage_dir.mkdir(parents=True, exist_ok=True)
        print(f"Downloading: {zip_uri}")
        download_file(zip_uri, zip_path)

        if expected_sha256:
            actual_sha256 = sha256_file(zip_path).lower()
            if actual_sha256 != expected_sha256:
                die(
                    f"SHA256 mismatch for {slug}: expected {expected_sha256}, got {actual_sha256}"
                )
        try:
            safe_extract_zip(zip_path, stage_dir)
        except zipfile.BadZipFile:
            die(f"Downloaded file is not a valid zip archive: {zip_uri}")

        if target_dir.exists():
            if not force:
                die(f"Target exists: {target_dir} (use --force to overwrite)")
            shutil.rmtree(target_dir)
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(stage_dir), str(target_dir))


def install_zip_to_target_with_fallback(
    slug: str,
    zip_uris: List[str],
    target_dir: Path,
    force: bool,
    expected_sha256: str = "",
) -> None:
    candidates = [str(x).strip() for x in zip_uris if str(x).strip()]
    seen = set()
    ordered: List[str] = []
    for x in candidates:
        if x in seen:
            continue
        seen.add(x)
        ordered.append(x)
    if not ordered:
        die(f'No download URL candidates for "{slug}"')

    if target_dir.exists() and not force:
        die(f"Target exists: {target_dir} (use --force to overwrite)")

    with tempfile.TemporaryDirectory(prefix="skills-store-cli-") as tmp:
        zip_path = Path(tmp) / f"{slug}.zip"
        stage_dir = Path(tmp) / "stage"
        stage_dir.mkdir(parents=True, exist_ok=True)
        last_err = ""
        used_uri = ""
        for idx, zip_uri in enumerate(ordered):
            try:
                print(f"Downloading: {zip_uri}")
                download_file_or_raise(zip_uri, zip_path)
                used_uri = zip_uri
                last_err = ""
                break
            except Exception as exc:
                last_err = str(exc)
                if idx + 1 < len(ordered):
                    print(f"Download failed, fallback next source: {exc}", file=sys.stderr)
                    continue
        if last_err:
            die(last_err)

        if expected_sha256:
            actual_sha256 = sha256_file(zip_path).lower()
            if actual_sha256 != expected_sha256:
                die(
                    f"SHA256 mismatch for {slug}: expected {expected_sha256}, got {actual_sha256}"
                )
        try:
            safe_extract_zip(zip_path, stage_dir)
        except zipfile.BadZipFile:
            die(f"Downloaded file is not a valid zip archive: {used_uri or ordered[0]}")

        if target_dir.exists():
            if not force:
                die(f"Target exists: {target_dir} (use --force to overwrite)")
            shutil.rmtree(target_dir)
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(stage_dir), str(target_dir))
