#!/usr/bin/env bash
set -euo pipefail

echo "Resetting branch and discarding all changes..."
git reset --hard HEAD
git clean -fd
echo "Done."
