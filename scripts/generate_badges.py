"""
scripts/generate_badges.py — Fetches live YouTube stats and writes JSON + SVG badges.
Used by GitHub Actions to keep README badges dynamically updated.
"""

import os
import sys
import json

# Add parent dir to path so we can import auth
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import get_authenticated_service


def fetch_stats(video_id):
    youtube = get_authenticated_service()
    response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()

    items = response.get("items", [])
    if not items:
        raise ValueError(f"No video found: {video_id}")

    stats = items[0]["statistics"]
    snippet = items[0]["snippet"]
    return {
        "title": snippet.get("title", ""),
        "views": int(stats.get("viewCount", 0)),
        "likes": int(stats.get("likeCount", 0)),
        "comments": int(stats.get("commentCount", 0)),
    }


def create_badge_svg(label, value, color, filename):
    """Creates a simple shields.io compatible SVG badge."""
    label_width = len(label) * 7 + 10
    value_width = len(str(value)) * 7 + 10
    total_width = label_width + value_width

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="20" role="img">
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r"><rect width="{total_width}" height="20" rx="3" fill="#fff"/></clipPath>
  <g clip-path="url(#r)">
    <rect width="{label_width}" height="20" fill="#555"/>
    <rect x="{label_width}" width="{value_width}" height="20" fill="{color}"/>
    <rect width="{total_width}" height="20" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="11">
    <text x="{label_width/2}" y="14">{label}</text>
    <text x="{label_width + value_width/2}" y="14">{value}</text>
  </g>
</svg>'''

    os.makedirs("badges", exist_ok=True)
    with open(f"badges/{filename}", "w", encoding="utf-8") as f:
        f.write(svg)


def main():
    # Load config
    config_path = "config.json"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
    else:
        config = {"video_id": "dINikoQUm6k"}

    video_id = config.get("video_id", "dINikoQUm6k")
    stats = fetch_stats(video_id)

    print(f"Fetched Stats — Views: {stats['views']}, Likes: {stats['likes']}, Comments: {stats['comments']}")

    # Save metrics.json
    with open("metrics.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    # Generate SVG badges
    create_badge_svg("views", f"{stats['views']:,}", "#e05d44", "views.svg")
    create_badge_svg("likes", f"{stats['likes']:,}", "#44cc11", "likes.svg")
    create_badge_svg("comments", f"{stats['comments']:,}", "#007ec6", "comments.svg")
    create_badge_svg("bot", "online", "#2ecc71", "status.svg")

    print("Badges generated successfully!")


if __name__ == "__main__":
    main()
