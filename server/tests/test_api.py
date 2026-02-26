import pytest
import os

os.environ['BLINKER_USE_MOCK'] = 'true'
os.environ['BLINKER_DB_PATH'] = 'server/data/test-blinker.db'

pytest.importorskip('fastapi')
from fastapi.testclient import TestClient
from app.main import create_app


def test_health():
    with TestClient(create_app()) as client:
        resp = client.get('/api/health')
        assert resp.status_code == 200
        assert resp.json()['status'] == 'ok'


def test_list_cameras_after_sync():
    with TestClient(create_app()) as client:
        client.post('/api/sync/now')
        resp = client.get('/api/cameras')
        assert resp.status_code == 200
        cams = resp.json()
        assert len(cams) >= 2


def test_sync_stores_events_and_search():
    with TestClient(create_app()) as client:
        resp = client.post('/api/sync/now')
        assert resp.status_code == 200
        ev = client.get('/api/events')
        assert ev.status_code == 200
        assert len(ev.json()) >= 2
        srch = client.get('/api/events/search?q=driveway')
        assert srch.status_code == 200
        assert len(srch.json()) >= 1


def test_snapshot_png_and_daily_report():
    with TestClient(create_app()) as client:
        client.post('/api/sync/now')
        resp = client.get('/api/snapshot.png')
        assert resp.status_code == 200
        assert resp.headers['content-type'] == 'image/png'
        assert resp.content[:8] == b'\x89PNG\r\n\x1a\n'

        daily = client.get('/api/reports/daily')
        assert daily.status_code == 200
        assert 'motion_events' in daily.json()
