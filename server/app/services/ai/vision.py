from abc import ABC, abstractmethod
from pathlib import Path
from PIL import Image, ImageStat


class VisionAnalyzer(ABC):
    @abstractmethod
    def analyze_image(self, image_path: str, previous_image_path: str | None = None) -> dict: ...


class HeuristicVisionAnalyzer(VisionAnalyzer):
    def analyze_image(self, image_path: str, previous_image_path: str | None = None) -> dict:
        path = Path(image_path)
        if not path.exists():
            return {'tags': ['unknown'], 'notes': 'image_missing'}
        img = Image.open(path).convert('L')
        brightness = ImageStat.Stat(img).mean[0]
        tags: list[str] = []
        notes: list[str] = []
        if brightness < 70:
            tags.append('low_light')
            notes.append('night_like')
        else:
            tags.append('day_light')
        if previous_image_path and Path(previous_image_path).exists():
            prev = Image.open(previous_image_path).convert('L').resize(img.size)
            diff = ImageStat.Stat(Image.eval(Image.blend(img, prev, 0.5), lambda p: p)).mean[0]
            if diff > 20:
                tags.append('motion_like')
        return {'tags': tags or ['unknown'], 'notes': ','.join(notes) or 'heuristic'}


class OptionalCVVisionAnalyzer(VisionAnalyzer):
    def __init__(self):
        self._cv2 = None
        try:
            import cv2  # type: ignore
            self._cv2 = cv2
        except Exception:
            self._cv2 = None

    def analyze_image(self, image_path: str, previous_image_path: str | None = None) -> dict:
        if self._cv2 is None:
            return HeuristicVisionAnalyzer().analyze_image(image_path, previous_image_path)
        img = self._cv2.imread(image_path)
        if img is None:
            return {'tags': ['unknown'], 'notes': 'cv_read_failed'}
        mean = float(img.mean())
        tags = ['low_light'] if mean < 70 else ['day_light']
        return {'tags': tags, 'notes': 'opencv'}
