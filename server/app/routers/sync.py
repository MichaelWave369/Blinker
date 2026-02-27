from fastapi import APIRouter, Request
from ..deps import get_monitor

router = APIRouter(prefix='/api/sync', tags=['sync'])


@router.post('/now')
async def sync_now(request: Request):
    monitor = get_monitor(request)
    return await monitor.sync_once()
