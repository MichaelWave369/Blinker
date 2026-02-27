from fastapi import APIRouter, Request
from sqlmodel import Session, select
from ..models import Camera

router = APIRouter(prefix='/api', tags=['cameras'])


@router.get('/cameras')
def list_cameras(request: Request):
    with Session(request.app.state.db_engine) as session:
        return session.exec(select(Camera)).all()
