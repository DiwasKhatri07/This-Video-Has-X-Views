"""
main.py - 100% Fully Automated YouTube Dynamic Bot (Panel Ready)
- Title: 'This Video Has X Views' (clean, unmentioned)
- Description: Real-time Stats, Top Liked Comment 👑, Latest 3 Comments,
               Community Goals Progress Bars, Bot Uptime, and GitHub Link.
- Comments: Smart personalized reply with ❤️, commenter #, views, and GitHub link.
- 100% Zero Manual Input: Controlled by config.json.
"""

import os
import sys
import time
import json
import signal
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from googleapiclient.errors import HttpError

from auth import get_authenticated_service
from title import (
    get_video_stats,
    get_all_comments_data,
    process_smart_comment_replies,
    format_dynamic_title,
    build_dynamic_description,
    update_video_metadata
)

try:
    from scripts.generate_badges import sync_github_metrics
except Exception:
    sync_github_metrics = None

CONFIG_FILE = "config.json"
LOG_FILE = "automation.log"

# Ensure UTF-8 output across all server panels and terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Setup Rotating Logger
logger = logging.getLogger("YouTubeAutomation")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Console logger
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Rotating File logger (max 5 MB, 3 backups)
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

running = True


def handle_shutdown(signum, frame):
    """Graceful shutdown for server panel/docker."""
    global running
    logger.info("Shutdown signal received. Stopping cleanly...")
    running = False


signal.signal(signal.SIGINT, handle_shutdown)
if hasattr(signal, "SIGTERM"):
    signal.signal(signal.SIGTERM, handle_shutdown)


def load_config():
    """Loads configuration without asking any interactive questions."""
    defaults = {
        "video_id": "dINikoQUm6k",
        "check_interval": 30,
        "github_url": "https://github.com/diwaskhatri07",
        "auto_reply_enabled": True,
        "show_top_comment": True,
        "show_latest_comments": True,
        "show_progress_bars": True,
        "show_uptime_and_milestones": True,
        "max_comments_in_description": 3
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                defaults.update(saved)
        except Exception as e:
            logger.warning("Error reading config.json, using defaults: %s", e)
    else:
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(defaults, f, indent=4)
        except Exception:
            pass

    return defaults


def run_automation():
    """Main loop for server panel and GitHub Actions execution."""
    global running
    start_time = datetime.now()

    # GitHub Actions: Run single cycle and exit
    run_once = os.getenv("RUN_ONCE", "").lower() in ("true", "1", "yes")

    config = load_config()
    video_id = config.get("video_id", "dINikoQUm6k").strip()
    check_interval = int(config.get("check_interval", 30))
    github_url = config.get("github_url", "https://github.com/diwaskhatri07")
    auto_reply = config.get("auto_reply_enabled", True)
    max_comments = int(config.get("max_comments_in_description", 3))

    logger.info("=" * 60)
    logger.info("YOUTUBE ADVANCED BOT STARTED (PANEL MODE)")
    logger.info("Target Video ID : %s", video_id)
    logger.info("Watch URL       : https://www.youtube.com/watch?v=%s", video_id)
    logger.info("Check Interval  : %d seconds", check_interval)
    logger.info("GitHub Link     : %s", github_url)
    logger.info("Auto Reply      : %s", "ENABLED" if auto_reply else "DISABLED")
    logger.info("Features Active : Top Comment, Latest Comments, Goals, Uptime")
    logger.info("=" * 60)

    # Connect to YouTube Data API
    youtube = get_authenticated_service()
    logger.info("Connected to YouTube Data API successfully.")

    last_views = None
    last_likes = None
    last_comment_count = None
    last_latest_comment_ids = None
    cycle = 1

    while running:
        try:
            # 1. Fetch live video statistics
            stats = get_video_stats(youtube, video_id)
            views = stats["view_count"]
            likes = stats["like_count"]
            comments_count = stats["comment_count"]
            current_title = stats["title"]
            snippet = stats["snippet"]

            # 2. Fetch comments (top liked + latest)
            comments_data = get_all_comments_data(youtube, video_id, max_results=max_comments)
            latest_comments = comments_data["latest_comments"]
            top_comment = comments_data["top_comment"]
            current_comment_ids = [c["id"] for c in latest_comments]

            # 3. Format pure title and dynamic interactive description
            expected_title = format_dynamic_title(views)
            expected_desc = build_dynamic_description(
                views=views,
                likes=likes,
                comments_count=comments_count,
                latest_comments=latest_comments,
                top_comment=top_comment,
                github_url=github_url,
                start_time=start_time,
                config=config
            )

            # 4. Check if updates are needed
            # We update if stats changed, new comments arrived, title needs fix, or periodically for uptime
            needs_update = (
                views != last_views
                or likes != last_likes
                or comments_count != last_comment_count
                or current_comment_ids != last_latest_comment_ids
                or current_title != expected_title
                or (cycle % 10 == 0)  # Refresh uptime every 5 minutes (10 cycles * 30s)
            )

            if needs_update:
                logger.info(
                    "[Cycle #%d] 🔄 Updating Metadata -> Views: %d | Likes: %d | Comments: %d",
                    cycle, views, likes, comments_count
                )
                logger.info("Title: '%s'", expected_title)

                success = update_video_metadata(
                    youtube,
                    video_id=video_id,
                    new_title=expected_title,
                    new_description=expected_desc,
                    current_snippet=snippet
                )

                if success:
                    logger.info("[Cycle #%d] ✅ Title and Description updated successfully!", cycle)
                    last_views = views
                    last_likes = likes
                    last_comment_count = comments_count
                    last_latest_comment_ids = current_comment_ids

                    # Sync live metrics to GitHub files (badges, metrics.json, README)
                    if sync_github_metrics:
                        try:
                            sync_github_metrics(views, likes, comments_count, video_id)
                        except Exception as sync_err:
                            logger.warning("Could not sync GitHub metrics: %s", sync_err)
                else:
                    logger.warning("[Cycle #%d] ⚠️ Update did not confirm.", cycle)
            else:
                logger.info(
                    "[Cycle #%d] 🟢 Up-to-date | Views: %d | Likes: %d | Comments: %d | Title: '%s'",
                    cycle, views, likes, comments_count, current_title
                )

                # Ensure initial sync even if stats haven't changed
                if cycle == 1 and sync_github_metrics:
                    try:
                        sync_github_metrics(views, likes, comments_count, video_id)
                    except Exception:
                        pass

            # 5. Smart personalized comment replies (with Heart ❤️ and viewer #)
            if auto_reply:
                process_smart_comment_replies(youtube, video_id, views, comments_count, github_url)

        except HttpError as api_err:
            logger.error("[API ERROR] %s. Sleeping for %ds...", api_err, check_interval)
        except Exception as err:
            logger.error("[ERROR] Unexpected error: %s", err, exc_info=False)

        # GitHub Actions: exit after single cycle
        if run_once:
            logger.info("RUN_ONCE mode: Single cycle completed. Exiting.")
            break

        cycle += 1

        # Sleep with 1-second check for immediate responsive shutdown
        elapsed = 0
        while elapsed < check_interval and running:
            time.sleep(1)
            elapsed += 1

    logger.info("YouTube Automation stopped cleanly. Goodbye!")


if __name__ == "__main__":
    run_automation()
