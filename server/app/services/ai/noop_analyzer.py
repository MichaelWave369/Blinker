from datetime import timezone
from .analyzer import Analyzer
from ...models import Event


class NoopAnalyzer(Analyzer):
    async def summarize(self, event: Event, camera_name: str | None = None) -> tuple[str, list[str]]:
        tz = event.created_at.astimezone(timezone.utc)
        cam = camera_name or event.camera_id
        clip_text = 'with clip' if event.clip_id else 'no clip'
        return (f'{cam} at {tz.strftime("%I:%M %p UTC")} — motion detected, {clip_text}', ['motion'])
