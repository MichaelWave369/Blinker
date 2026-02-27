from fastapi import Request
from .core.config import Settings
from .db import build_engine, init_db
from .services.ai.noop_analyzer import NoopAnalyzer
from .services.ai.ollama_analyzer import OllamaAnalyzer
from .services.ai.vision import HeuristicVisionAnalyzer, OptionalCVVisionAnalyzer
from .services.blink.blinkpy_client import BlinkPyClient
from .services.blink.mock_client import MockBlinkClient
from .services.monitor import MonitorService


def build_blink_client(settings: Settings):
    return MockBlinkClient() if settings.blinker_use_mock else BlinkPyClient()


def build_analyzer(settings: Settings):
    if settings.blinker_ai_provider.lower() == 'ollama':
        return OllamaAnalyzer()
    return NoopAnalyzer()


def build_vision_analyzer():
    cv = OptionalCVVisionAnalyzer()
    if cv._cv2 is None:
        return HeuristicVisionAnalyzer()
    return cv


def build_monitor_from_settings(settings: Settings):
    engine = build_engine(settings.db_url)
    init_db(engine)
    return MonitorService(
        blink_client=build_blink_client(settings),
        analyzer=build_analyzer(settings),
        vision_analyzer=build_vision_analyzer(),
        engine=engine,
        poll_seconds=settings.blinker_poll_seconds,
        auto_download_clips=settings.blinker_auto_download_clips,
    ), engine


def get_monitor(request: Request) -> MonitorService:
    if not hasattr(request.app.state, 'monitor'):
        settings = getattr(request.app.state, 'settings', Settings())
        monitor, engine = build_monitor_from_settings(settings)
        request.app.state.settings = settings
        request.app.state.monitor = monitor
        request.app.state.db_engine = engine
        request.app.state.blink_client = monitor.blink_client
        request.app.state.analyzer = monitor.analyzer
        request.app.state.vision_analyzer = monitor.vision_analyzer
    return request.app.state.monitor
