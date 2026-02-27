from fastapi import APIRouter, Request
from fastapi.responses import Response
from sqlmodel import Session, select
from ..deps import get_monitor
from ..models import Camera, Event, EventTag
from ..services.snapshot import generate_snapshot_png

router = APIRouter(prefix='/api', tags=['snapshot'])


@router.get('/snapshot.png')
def snapshot_png(request: Request):
    get_monitor(request)
    with Session(request.app.state.db_engine) as session:
        cameras = session.exec(select(Camera)).all()
        events = session.exec(select(Event).order_by(Event.created_at.desc()).limit(10)).all()
        tags = session.exec(select(EventTag)).all()
    lines = [e.summary or f'{e.camera_id} @ {e.created_at.isoformat()}' for e in events]
    tag_counts = {}
    for tag in tags:
        tag_counts[tag.tag] = tag_counts.get(tag.tag, 0) + 1
    png = generate_snapshot_png(
        len(cameras),
        sum(1 for c in cameras if c.armed),
        lines,
        motion_events=len([e for e in events if e.motion]),
        important_events=len([e for e in events if e.important]),
        tags_summary=tag_counts,
    )
    return Response(content=png, media_type='image/png')
