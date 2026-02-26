from .client import BlinkClient


class BlinkPyClient(BlinkClient):
    def __init__(self):
        self._client = None

    async def login(self, username: str, password: str, pin: str | None = None) -> dict:
        raise NotImplementedError('blinkpy integration scaffolded; use mock mode for tests/dev')

    async def verify_pin(self, pin: str) -> dict:
        raise NotImplementedError

    async def logout(self) -> None:
        return None

    async def list_cameras(self):
        return []

    async def list_events(self, camera_id: str | None = None):
        return []

    async def list_clips(self, camera_id: str | None = None):
        return []

    async def take_snapshot(self, camera_id: str):
        return None

    async def download_clip(self, clip_id: str):
        return None

    async def download_thumbnail(self, event_id: str):
        return None
