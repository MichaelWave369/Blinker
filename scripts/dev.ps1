python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r server\requirements.txt
Push-Location web
npm ci
Pop-Location
$env:BLINKER_USE_MOCK='true'
Start-Process python -ArgumentList '-m uvicorn server.app.main:app --reload --host 127.0.0.1 --port 8090'
Push-Location web
npm run dev
Pop-Location
