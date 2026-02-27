import httpx
from .analyzer import Analyzer
from ...core.config import settings
from ...models import Event


class OllamaAnalyzer(Analyzer):
    async def summarize(self, event: Event, camera_name: str | None = None) -> tuple[str, list[str]]:
        cam = camera_name or event.camera_id
        prompt = f'Summarize this Blink event in one sentence: camera={cam}, timestamp={event.created_at.isoformat()}, motion={event.motion}, clip={event.clip_id}'
        payload = {'model': settings.blinker_ollama_model, 'prompt': prompt, 'stream': False}
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(f'{settings.blinker_ollama_url}/api/generate', json=payload)
            resp.raise_for_status()
            text = resp.json().get('response', '').strip()
        tags = ['motion']
        lower = text.lower()
        for label in ('person', 'vehicle', 'animal'):
            if label in lower:
                tags.append(label)
        return text or f'{cam} motion event', tags
