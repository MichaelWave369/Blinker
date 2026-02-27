from fastapi import APIRouter, Request
from sqlmodel import Session, select
from ..models import Notification

router = APIRouter(prefix='/api', tags=['notifications'])


@router.get('/notifications')
def list_notifications(request: Request):
    with Session(request.app.state.db_engine) as session:
        return session.exec(select(Notification).order_by(Notification.created_at.desc())).all()
