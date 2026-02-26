from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
DIST.mkdir(exist_ok=True)
OUT = DIST / 'blinker-v0.2-github-ready.zip'
EXCLUDE_PARTS = {'.git', '.venv', 'node_modules', '__pycache__', '.pytest_cache', 'dist'}

with zipfile.ZipFile(OUT, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for path in ROOT.rglob('*'):
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDE_PARTS for part in rel.parts):
            continue
        if rel.parts[:2] == ('server', 'data'):
            continue
        if path.is_file():
            zf.write(path, rel.as_posix())
print(OUT)
