from datetime import date, datetime, timedelta
from fastapi import APIRouter, Query, Request
from sqlmodel import Session, select
from ..models import Camera, Event, EventTag
from ..services.snapshot import generate_snapshot_png

router = APIRouter(prefix='/api/reports', tags=['reports'])


@router.get('/daily')
def daily_report(request: Request, date_value: date | None = Query(default=None, alias='date'), format: str = 'json'):
    target = date_value or datetime.utcnow().date()
    start = datetime.combine(target, datetime.min.time())
    end = start + timedelta(days=1)
    with Session(request.app.state.db_engine) as session:
        events = session.exec(select(Event).where(Event.created_at >= start).where(Event.created_at < end)).all()
        cameras = session.exec(select(Camera)).all()
        tags = session.exec(select(EventTag)).all()
    tag_counts: dict[str, int] = {}
    for tag in tags:
        tag_counts[tag.tag] = tag_counts.get(tag.tag, 0) + 1
    top_cameras: dict[str, int] = {}
    for event in events:
        top_cameras[event.camera_id] = top_cameras.get(event.camera_id, 0) + 1
    report = {
        'date': str(target),
        'total_cameras': len(cameras),
        'motion_events': len([e for e in events if e.motion]),
        'important_events': len([e for e in events if e.important]),
        'top_cameras': sorted(top_cameras.items(), key=lambda kv: kv[1], reverse=True)[:3],
        'tags_summary': tag_counts,
    }
    if format == 'png':
        lines = [f"{e.camera_id} {e.summary or ''}" for e in events[:10]]
        png = generate_snapshot_png(report['total_cameras'], len([c for c in cameras if c.armed]), lines)
        from fastapi.responses import Response
        return Response(content=png, media_type='image/png')
    return report
