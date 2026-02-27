from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import Settings
from .core.logging import configure_logging
from .deps import build_monitor_from_settings
from .routers import analyze, auth, cameras, clips, events, health, notifications, reports, rules, snapshot, sync


def create_app() -> FastAPI:
    settings = Settings()
    monitor, engine = build_monitor_from_settings(settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        configure_logging()
        await app.state.monitor.start()
        yield
        await app.state.monitor.stop()

    app = FastAPI(title='Blinker', version=settings.blinker_version, lifespan=lifespan)
    app.state.settings = settings
    app.state.db_engine = engine
    app.state.blink_client = monitor.blink_client
    app.state.analyzer = monitor.analyzer
    app.state.vision_analyzer = monitor.vision_analyzer
    app.state.monitor = monitor

    app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(cameras.router)
    app.include_router(events.router)
    app.include_router(clips.router)
    app.include_router(sync.router)
    app.include_router(analyze.router)
    app.include_router(snapshot.router)
    app.include_router(rules.router)
    app.include_router(notifications.router)
    app.include_router(reports.router)
    return app


app = create_app()
