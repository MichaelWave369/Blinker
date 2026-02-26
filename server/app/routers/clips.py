from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from ..db import engine
from ..models import Clip

router = APIRouter(prefix='/api', tags=['clips'])


@router.get('/clips')
def list_clips(camera_id: str | None = None, from_: datetime | None = Query(default=None, alias='from'), to: datetime | None = None):
    with Session(engine) as session:
        stmt = select(Clip)
        if camera_id:
            stmt = stmt.where(Clip.camera_id == camera_id)
        if from_:
            stmt = stmt.where(Clip.created_at >= from_)
        if to:
            stmt = stmt.where(Clip.created_at <= to)
        return session.exec(stmt.order_by(Clip.created_at.desc())).all()


@router.get('/clips/{clip_id}/file')
def download_clip_file(clip_id: str):
    with Session(engine) as session:
        clip = session.get(Clip, clip_id)
        if not clip or not clip.file_path:
            raise HTTPException(status_code=404, detail='clip file not found')
        return FileResponse(clip.file_path, filename=f'{clip_id}.mp4')
