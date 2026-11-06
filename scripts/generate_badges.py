"""
generate_badges.py - Updates SVG badges, metrics.json, and README.md with live YouTube stats.
"""

import os
import json
import re
from datetime import datetime


def create_svg_badge(label, value, color, filename):
    label_w = len(label) * 7 + 12
    val_w = len(str(value)) * 7 + 14
    total_w = label_w + val_w

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="20" role="img" aria-label="{label}: {value}">
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r">
    <rect width="{total_w}" height="20" rx="3" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#r)">
    <rect width="{label_w}" height="20" fill="#555"/>
    <rect x="{label_w}" width="{val_w}" height="20" fill="{color}"/>
    <rect width="{total_w}" height="20" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="11">
    <text x="{label_w / 2}" y="15" fill="#010101" fill-opacity=".3">{label}</text>
    <text x="{label_w / 2}" y="14">{label}</text>
    <text x="{label_w + val_w / 2}" y="15" fill="#010101" fill-opacity=".3">{value}</text>
    <text x="{label_w + val_w / 2}" y="14">{value}</text>
  </g>
</svg>'''

    os.makedirs("badges", exist_ok=True)
    with open(os.path.join("badges", filename), "w", encoding="utf-8") as f:
        f.write(svg.strip())


def sync_github_metrics(views: int, likes: int, comments: int, video_id: str = "dINikoQUm6k"):
    """
    Synchronizes:
    1. metrics.json
    2. SVG badges in badges/
    3. README.md live table block
    """
    now_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    metrics_path = "metrics.json"
    previous_metrics = {}
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, "r", encoding="utf-8") as f:
                loaded_metrics = json.load(f)
                if isinstance(loaded_metrics, dict):
                    previous_metrics = loaded_metrics
        except (OSError, json.JSONDecodeError):
            previous_metrics = {}

    values = {
        "video_id": video_id,
        "views": views,
        "likes": likes,
        "comments": comments,
        "title": f"This Video Has {views} Views",
    }
    values_changed = any(previous_metrics.get(key) != value for key, value in values.items())
    last_updated = now_utc if values_changed else previous_metrics.get("last_updated", now_utc)
    metrics = {**values, "last_updated": last_updated}

    # 1. Update metrics.json; preserve its timestamp while values are unchanged.
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # 2. Update SVG badges
    create_svg_badge("views", f"{views:,}", "#e05d44", "views.svg")
    create_svg_badge("likes", f"{likes:,}", "#44cc11", "likes.svg")
    create_svg_badge("comments", f"{comments:,}", "#007ec6", "comments.svg")
    create_svg_badge("bot", "online", "#2ecc71", "status.svg")

    # 3. Update README.md live table if markers exist
    readme_path = "README.md"
    if os.path.exists(readme_path):
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()

            table_replacement = f"""<!-- LIVE_METRICS_START -->
| Metric | Real-time Value | Status |
| :--- | :--- | :--- |
| **YouTube Views** | **`{views:,}`** | Synchronized |
| **Video Likes** | **`{likes:,}`** | Active |
| **Total Comments** | **`{comments:,}`** | Live |
| **Current Title** | **`This Video Has {views} Views`** | Active |
| **Last Data Change** | `{last_updated}` | Checked every 5 min |
<!-- LIVE_METRICS_END -->"""

            pattern = r"<!-- LIVE_METRICS_START -->.*?<!-- LIVE_METRICS_END -->"
            if re.search(pattern, content, flags=re.DOTALL):
                new_content = re.sub(pattern, table_replacement, content, flags=re.DOTALL)
                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
        except Exception as e:
            print(f"[METRICS] Could not update README table: {e}")
