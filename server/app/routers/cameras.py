from fastapi import APIRouter
from sqlmodel import Session, select
from ..db import engine
from ..models import Camera

router = APIRouter(prefix='/api', tags=['cameras'])


@router.get('/cameras')
def list_cameras():
    with Session(engine) as session:
        return session.exec(select(Camera)).all()
