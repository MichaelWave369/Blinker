from fastapi import APIRouter, HTTPException, Request
from sqlmodel import Session
from ..models import Camera, Event, EventTag

router = APIRouter(prefix='/api', tags=['analyze'])


@router.post('/analyze/{event_id}')
async def analyze_event(event_id: str, request: Request):
    with Session(request.app.state.db_engine) as session:
        event = session.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail='event not found')
        cam = session.get(Camera, event.camera_id)
        summary, tags = await request.app.state.analyzer.summarize(event, cam.name if cam else None)
        event.summary = summary
        event.tags = ','.join(tags)
        session.add(event)
        for tag in tags:
            session.add(EventTag(event_id=event.id, tag=tag, confidence=0.7, source='ai'))
        session.commit()
        session.refresh(event)
        return event
