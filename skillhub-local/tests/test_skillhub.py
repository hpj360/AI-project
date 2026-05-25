import hashlib
import json
import os
import tempfile
import zipfile
from pathlib import Path

import pytest

from skillhub.version import parse_version_key, version_is_newer, version_at_least, parse_bool_like
from skillhub.archive import sha256_file, safe_extract_zip
from skillhub.lockfile import load_lockfile, save_lockfile
from skillhub.config import normalize_file_uri, parse_path_like_uri, append_slug_zip, fill_slug_template


class TestParseVersionKey:
    def test_simple_semver(self):
        assert parse_version_key("1.2.3") == (1, 2, 3)

    def test_with_v_prefix(self):
        assert parse_version_key("v2.0.1") == (2, 0, 1)

    def test_with_prerelease(self):
        assert parse_version_key("1.0.0-beta.1") == (1, 0, 0)

    def test_with_build_metadata(self):
        assert parse_version_key("1.0.0+build.123") == (1, 0, 0)

    def test_empty_string(self):
        assert parse_version_key("") is None

    def test_non_numeric(self):
        assert parse_version_key("abc") is None

    def test_two_parts(self):
        assert parse_version_key("1.0") == (1, 0)

    def test_single_part(self):
        assert parse_version_key("5") == (5,)

    def test_whitespace(self):
        assert parse_version_key("  3.2.1  ") == (3, 2, 1)


class TestVersionIsNewer:
    def test_major_newer(self):
        assert version_is_newer("2.0.0", "1.0.0") is True

    def test_minor_newer(self):
        assert version_is_newer("1.1.0", "1.0.0") is True

    def test_patch_newer(self):
        assert version_is_newer("1.0.1", "1.0.0") is True

    def test_same_version(self):
        assert version_is_newer("1.0.0", "1.0.0") is False

    def test_older(self):
        assert version_is_newer("1.0.0", "2.0.0") is False

    def test_empty_candidate(self):
        assert version_is_newer("", "1.0.0") is False

    def test_empty_current(self):
        assert version_is_newer("1.0.0", "") is True

    def test_both_empty(self):
        assert version_is_newer("", "") is False

    def test_prerelease_vs_release(self):
        assert version_is_newer("1.0.0", "1.0.0-beta.1") is False

    def test_prerelease_vs_release_note(self):
        assert version_is_newer("1.0.0", "1.0.0-beta.1") is False
        assert version_is_newer("1.0.1", "1.0.0-beta.1") is True

    def test_different_lengths(self):
        assert version_is_newer("1.2.3.4", "1.2.3") is True


class TestVersionAtLeast:
    def test_at_least_true(self):
        assert version_at_least("3.14.0", (3, 13)) is True

    def test_at_least_equal(self):
        assert version_at_least("3.13.0", (3, 13)) is True

    def test_at_least_false(self):
        assert version_at_least("3.12.0", (3, 13)) is False

    def test_invalid_version(self):
        assert version_at_least("abc", (1, 0)) is False


class TestParseBoolLike:
    def test_true_strings(self):
        for val in ("1", "true", "True", "TRUE", "yes", "Yes", "on", "On"):
            assert parse_bool_like(val) is True

    def test_false_strings(self):
        for val in ("0", "false", "False", "FALSE", "no", "No", "off", "Off"):
            assert parse_bool_like(val) is False

    def test_bool_input(self):
        assert parse_bool_like(True) is True
        assert parse_bool_like(False) is False

    def test_int_input(self):
        assert parse_bool_like(1) is True
        assert parse_bool_like(0) is False

    def test_none_for_invalid(self):
        assert parse_bool_like("maybe") is None
        assert parse_bool_like(None) is None

    def test_whitespace(self):
        assert parse_bool_like("  true  ") is True


class TestSha256File:
    def test_known_content(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
            content = b"hello world"
            f.write(content)
            f.flush()
            name = f.name
        try:
            expected = hashlib.sha256(content).hexdigest()
            assert sha256_file(Path(name)) == expected
        finally:
            os.unlink(name)

    def test_empty_file(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
            name = f.name
        try:
            expected = hashlib.sha256(b"").hexdigest()
            assert sha256_file(Path(name)) == expected
        finally:
            os.unlink(name)


class TestSafeExtractZip:
    def test_normal_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            zip_path = Path(tmp) / "test.zip"
            extract_dir = Path(tmp) / "out"
            extract_dir.mkdir()
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.writestr("hello.txt", "hello")
            safe_extract_zip(zip_path, extract_dir)
            assert (extract_dir / "hello.txt").read_text() == "hello"

    def test_path_traversal_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            zip_path = Path(tmp) / "evil.zip"
            extract_dir = Path(tmp) / "out"
            extract_dir.mkdir()
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.writestr("../etc/passwd", "evil")
            with pytest.raises(SystemExit):
                safe_extract_zip(zip_path, extract_dir)

    def test_absolute_path_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            zip_path = Path(tmp) / "evil2.zip"
            extract_dir = Path(tmp) / "out"
            extract_dir.mkdir()
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.writestr("C:\\Windows\\system32\\config\\SAM", "evil")
            with pytest.raises(SystemExit):
                safe_extract_zip(zip_path, extract_dir)


class TestLockfile:
    def test_load_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            lock = load_lockfile(Path(tmp))
            assert lock == {"version": 1, "skills": {}}

    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = {"version": 1, "skills": {"test-skill": {"version": "1.0.0"}}}
            save_lockfile(root, data)
            loaded = load_lockfile(root)
            assert loaded["skills"]["test-skill"]["version"] == "1.0.0"

    def test_load_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".skills_store_lock.json").write_text("not json", encoding="utf-8")
            lock = load_lockfile(root)
            assert lock == {"version": 1, "skills": {}}


class TestNormalizeFileUri:
    def test_file_uri(self):
        result = normalize_file_uri("file:///tmp/test")
        assert str(result).endswith("tmp/test") or str(result).endswith("tmp\\test")

    def test_plain_path(self):
        result = normalize_file_uri("/tmp/test")
        assert "tmp" in str(result)


class TestFillSlugTemplate:
    def test_with_slug_placeholder(self):
        assert fill_slug_template("https://example.com/{slug}.zip", "my-skill") == \
            "https://example.com/my-skill.zip"

    def test_without_placeholder(self):
        assert fill_slug_template("https://example.com/skills.zip", "my-skill") == \
            "https://example.com/skills.zip"

    def test_empty_template(self):
        assert fill_slug_template("", "my-skill") == ""
