import base64
import os

os.environ['BLINKER_USE_MOCK'] = 'true'
os.environ['BLINKER_DB_PATH'] = 'server/data/test-blinker.db'

from fastapi.testclient import TestClient
from app.main import create_app
from app.services.ai.vision import HeuristicVisionAnalyzer


def _write_fixture(path: str, b64_data: str) -> None:
    with open(path, 'wb') as f:
        f.write(base64.b64decode(b64_data))


def test_heuristic_vision_tags_are_deterministic(tmp_path):
    analyzer = HeuristicVisionAnalyzer()
    dark_path = tmp_path / 'dark.png'
    bright_path = tmp_path / 'bright.png'

    # 1x1 black / white PNG fixtures generated at runtime to avoid committed binaries.
    dark = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jk3sAAAAASUVORK5CYII='
    bright = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8z8AABQMBgLQ6n2sAAAAASUVORK5CYII='
    _write_fixture(str(dark_path), dark)
    _write_fixture(str(bright_path), bright)

    dark_result = analyzer.analyze_image(str(dark_path))
    bright_result = analyzer.analyze_image(str(bright_path))
    assert 'low_light' in dark_result['tags']
    assert 'day_light' in bright_result['tags']


def test_rule_application_creates_notification():
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

        client.post('/api/sync/now')
        notifications = client.get('/api/notifications')
        assert notifications.status_code == 200
        assert len(notifications.json()) >= 1
