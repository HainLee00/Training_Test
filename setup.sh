#!/usr/bin/env bash
# setup.sh – one-shot setup script for the free-tools trading agent
#
# Usage:
#   bash setup.sh [MODEL_NAME]
#   Example: bash setup.sh qwen2.5:3b
#
# What it does:
#   1. Checks Python version (3.10+)
#   2. Creates a virtual environment
#   3. Installs all Python dependencies
#   4. Checks Ollama is installed and running
#   5. Pulls the chosen Ollama model

set -euo pipefail

MODEL="${1:-llama3.1:8b}"
VENV_DIR=".venv"

# ── Helpers ────────────────────────────────────────────────────────────────────
info()  { echo -e "\033[1;34m[INFO]\033[0m  $*"; }
ok()    { echo -e "\033[1;32m[ OK ]\033[0m  $*"; }
warn()  { echo -e "\033[1;33m[WARN]\033[0m  $*"; }
err()   { echo -e "\033[1;31m[ERR ]\033[0m  $*"; exit 1; }

# ── 1. Python version check ────────────────────────────────────────────────────
info "Checking Python version …"
PYTHON=$(command -v python3 || command -v python || err "Python not found.")
PY_VER=$("$PYTHON" -c "import sys; print(sys.version_info[:2])" 2>/dev/null)
"$PYTHON" -c "
import sys
if sys.version_info < (3, 10):
    print('[ERR]  Python 3.10+ required, found', sys.version)
    sys.exit(1)
"
ok "Python version OK"

# ── 2. Virtual environment ─────────────────────────────────────────────────────
if [ ! -d "$VENV_DIR" ]; then
    info "Creating virtual environment in $VENV_DIR …"
    "$PYTHON" -m venv "$VENV_DIR"
    ok "Virtual environment created"
else
    info "Virtual environment already exists at $VENV_DIR"
fi

# Activate
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# ── 3. Install dependencies ────────────────────────────────────────────────────
info "Upgrading pip …"
pip install --quiet --upgrade pip

info "Installing Python dependencies (this may take a few minutes) …"
pip install --quiet -e ".[dev]" 2>/dev/null || pip install --quiet -e .
ok "Python dependencies installed"

# ── 4. Copy .env if it does not exist ─────────────────────────────────────────
if [ ! -f ".env" ]; then
    cp .env.example .env
    info "Created .env from .env.example – review it to change the default model."
fi

# ── 5. Ollama checks ───────────────────────────────────────────────────────────
info "Checking for Ollama …"
if ! command -v ollama &>/dev/null; then
    warn "Ollama is not installed."
    echo ""
    echo "  Install Ollama from: https://ollama.com/download"
    echo "  Then run:  ollama serve"
    echo "  Then run:  ollama pull ${MODEL}"
    echo ""
    echo "  After that, rerun:  bash setup.sh"
    exit 0
fi
ok "Ollama found at $(command -v ollama)"

info "Checking Ollama server …"
if curl --silent --fail http://localhost:11434/api/tags >/dev/null 2>&1; then
    ok "Ollama server is running"
else
    warn "Ollama server is not running. Start it with: ollama serve"
    echo "  Then pull the model: ollama pull ${MODEL}"
    exit 0
fi

# ── 6. Pull model ──────────────────────────────────────────────────────────────
info "Pulling model '${MODEL}' (may download several GB on first run) …"
ollama pull "${MODEL}"
ok "Model '${MODEL}' ready"

# ── Done ───────────────────────────────────────────────────────────────────────
echo ""
echo -e "\033[1;32m✔ Setup complete!\033[0m"
echo ""
echo "  Activate the virtual environment:"
echo "    source $VENV_DIR/bin/activate"
echo ""
echo "  Run an analysis:"
echo "    python main.py --ticker AAPL --date 2024-05-10 --debug"
echo ""
