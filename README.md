# Blinker v0.2.0

Blinker is a **local-first** Blink camera monitoring app with optional AI-assisted summaries and lightweight vision tagging.

## What Blinker does
- Connects to your Blink account via an unofficial adapter (`blinkpy` implementation scaffold + mock client for tests/dev).
- Syncs cameras, motion events, and clip metadata into local SQLite.
- Stores clips and thumbnails under local media folders.
- Provides timeline search (`/api/events/search`) by camera, summary text, and tags.
- Adds local-only rules engine to mark events important and create notifications.
- Adds lightweight vision tags from thumbnails (heuristic by default, optional OpenCV fallback plugin).
- Generates snapshot PNG and daily digest reports.

## What Blinker does NOT do
- No guaranteed live local LAN streaming.
- No cloud AI dependency required.
- No telemetry, scraping, or hidden outbound calls.

## v0.2 feature highlights
- Event tags table + rules table + notifications queue.
- Search endpoint and timeline search UI.
- Daily report endpoint (`/api/reports/daily`).
- Snapshot v2 with important events and tags summary.

## Security and privacy notes
- Secrets are never committed.
- Use `.env` for local settings.
- Session artifacts and downloaded media are under `server/data/` (gitignored).
- Outbound calls are limited to Blink account endpoints and optional local Ollama endpoint.

## Quickstart

### macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r server/requirements.txt
cd web && npm ci && cd ..
cp .env.example .env
export BLINKER_USE_MOCK=true
PYTHONPATH=server uvicorn app.main:app --host 127.0.0.1 --port 8090
# second terminal
cd web && npm run dev
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r server\requirements.txt
cd web; npm ci; cd ..
Copy-Item .env.example .env
$env:BLINKER_USE_MOCK='true'
$env:PYTHONPATH='server'
python -m uvicorn app.main:app --host 127.0.0.1 --port 8090
# second terminal
cd web; npm run dev
```

## Optional Ollama setup
1. Install Ollama locally and run it.
2. Pull model: `ollama pull llama3.1`
3. Set:
   - `BLINKER_AI_PROVIDER=ollama`
   - `BLINKER_OLLAMA_URL=http://localhost:11434`
   - `BLINKER_OLLAMA_MODEL=llama3.1`

## Troubleshooting
- **2FA PIN errors:** retry with current PIN in setup page.
- **Rate limits / delayed updates:** increase `BLINKER_POLL_SECONDS`.
- **Empty timeline:** run `POST /api/sync/now` and verify credentials.
- **No vision tags:** ensure thumbnails are downloaded; OpenCV is optional and heuristic mode still works.

## Release zip
```bash
python scripts/make_release_zip.py
```
Creates: `dist/blinker-v0.2-github-ready.zip`
