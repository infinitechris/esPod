# Device Dataset v1

`esPod` consumes the portable dataset exported by `pyPodcastCatcher`:

```text
device-export/
  manifest.json
  media/<podcast directory>/<episode filename>.mp3
```

The manifest is UTF-8 JSON with `schema_version: 1`. Each `episodes` entry
contains `feed_url`, `episode_key`, display metadata, the authoritative POSIX
`relative_path`, file size, SHA-256 checksum, and playback state.

The firmware must identify episodes by `feed_url` plus `episode_key`, never by
desktop SQLite row IDs or filenames. `relative_path` is authoritative and
must be resolved beneath the dataset root after rejecting path traversal.

The exporter includes only episodes whose local audio file exists. Artwork is
not copied separately; the MP3 may contain embedded ID3 APIC artwork. The
firmware should try embedded artwork first, then optional folder artwork.

The device should reject unsupported schema versions, tolerate unknown fields,
and write playback changes to a device-local state file. It must not require
SQLite or the Python application to browse and play the dataset.