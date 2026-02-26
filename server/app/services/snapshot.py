from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw


def generate_snapshot_png(total_cameras: int, armed_count: int, event_lines: list[str]) -> bytes:
    image = Image.new('RGB', (1100, 700), '#0f172a')
    draw = ImageDraw.Draw(image)
    draw.text((40, 30), f'Blinker Snapshot Report - {datetime.now().isoformat(timespec="seconds")}', fill='white')
    draw.text((40, 80), f'Total cameras: {total_cameras}', fill='#93c5fd')
    draw.text((40, 110), f'Armed cameras: {armed_count}', fill='#93c5fd')
    y = 170
    draw.text((40, y), 'Last 10 events:', fill='white')
    for line in event_lines[:10]:
        y += 40
        draw.text((60, y), f'- {line}', fill='#e2e8f0')
    b = BytesIO()
    image.save(b, format='PNG')
    return b.getvalue()
