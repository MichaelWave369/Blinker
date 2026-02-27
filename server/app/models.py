from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Camera(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    battery: Optional[int] = None
    signal: Optional[int] = None
    armed: bool = False
    last_motion: Optional[datetime] = None


class Clip(SQLModel, table=True):
    id: str = Field(primary_key=True)
    camera_id: str = Field(index=True)
    event_id: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(index=True)
    duration_seconds: Optional[int] = None
    file_path: Optional[str] = None
    hash_sha256: Optional[str] = None
    remote_url: Optional[str] = None


class Event(SQLModel, table=True):
    id: str = Field(primary_key=True)
    camera_id: str = Field(index=True)
    created_at: datetime = Field(index=True)
    motion: bool = True
    thumbnail_path: Optional[str] = None
    clip_id: Optional[str] = Field(default=None, index=True)
    summary: Optional[str] = None
    tags: Optional[str] = None
    important: bool = False


class EventTag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    event_id: str = Field(index=True)
    tag: str = Field(index=True)
    confidence: float = 0.0
    source: str = 'ai'


class Rule(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    enabled: bool = True
    camera_id_optional: Optional[str] = Field(default=None, index=True)
    conditions_json: str
    actions_json: str


class Notification(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    title: str
    body: str
    delivered_at: Optional[datetime] = None
    channel: str = 'web'


class AuthSession(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    token: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AssistantMessage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    role: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    source: str = 'chat'
