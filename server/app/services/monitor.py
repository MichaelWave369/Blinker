import asyncio
import logging
from sqlmodel import Session, select
from ..models import Camera, Clip, Event, EventTag
from .media_store import MediaStore
from .rules import RuleEngine

logger = logging.getLogger(__name__)


class MonitorService:
    def __init__(self, blink_client, analyzer, vision_analyzer, engine, poll_seconds: int, auto_download_clips: bool):
        self.blink_client = blink_client
        self.analyzer = analyzer
        self.vision_analyzer = vision_analyzer
        self.engine = engine
        self.poll_seconds = max(10, poll_seconds)
        self.auto_download_clips = auto_download_clips
        self.media_store = MediaStore()
        self.rules = RuleEngine()
        self._stop = asyncio.Event()
        self._task: asyncio.Task | None = None

    async def start(self):
        self._task = asyncio.create_task(self._loop())

    async def stop(self):
        self._stop.set()
        if self._task:
            await self._task

    async def _loop(self):
        while not self._stop.is_set():
            try:
                await self.sync_once()
            except Exception as exc:
                logger.exception('sync loop failed: %s', exc)
            if not self._stop.is_set():
                try:
                    await asyncio.wait_for(self._stop.wait(), timeout=self.poll_seconds)
                except asyncio.TimeoutError:
                    pass

    async def sync_once(self):
        cameras = await self.blink_client.list_cameras()
        events = await self.blink_client.list_events()
        clips = await self.blink_client.list_clips()
        created_events = 0

        with Session(self.engine) as session:
            for cam in cameras:
                session.merge(Camera(id=cam.id, name=cam.name, battery=cam.battery, signal=cam.signal, armed=cam.armed, last_motion=cam.last_motion))

            for clip in clips:
                if session.get(Clip, clip.id):
                    continue
                data = await self.blink_client.download_clip(clip.id) if self.auto_download_clips else None
                file_path = hash_sha = None
                if data:
                    file_path, hash_sha = self.media_store.store_bytes(clip.camera_id, clip.created_at, clip.id, data, 'mp4')
                session.add(Clip(id=clip.id, camera_id=clip.camera_id, event_id=clip.event_id, created_at=clip.created_at,
                                 duration_seconds=clip.duration_seconds, file_path=file_path, hash_sha256=hash_sha, remote_url=clip.remote_url))

            for evt in events:
                if session.get(Event, evt.id):
                    continue
                thumb_data = await self.blink_client.download_thumbnail(evt.id) if evt.thumbnail_url else None
                thumb_path = None
                if thumb_data:
                    thumb_path, _ = self.media_store.store_bytes(evt.camera_id, evt.created_at, evt.id, thumb_data, 'jpg')
                db_evt = Event(id=evt.id, camera_id=evt.camera_id, created_at=evt.created_at, motion=evt.motion, thumbnail_path=thumb_path, clip_id=evt.clip_id)
                summary, tags = await self.analyzer.summarize(db_evt)
                db_evt.summary = summary
                db_evt.tags = ','.join(tags)
                session.add(db_evt)
                session.flush()
                for tag in tags:
                    session.add(EventTag(event_id=db_evt.id, tag=tag, confidence=0.7, source='ai'))

                if thumb_path:
                    vision_result = self.vision_analyzer.analyze_image(thumb_path)
                    for vt in vision_result.get('tags', []):
                        session.add(EventTag(event_id=db_evt.id, tag=vt, confidence=0.5, source='rule'))
                        tags.append(vt)

                self.rules.apply(session, db_evt, tags)
                created_events += 1
            session.commit()
        return {'status': 'synced', 'new_events': created_events}

    def recent_events(self, limit: int = 10):
        with Session(self.engine) as session:
            return session.exec(select(Event).order_by(Event.created_at.desc()).limit(limit)).all()
