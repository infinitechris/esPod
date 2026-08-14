#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
pio device monitor -b 115200
