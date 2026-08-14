# esPod

esPod is a portable local-audio player for podcasts and MP3s, built for ESP32-family handheld hardware and designed to remain reusable across future appliance targets.

This directory is the active working space for the new embedded audio project.

## Purpose

This project intentionally starts fresh and separate from the archived TrimUI Smart Pro / Rockbox effort. The old work is preserved in the neighboring `rockbox` tree as historical reference only.

The long-term goal is to build reusable embedded software for a portable local-audio player that can run across ESP32-family handheld hardware and later adapt to a dedicated appliance or CM0-based hardware target.

This project is intentionally designed as reusable embedded software, not as a board-specific one-off.

## Target device

- Primary target: M5Stack Cardputer ADV
- MCU: ESP32-S3
- Platform: PlatformIO + Arduino framework
- Status: bring-up ready; hardware validation pending actual device arrival

## Goal

Build a viable handheld audio / UI product around the Cardputer ADV platform with a clear, repeatable, hardware-first development flow and minimal dependence on browser-based simulators.

This project is a portable local-audio player for both podcasts and MP3s, with playback telemetry, smart playlists, and visual media browsing as core product features.

The software stack is intended to remain reusable across future hardware targets, including a dedicated ESP32 board and a CM0-based appliance form factor.

## Vision

esPod is meant to be more than a single-device app. It is a reusable embedded software foundation for:

- handheld ESP32 music and podcast devices
- dedicated ESP32-based audio appliances
- future low-power appliance targets with a shared audio and library stack

This keeps the project flexible while still starting with the Cardputer ADV as the validation target.

## Product requirements

- Local podcast playback
- Local MP3 playback
- Unified library browsing
- Playback analytics and skip/play counts
- Resume-aware playback state
- Smart playlist generation based on listening habits
- Cover art for current item, library entries, and podcast metadata
- Artwork fallback paths for embedded art, folder art, and podcast feed images

## Current setup

The project has been configured for a supported ESP32-S3 toolchain path rather than the earlier invalid board ID attempt.

This is intended to be a reusable software foundation rather than a board-specific one-off. The focus is on portable firmware architecture, hardware abstractions, and repeatable build tooling.

- Toolchain: PlatformIO in a local virtual environment
- Environment path: `~/.venvs/cardputer`
- Board target: `esp32-s3-devkitc-1`
- Required USB fix: install PlatformIO udev rules for Linux

## USB rules requirement

If the board is not visible to PlatformIO or upload fails with permission issues, install the rules:

```bash
curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core/develop/platformio/udev/rules.d/99-platformio-udev.rules | sudo tee /etc/udev/rules.d/99-platformio-udev.rules >/dev/null
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Then unplug and replug the board before flashing or monitoring.

## Build and validation flow

### Local build

```bash
cd /home/triconda/.vscode/tmp/tmp_vscode_1/cardputer-esp32-target
source /home/triconda/.venvs/cardputer/bin/activate.fish
pio run -e m5stack-cardputer
```

### Upload to device

```bash
pio run -e m5stack-cardputer -t upload
```

### Serial monitor

```bash
pio device monitor -b 115200
```

## Roadmap / checklist

This project should be executed as a staged hardware-first roadmap. Do not add product features until each milestone is proven on the real device.

### Phase 1: Device bring-up
- [ ] Confirm the Cardputer ADV is detected over USB
- [ ] Install PlatformIO udev rules if required
- [ ] Build the project successfully
- [ ] Upload the boot firmware to the board
- [ ] Confirm serial output on the console
- [ ] Confirm the LCD renders text and basic UI elements
- [ ] Confirm button input events trigger expected actions

### Phase 2: Audio and storage validation
- [ ] Confirm speaker output path and PWM / DAC behavior
- [ ] Play a short audio test tone or PCM clip successfully
- [ ] Validate SD card mounting and read access
- [ ] Confirm file listing from local storage works
- [ ] Validate cover-art extraction for local media and podcast metadata

### Phase 3: Core app slice
- [ ] Build a minimal local media browser
- [ ] Select a sample audio file and play it
- [ ] Add pause / resume / stop controls
- [ ] Add simple persistent state tracking for last played item
- [ ] Display current artwork on the playback screen

### Phase 4: Podcast product flow
- [ ] Add podcast directory or feed discovery flow
- [ ] Add queue / episode selection
- [ ] Add playback progress persistence
- [ ] Add resume behavior across reboots
- [ ] Validate podcast cover art and feed image handling
- [ ] Validate battery and thermal behavior under real use

### Phase 5: Polish and release gate
- [ ] Final UI pass for readability and button mapping
- [ ] Audio quality and latency checks
- [ ] Artwork consistency pass across genres, podcast feeds, and local files
- [ ] Reliability / crash-check pass
- [ ] Final device validation checklist

## Structure

- `docs/` — target notes, design decisions, constraints, and research
- `src/` — application code and platform-specific implementation
- `scripts/` — build, flash, and monitor helpers
- `platformio.ini` — PlatformIO project configuration
- `.gitignore` — project-local ignore rules

## Status

- Active target: Cardputer ADV / ESP32-S3
- Future targets: dedicated ESP32 board, CM0 appliance platform
- Archived target: TrimUI Smart Pro / PortMaster / Rockbox
- Working assumption: do not reuse the dead-end Rockbox plugin path unless it becomes a clearly supported platform again
- Current validation state: toolchain and project configuration are ready; real hardware validation remains pending arrival of the device
- Architecture priority: reusable software layers over hardware-specific code

## Notes

Keep this tree focused on:

- device-specific constraints
- maintainable firmware workflow
- reproducible build steps
- testable validation paths

This directory should remain independent from the old Rockbox repo so the new effort is not polluted by stale artifact assumptions.
