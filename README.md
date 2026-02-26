# Blinker (MVP v0.1)

Blinker is a **local-first** Blink camera monitoring app with optional AI-assisted summaries.

## What Blinker does
- Connects to your Blink account via an unofficial adapter (`blinkpy` implementation scaffold + mock client).
- Syncs cameras, motion events, and clip metadata.
- Stores metadata in local SQLite and media in local folders.
- Builds a timeline and dashboard UI.
- Generates deterministic summaries by default, or optional Ollama summaries.
- Produces a downloadable PNG status snapshot report.

## What Blinker does NOT do
- No guaranteed live local LAN streaming.
- No cloud AI dependency required.
- No telemetry, scraping, or hidden outbound calls.

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

## API endpoints
- `GET /api/health`
- `POST /api/auth/login`
- `POST /api/auth/verify-pin`
- `POST /api/auth/logout`
- `GET /api/cameras`
- `GET /api/events?camera_id=&from=&to=`
- `POST /api/sync/now`
- `GET /api/clips?camera_id=&from=&to=`
- `GET /api/clips/{clip_id}/file`
- `POST /api/analyze/{event_id}`
- `GET /api/snapshot.png`

## Troubleshooting
- **2FA PIN errors:** retry with current PIN in setup page.
- **Rate limits / delayed updates:** increase `BLINKER_POLL_SECONDS`.
- **Empty timeline:** run `POST /api/sync/now` and verify credentials.

## Release zip
```bash
python scripts/make_release_zip.py
```
Creates: `dist/blinker-github-ready.zip`
