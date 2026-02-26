from fastapi import APIRouter, Request

router = APIRouter(prefix='/api/sync', tags=['sync'])


@router.post('/now')
async def sync_now(request: Request):
    await request.app.state.monitor.sync_once()
    return {'status': 'synced'}
