from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BlinkCamera:
    id: str
    name: str
    battery: Optional[int]
    signal: Optional[int]
    armed: bool
    last_motion: Optional[datetime]


@dataclass
class BlinkEvent:
    id: str
    camera_id: str
    created_at: datetime
    motion: bool
    thumbnail_url: Optional[str]
    clip_id: Optional[str]


@dataclass
class BlinkClip:
    id: str
    camera_id: str
    event_id: Optional[str]
    created_at: datetime
    duration_seconds: Optional[int]
    remote_url: Optional[str]


class PinRequiredError(Exception):
    pass


class BlinkClient(ABC):
    @abstractmethod
    async def login(self, username: str, password: str, pin: str | None = None) -> dict: ...

    @abstractmethod
    async def verify_pin(self, pin: str) -> dict: ...

    @abstractmethod
    async def logout(self) -> None: ...

    @abstractmethod
    async def list_cameras(self) -> list[BlinkCamera]: ...

    @abstractmethod
    async def list_events(self, camera_id: str | None = None) -> list[BlinkEvent]: ...

    @abstractmethod
    async def list_clips(self, camera_id: str | None = None) -> list[BlinkClip]: ...

    @abstractmethod
    async def take_snapshot(self, camera_id: str) -> bytes | None: ...

    @abstractmethod
    async def download_clip(self, clip_id: str) -> bytes | None: ...

    @abstractmethod
    async def download_thumbnail(self, event_id: str) -> bytes | None: ...
