from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SUPPORTED_SCHEMA_VERSION = 1
REQUIRED_ENTRY_FIELDS = {
    "feed_url",
    "episode_key",
    "podcast_title",
    "episode_title",
    "relative_path",
    "byte_size",
    "sha256",
}


class DatasetError(ValueError):
    """Raised when a device dataset violates the v1 contract."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_dataset_path(root: Path, relative_path: str) -> Path:
    candidate = Path(relative_path)
    if candidate.is_absolute() or candidate.as_posix() != relative_path or ".." in candidate.parts:
        raise DatasetError(f"unsafe relative_path: {relative_path}")
    resolved_root = root.resolve()
    resolved_path = (root / candidate).resolve()
    try:
        resolved_path.relative_to(resolved_root)
    except ValueError as exc:
        raise DatasetError(f"relative_path escapes dataset: {relative_path}") from exc
    return resolved_path


def validate_dataset(dataset_dir: str | Path) -> list[dict[str, Any]]:
    root = Path(dataset_dir)
    manifest_path = root / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DatasetError("manifest.json is missing") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise DatasetError("manifest.json is not valid UTF-8 JSON") from exc

    if not isinstance(manifest, dict) or manifest.get("schema_version") != SUPPORTED_SCHEMA_VERSION:
        raise DatasetError("unsupported manifest schema_version")
    episodes = manifest.get("episodes")
    if not isinstance(episodes, list):
        raise DatasetError("manifest episodes must be a list")

    seen_keys: set[tuple[str, str]] = set()
    for entry in episodes:
        if not isinstance(entry, dict) or not REQUIRED_ENTRY_FIELDS.issubset(entry):
            raise DatasetError("episode entry is missing required fields")
        identity = (str(entry["feed_url"]), str(entry["episode_key"]))
        if identity in seen_keys:
            raise DatasetError(f"duplicate episode identity: {identity[0]}|{identity[1]}")
        seen_keys.add(identity)

        relative_path = entry["relative_path"]
        if not isinstance(relative_path, str) or not relative_path.startswith("media/"):
            raise DatasetError("episode relative_path must be a media path")
        media_path = _safe_dataset_path(root, relative_path)
        if not media_path.is_file():
            raise DatasetError(f"media file is missing: {relative_path}")
        if entry["byte_size"] != media_path.stat().st_size:
            raise DatasetError(f"media size mismatch: {relative_path}")
        if entry["sha256"] != _sha256(media_path):
            raise DatasetError(f"media checksum mismatch: {relative_path}")

    return episodes


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an esPod device dataset")
    parser.add_argument("dataset", nargs="?", default="device-export")
    args = parser.parse_args()
    try:
        episodes = validate_dataset(args.dataset)
    except DatasetError as exc:
        parser.error(str(exc))
    print(f"Valid device dataset: {len(episodes)} episode(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())