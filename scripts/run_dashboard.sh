#!/usr/bin/env bash
set -euo pipefail

# Always run from the repo root
cd "$(dirname "$0")/.."

# Activate the project venv
source .venv/bin/activate

# Run Streamlit
exec streamlit run dashboard/app.py