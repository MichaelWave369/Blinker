from fastapi import APIRouter, Request
from pydantic import BaseModel
from ..services.assistant import AssistantService

router = APIRouter(prefix='/api/assistant', tags=['assistant'])


class ChatPayload(BaseModel):
    content: str


@router.get('/feed')
def feed(request: Request, limit: int = 20):
    svc = AssistantService(request.app.state.db_engine)
    return svc.list_messages(limit=limit)


@router.get('/messages')
def list_messages(request: Request, limit: int = 100):
    svc = AssistantService(request.app.state.db_engine)
    return svc.list_messages(limit=limit)


@router.post('/messages')
def post_message(payload: ChatPayload, request: Request):
    svc = AssistantService(request.app.state.db_engine)
    return svc.post_user_message(payload.content)
