from fastapi import APIRouter, Request

router = APIRouter(prefix='/api', tags=['health'])


@router.get('/health')
def health(request: Request):
    return {'status': 'ok', 'version': request.app.version}
