from fastapi import APIRouter, HTTPException, Request
from sqlmodel import Session
from ..db import engine
from ..models import Camera, Event

router = APIRouter(prefix='/api', tags=['analyze'])


@router.post('/analyze/{event_id}')
async def analyze_event(event_id: str, request: Request):
    with Session(engine) as session:
        event = session.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail='event not found')
        cam = session.get(Camera, event.camera_id)
        summary, tags = await request.app.state.analyzer.summarize(event, cam.name if cam else None)
        event.summary = summary
        event.tags = ','.join(tags)
        session.add(event)
        session.commit()
        session.refresh(event)
        return event
