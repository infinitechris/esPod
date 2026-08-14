# Target Notes

## Device choice

- Primary candidate: Cardputer
- Secondary candidate: ESP32-based board with a compact UI and practical battery / I/O support

## Why this target

- More flexible dev path than the dead-end Rockbox plugin target
- Better chance of a working, reproducible handheld product
- Easier to test and iterate locally
- Clearer runtime and build ownership

## Constraints

- Avoid reusing unsupported plugin assumptions from the TrimUI work
- Keep device integration simple and hardware-aware
- Prefer a build and deploy path that can be repeated without hidden runtime requirements

## Next actions

1. Select the specific Cardputer / ESP32 board model
2. Confirm display, audio, and input capabilities
3. Define the minimal application structure
4. Set up build and flash toolchain
5. Validate the app on hardware before broadening scope
