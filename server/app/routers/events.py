from datetime import datetime
from fastapi import APIRouter, Query, Request
from sqlmodel import Session, select
from ..models import Camera, Event, EventTag

router = APIRouter(prefix='/api', tags=['events'])


@router.get('/events')
def list_events(request: Request, camera_id: str | None = None, from_: datetime | None = Query(default=None, alias='from'), to: datetime | None = None):
    with Session(request.app.state.db_engine) as session:
        stmt = select(Event)
        if camera_id:
            stmt = stmt.where(Event.camera_id == camera_id)
        if from_:
            stmt = stmt.where(Event.created_at >= from_)
        if to:
            stmt = stmt.where(Event.created_at <= to)
        return session.exec(stmt.order_by(Event.created_at.desc())).all()


@router.get('/events/search')
def search_events(request: Request, q: str | None = None, tag: str | None = None, camera_id: str | None = None,
                  from_: datetime | None = Query(default=None, alias='from'), to: datetime | None = None):
    with Session(request.app.state.db_engine) as session:
        events = session.exec(select(Event).order_by(Event.created_at.desc())).all()
        cameras = {c.id: c.name for c in session.exec(select(Camera)).all()}
        tag_map: dict[str, list[str]] = {}
        for t in session.exec(select(EventTag)).all():
            tag_map.setdefault(t.event_id, []).append(t.tag)
    results = []
    for event in events:
        if camera_id and event.camera_id != camera_id:
            continue
        if from_ and event.created_at < from_:
            continue
        if to and event.created_at > to:
            continue
        tags = tag_map.get(event.id, [])
        hay = f"{cameras.get(event.camera_id, event.camera_id)} {event.summary or ''} {' '.join(tags)}".lower()
        if q and q.lower() not in hay:
            continue
        if tag and tag not in tags and (not event.tags or tag not in event.tags):
            continue
        results.append({'event': event, 'camera_name': cameras.get(event.camera_id, event.camera_id), 'tags': tags})
    return results
