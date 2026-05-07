#!/bin/bash
# =============================================================================
# setup.sh — Get Pizza Quest ready to play!
#
# What this script does:
#   1. Figures out what kind of computer you're on
#   2. Installs any system packages that pygame needs (Raspberry Pi only)
#   3. Creates a "virtual environment" — a private folder for Python packages
#   4. Installs pygame inside that folder
#
# You can run this script as many times as you want — it won't break anything!
# =============================================================================

# Stop immediately if anything goes wrong so the error is easy to spot.
set -e

echo ""
echo "==============================="
echo "  Pizza Quest — Setup"
echo "==============================="

# ---------------------------------------------------------------------------
# Step 1 — Detect the computer type
# ---------------------------------------------------------------------------
# 'uname' prints the operating system name.
# We use it to decide whether we're on a Raspberry Pi / Linux or a Mac.

OS_TYPE=$(uname -s)   # "Linux" or "Darwin" (Mac)

# On Linux, check if we're on a Raspberry Pi specifically.
IS_PI=false
if [ "$OS_TYPE" = "Linux" ] && grep -qi "raspberry pi\|raspbian" /proc/cpuinfo /etc/os-release 2>/dev/null; then
    IS_PI=true
fi

if [ "$IS_PI" = true ]; then
    echo ""
    echo ">>> Raspberry Pi detected!"
elif [ "$OS_TYPE" = "Darwin" ]; then
    echo ""
    echo ">>> Mac detected."
else
    echo ""
    echo ">>> Linux detected."
fi

# ---------------------------------------------------------------------------
# Step 2 — Install system-level SDL libraries (Raspberry Pi only)
# ---------------------------------------------------------------------------
# pygame is built on top of a library called SDL. On a Raspberry Pi running
# Raspberry Pi OS, we need to make sure those system libraries are installed
# before we can use pygame.
#
# On Mac this step is skipped — homebrew or pip handles it automatically.

if [ "$IS_PI" = true ]; then
    echo ""
    echo ">>> Checking SDL system libraries (needed by pygame on Pi)..."

    # 'dpkg -s' checks if a package is already installed.
    # We only run apt-get if something is missing.
    NEED_INSTALL=false
    for pkg in libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev; do
        if ! dpkg -s "$pkg" > /dev/null 2>&1; then
            NEED_INSTALL=true
            break
        fi
    done

    if [ "$NEED_INSTALL" = true ]; then
        echo "    Installing missing SDL libraries (you may be asked for your password)..."
        sudo apt-get update -qq
        sudo apt-get install -y -qq \
            libsdl2-dev libsdl2-image-dev \
            libsdl2-mixer-dev libsdl2-ttf-dev \
            python3-dev
        echo "    Done!"
    else
        echo "    All SDL libraries already installed — skipping."
    fi
fi

# ---------------------------------------------------------------------------
# Step 3 — Find Python 3
# ---------------------------------------------------------------------------

echo ""
echo ">>> Looking for Python 3..."

# Try 'python3' first, then plain 'python'.
if command -v python3 > /dev/null 2>&1; then
    PYTHON=python3
elif command -v python > /dev/null 2>&1; then
    PYTHON=python
else
    echo ""
    echo "ERROR: Python 3 was not found."
    echo "On Raspberry Pi: sudo apt-get install python3"
    echo "On Mac: https://www.python.org/downloads/"
    exit 1
fi

PY_VERSION=$($PYTHON --version 2>&1)
echo "    Found: $PY_VERSION"

# ---------------------------------------------------------------------------
# Step 4 — Create the virtual environment (skip if it already exists)
# ---------------------------------------------------------------------------
# A virtual environment is like a lunchbox just for this project's Python
# packages. It keeps things tidy and won't affect anything else on the computer.

VENV_DIR="venv"

echo ""
echo ">>> Setting up virtual environment in './$VENV_DIR' ..."

if [ -d "$VENV_DIR" ]; then
    echo "    Already exists — skipping."
else
    $PYTHON -m venv "$VENV_DIR"
    echo "    Created!"
fi

# ---------------------------------------------------------------------------
# Step 5 — Install pygame
# ---------------------------------------------------------------------------

echo ""
echo ">>> Installing packages from game/requirements.txt ..."

# Upgrade pip first so we get the best wheel (pre-built package) selection.
"$VENV_DIR/bin/pip" install --upgrade pip --quiet

# Install everything listed in requirements.txt.
"$VENV_DIR/bin/pip" install -r game/requirements.txt

echo "    Done!"

# ---------------------------------------------------------------------------
# All finished!
# ---------------------------------------------------------------------------

echo ""
echo "============================================================"
echo "  All done! To start the game, run:"
echo ""
echo "    source venv/bin/activate"
echo "    python run.py"
echo ""
echo "  Tip: you only need to run setup.sh once. After that,"
echo "  just activate the environment and run run.py."
echo "============================================================"
echo ""
