#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

export UV_CACHE_DIR="$APP_DIR/.uv-cache"

if command -v xdg-open >/dev/null 2>&1; then
  (sleep 3; xdg-open "http://localhost:8501" >/dev/null 2>&1 || true) &
fi

uv run streamlit run app.py --server.headless true --server.address localhost --server.port 8501
