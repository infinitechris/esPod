# Source

Place application code here.

Suggested layout:

- `app/` — main application flow
- `ui/` — display and input handling
- `audio/` — playback and audio logic
- `storage/` — local data, config, and manifests
- `platform/` — board-specific integration code

Keep the code split by responsibility so the project stays readable while the target device is still being validated.

The storage layer should implement the dataset contract in
`docs/device-dataset-v1.md`. Keep manifest parsing, path validation, and
device-local playback state separate from audio playback and UI code.
