import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "tools"))

from validate_device_dataset import DatasetError, validate_dataset


def _write_dataset(tmp_path, relative_path="media/Example/episode.mp3"):
    media_path = tmp_path / "media/Example/episode.mp3"
    media_path.parent.mkdir(parents=True)
    media_path.write_bytes(b"audio fixture")
    manifest = {
        "schema_version": 1,
        "episodes": [
            {
                "feed_url": "https://example.com/feed.xml",
                "episode_key": "https://example.com/episode.mp3",
                "podcast_title": "Example",
                "episode_title": "Episode",
                "relative_path": relative_path,
                "byte_size": media_path.stat().st_size,
                "sha256": hashlib.sha256(media_path.read_bytes()).hexdigest(),
            }
        ],
    }
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")


def test_validates_media_path_size_and_checksum(tmp_path):
    _write_dataset(tmp_path)

    entries = validate_dataset(tmp_path)

    assert len(entries) == 1


@pytest.mark.parametrize("relative_path", ["../episode.mp3", "/tmp/episode.mp3", "media/../episode.mp3"])
def test_rejects_unsafe_media_paths(tmp_path, relative_path):
    _write_dataset(tmp_path, relative_path)

    with pytest.raises(DatasetError, match="relative_path"):
        validate_dataset(tmp_path)


def test_rejects_checksum_mismatch(tmp_path):
    _write_dataset(tmp_path)
    manifest_path = tmp_path / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["episodes"][0]["sha256"] = "0" * 64
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(DatasetError, match="checksum"):
        validate_dataset(tmp_path)