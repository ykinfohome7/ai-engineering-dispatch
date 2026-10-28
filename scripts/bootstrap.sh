#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m pip install --user --no-build-isolation -e . 2>/dev/null || {
  echo 'Editable pip install skipped; using PYTHONPATH=src for tests.'
}
PYTHONPATH=src python3 -m unittest discover -s tests -v
printf '\nBGDB AI-EMDS initialized. Run: PYTHONPATH=src python3 -m bgdb_dispatch.cli roles\n'
