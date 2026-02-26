from datetime import datetime
import hashlib
from pathlib import Path
from ..core.config import settings


class MediaStore:
    def __init__(self, base: str | None = None):
        self.base = Path(base or settings.blinker_media_dir)
        self.base.mkdir(parents=True, exist_ok=True)

    def _event_path(self, camera_id: str, created_at: datetime, suffix: str) -> Path:
        d = self.base / camera_id / created_at.strftime('%Y/%m/%d')
        d.mkdir(parents=True, exist_ok=True)
        return d / suffix

    def store_bytes(self, camera_id: str, created_at: datetime, stem: str, data: bytes, ext: str) -> tuple[str, str]:
        digest = hashlib.sha256(data).hexdigest()
        path = self._event_path(camera_id, created_at, f'{stem}-{digest[:8]}.{ext}')
        if not path.exists():
            path.write_bytes(data)
        return str(path), digest
