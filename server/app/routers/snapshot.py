from fastapi import APIRouter
from fastapi.responses import Response
from sqlmodel import Session, select
from ..db import engine
from ..models import Camera, Event
from ..services.snapshot import generate_snapshot_png

router = APIRouter(prefix='/api', tags=['snapshot'])


@router.get('/snapshot.png')
def snapshot_png():
    with Session(engine) as session:
        cameras = session.exec(select(Camera)).all()
        events = session.exec(select(Event).order_by(Event.created_at.desc()).limit(10)).all()
    lines = [e.summary or f'{e.camera_id} @ {e.created_at.isoformat()}' for e in events]
    png = generate_snapshot_png(len(cameras), sum(1 for c in cameras if c.armed), lines)
    return Response(content=png, media_type='image/png')
