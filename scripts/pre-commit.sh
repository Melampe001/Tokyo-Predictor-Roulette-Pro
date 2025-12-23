#!/usr/bin/env bash
set -euo pipefail
echo "Running make fmt before commit..."
if command -v make >/dev/null 2>&1; then
  make fmt
else
  echo "make not found, attempting to run black directly..."
  if command -v black >/dev/null 2>&1; then
    black .
  else
    echo "black not installed. Install with: pip install black"
    exit 1
  fi
fi
echo "Formatting complete."
# Exit 0 to allow commit; remove or change to run tests if you want to block commits on failing tests
exit 0
