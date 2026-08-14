#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
pio run -e m5stack-cardputer -t upload
