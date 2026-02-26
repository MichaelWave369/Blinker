#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv
source .venv/bin/activate
pip install -r server/requirements.txt
(cd web && npm ci)
BLINKER_USE_MOCK=true uvicorn server.app.main:app --reload --host 127.0.0.1 --port 8090 &
(cd web && npm run dev)
