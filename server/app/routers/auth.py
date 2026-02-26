from datetime import datetime
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from sqlmodel import Session, select
from ..models import AuthSession
from ..services.blink.client import PinRequiredError

router = APIRouter(prefix='/api/auth', tags=['auth'])


class LoginPayload(BaseModel):
    username: str
    password: str
    pin: str | None = None


class PinPayload(BaseModel):
    pin: str


@router.post('/login')
async def login(payload: LoginPayload, request: Request):
    blink = request.app.state.blink_client
    with Session(request.app.state.db_engine) as session:
        try:
            result = await blink.login(payload.username, payload.password, payload.pin)
        except PinRequiredError as exc:
            raise HTTPException(status_code=401, detail=str(exc))
        except ValueError as exc:
            raise HTTPException(status_code=401, detail=str(exc))
        token = result.get('token', 'session-token')
        session.add(AuthSession(username=payload.username, token=token, created_at=datetime.utcnow()))
        session.commit()
    return {'status': 'ok'}


@router.post('/verify-pin')
async def verify_pin(payload: PinPayload, request: Request):
    try:
        return await request.app.state.blink_client.verify_pin(payload.pin)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc))


@router.post('/logout')
async def logout(request: Request):
    await request.app.state.blink_client.logout()
    with Session(request.app.state.db_engine) as session:
        for row in session.exec(select(AuthSession)).all():
            session.delete(row)
        session.commit()
    return {'status': 'logged_out'}
