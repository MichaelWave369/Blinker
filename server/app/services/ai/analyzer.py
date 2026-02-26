from abc import ABC, abstractmethod
from ...models import Event


class Analyzer(ABC):
    @abstractmethod
    async def summarize(self, event: Event, camera_name: str | None = None) -> tuple[str, list[str]]: ...
