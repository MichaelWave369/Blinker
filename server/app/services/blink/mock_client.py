from datetime import datetime, timedelta, timezone
from .client import BlinkCamera, BlinkClip, BlinkClient, BlinkEvent, PinRequiredError


class MockBlinkClient(BlinkClient):
    def __init__(self):
        now = datetime.now(timezone.utc).replace(microsecond=0)
        self._logged_in = False
        self._pin_verified = False
        self._cameras = [
            BlinkCamera('cam_driveway', 'Driveway', 91, 4, True, now - timedelta(minutes=5)),
            BlinkCamera('cam_backyard', 'Backyard', 74, 3, False, now - timedelta(minutes=20)),
        ]
        self._events = [
            BlinkEvent('evt_1', 'cam_driveway', now - timedelta(minutes=10), True, 'mock://thumb/evt_1', 'clip_1'),
            BlinkEvent('evt_2', 'cam_backyard', now - timedelta(minutes=30), True, 'mock://thumb/evt_2', 'clip_2'),
        ]
        self._clips = [
            BlinkClip('clip_1', 'cam_driveway', 'evt_1', now - timedelta(minutes=10), 12, 'mock://clip/clip_1'),
            BlinkClip('clip_2', 'cam_backyard', 'evt_2', now - timedelta(minutes=30), 8, 'mock://clip/clip_2'),
        ]

    async def login(self, username: str, password: str, pin: str | None = None) -> dict:
        if pin is None:
            raise PinRequiredError('2FA PIN required')
        if pin != '123456':
            raise ValueError('Invalid PIN')
        self._logged_in = True
        self._pin_verified = True
        return {'status': 'ok', 'token': 'mock-token'}

    async def verify_pin(self, pin: str) -> dict:
        if pin != '123456':
            raise ValueError('Invalid PIN')
        self._pin_verified = True
        self._logged_in = True
        return {'status': 'verified'}

    async def logout(self) -> None:
        self._logged_in = False

    async def list_cameras(self):
        return self._cameras

    async def list_events(self, camera_id: str | None = None):
        return [e for e in self._events if camera_id is None or e.camera_id == camera_id]

    async def list_clips(self, camera_id: str | None = None):
        return [c for c in self._clips if camera_id is None or c.camera_id == camera_id]

    async def take_snapshot(self, camera_id: str):
        return f'snapshot-{camera_id}'.encode()

    async def download_clip(self, clip_id: str):
        return f'clip-bytes-{clip_id}'.encode()

    async def download_thumbnail(self, event_id: str):
        return f'thumb-bytes-{event_id}'.encode()
