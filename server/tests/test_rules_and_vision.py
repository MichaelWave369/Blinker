import os
import uuid
from datetime import datetime, timezone
import pytest

os.environ['BLINKER_USE_MOCK'] = 'true'
pytest.importorskip('fastapi')

from fastapi.testclient import TestClient
from app.main import create_app
from app.services.ai.vision import HeuristicVisionAnalyzer
from PIL import Image
from app.services.blink.client import BlinkEvent


def _fresh_db_path() -> str:
    return f'server/data/test-blinker-{uuid.uuid4().hex}.db'


def test_heuristic_vision_tags_are_deterministic(tmp_path):
    analyzer = HeuristicVisionAnalyzer()
    dark_path = tmp_path / 'dark.png'
    bright_path = tmp_path / 'bright.png'

    Image.new('RGB', (10, 10), (10, 10, 10)).save(dark_path)
    Image.new('RGB', (10, 10), (240, 240, 240)).save(bright_path)

    dark_result = analyzer.analyze_image(str(dark_path))
    bright_result = analyzer.analyze_image(str(bright_path))
    assert 'low_light' in dark_result['tags']
    assert 'day_light' in bright_result['tags']


def test_rule_application_creates_notification():
    os.environ['BLINKER_DB_PATH'] = _fresh_db_path()
    with TestClient(create_app()) as client:
        rule_payload = {
            'name': 'Night motion important',
            'enabled': True,
            'camera_id_optional': 'cam_driveway',
            'conditions': {'camera_match': 'cam_driveway'},
            'actions': {'mark_important': True, 'create_notification': True, 'add_tags': ['important']},
        }
        create = client.post('/api/rules', json=rule_payload)
        assert create.status_code == 200

        client.app.state.blink_client._events.append(
            BlinkEvent('evt_rule_test', 'cam_driveway', datetime.now(timezone.utc), True, 'mock://thumb/evt_rule_test', None)
        )
        client.post('/api/sync/now')
        notifications = client.get('/api/notifications')
        assert notifications.status_code == 200
        assert len(notifications.json()) >= 1
