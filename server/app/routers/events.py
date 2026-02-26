from datetime import datetime
from fastapi import APIRouter, Query
from sqlmodel import Session, select
from ..db import engine
from ..models import Event

router = APIRouter(prefix='/api', tags=['events'])


@router.get('/events')
def list_events(camera_id: str | None = None, from_: datetime | None = Query(default=None, alias='from'), to: datetime | None = None):
    with Session(engine) as session:
        stmt = select(Event)
        if camera_id:
            stmt = stmt.where(Event.camera_id == camera_id)
        if from_:
            stmt = stmt.where(Event.created_at >= from_)
        if to:
            stmt = stmt.where(Event.created_at <= to)
        return session.exec(stmt.order_by(Event.created_at.desc())).all()
