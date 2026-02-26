from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.logging import configure_logging
from .db import init_db
from .routers import health, auth, cameras, events, clips, sync, analyze, snapshot
from .services.ai.noop_analyzer import NoopAnalyzer
from .services.ai.ollama_analyzer import OllamaAnalyzer
from .services.blink.blinkpy_client import BlinkPyClient
from .services.blink.mock_client import MockBlinkClient
from .services.monitor import MonitorService


def build_analyzer():
    if settings.blinker_ai_provider.lower() == 'ollama':
        return OllamaAnalyzer()
    return NoopAnalyzer()


def build_blink_client():
    if settings.blinker_use_mock:
        return MockBlinkClient()
    return BlinkPyClient()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    init_db()
    app.state.blink_client = build_blink_client()
    app.state.analyzer = build_analyzer()
    app.state.monitor = MonitorService(
        app.state.blink_client,
        app.state.analyzer,
        settings.blinker_poll_seconds,
        settings.blinker_auto_download_clips,
    )
    await app.state.monitor.start()
    yield
    await app.state.monitor.stop()


app = FastAPI(title='Blinker', lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(cameras.router)
app.include_router(events.router)
app.include_router(clips.router)
app.include_router(sync.router)
app.include_router(analyze.router)
app.include_router(snapshot.router)
