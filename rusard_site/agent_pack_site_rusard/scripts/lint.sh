#!/usr/bin/env bash
set -euo pipefail
ruff check .
python -m compileall -q .
