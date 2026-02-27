from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw


def generate_snapshot_png(total_cameras: int, armed_count: int, event_lines: list[str], motion_events: int | None = None,
                          important_events: int | None = None, tags_summary: dict[str, int] | None = None) -> bytes:
    image = Image.new('RGB', (1200, 760), '#0f172a')
    draw = ImageDraw.Draw(image)
    draw.text((40, 30), f'Blinker Snapshot Report - {datetime.now().isoformat(timespec="seconds")}', fill='white')
    draw.text((40, 80), f'Total cameras: {total_cameras}', fill='#93c5fd')
    draw.text((40, 110), f'Armed cameras: {armed_count}', fill='#93c5fd')
    if motion_events is not None:
        draw.text((40, 140), f'Motion events: {motion_events}', fill='#93c5fd')
    if important_events is not None:
        draw.text((40, 170), f'Important events: {important_events}', fill='#93c5fd')
    if tags_summary:
        draw.text((700, 80), 'Tags summary:', fill='white')
        y2 = 110
        for tag, cnt in sorted(tags_summary.items(), key=lambda kv: kv[1], reverse=True)[:8]:
            draw.text((700, y2), f'{tag}: {cnt}', fill='#a7f3d0')
            y2 += 28
    y = 230
    draw.text((40, y), 'Last 10 events:', fill='white')
    for line in event_lines[:10]:
        y += 40
        draw.text((60, y), f'- {line[:130]}', fill='#e2e8f0')
    b = BytesIO()
    image.save(b, format='PNG')
    return b.getvalue()
