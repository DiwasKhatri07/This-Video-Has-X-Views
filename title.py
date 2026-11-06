"""
title.py - Advanced YouTube Title, Description & Interactive Community Engine
Features:
1. Pure Title: 'This Video Has X Views'
2. 👑 Top Liked Comment Hall of Fame
3. 💬 Latest 3 Comments
4. 📊 Live ASCII Progress Bars (Likes & Comments goals)
5. 🎯 Smart Personalized Auto-Replies (Commenter #, Views at time, Heart ❤️, GitHub link)
6. ⏳ Bot Live Uptime & Milestone Checklist
"""

import os
import sys
import json
import logging
from datetime import datetime
from googleapiclient.errors import HttpError

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

logger = logging.getLogger("YouTubeAutomation")
REPLIED_COMMENTS_FILE = "replied_comments.json"


def load_replied_comments():
    """Loads comment IDs that have already received an auto-reply."""
    if os.path.exists(REPLIED_COMMENTS_FILE):
        try:
            with open(REPLIED_COMMENTS_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception as e:
            logger.warning("Could not load '%s': %s", REPLIED_COMMENTS_FILE, e)
    return set()


def save_replied_comments(replied_set):
    """Saves set of replied comment IDs."""
    try:
        with open(REPLIED_COMMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(list(replied_set), f, indent=2)
    except Exception as e:
        logger.error("Could not save '%s': %s", REPLIED_COMMENTS_FILE, e)


def get_video_stats(youtube, video_id: str):
    """Retrieves real-time statistics and snippet for target video."""
    try:
        response = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        ).execute()

        items = response.get("items", [])
        if not items:
            raise ValueError(f"No video found with ID: '{video_id}'")

        video_item = items[0]
        snippet = video_item.get("snippet", {})
        statistics = video_item.get("statistics", {})

        return {
            "view_count": int(statistics.get("viewCount", 0)),
            "like_count": int(statistics.get("likeCount", 0)),
            "comment_count": int(statistics.get("commentCount", 0)),
            "title": snippet.get("title", ""),
            "description": snippet.get("description", ""),
            "snippet": snippet
        }
    except HttpError as e:
        raise RuntimeError(f"YouTube API Error fetching stats: {e}") from e


def get_all_comments_data(youtube, video_id: str, max_results: int = 3):
    """
    Fetches comments to extract:
    1. Latest comments (up to max_results)
    2. Top liked comment
    3. List of comment dicts for processing
    """
    comments_list = []
    top_comment = None

    try:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=30,
            order="time",
            textFormat="plainText"
        ).execute()

        for item in response.get("items", []):
            top_obj = item.get("snippet", {}).get("topLevelComment", {})
            comment_id = top_obj.get("id", "")
            s = top_obj.get("snippet", {})
            author = s.get("authorDisplayName", "Anonymous")
            text = s.get("textDisplay", "").strip().replace("\n", " ")
            likes = int(s.get("likeCount", 0))

            if len(text) > 75:
                text = text[:72] + "..."

            data = {
                "id": comment_id,
                "author": author,
                "text": text,
                "likes": likes,
                "published_at": s.get("publishedAt", "")
            }
            comments_list.append(data)

        # Find top liked comment (if any has > 0 likes)
        liked_comments = [c for c in comments_list if c["likes"] > 0]
        if liked_comments:
            top_comment = max(liked_comments, key=lambda c: c["likes"])

    except HttpError as e:
        logger.warning("Could not fetch comments (might be disabled): %s", e)

    latest_comments = comments_list[:max_results]
    return {
        "latest_comments": latest_comments,
        "top_comment": top_comment,
        "raw_comments": comments_list
    }


def format_dynamic_title(views: int) -> str:
    """Pure title format: 'This Video Has X Views'"""
    return f"This Video Has {views} Views"


def make_progress_bar(current: int, targets=(5, 10, 25, 50, 100, 250, 500, 1000, 5000, 10000), bar_len=10) -> str:
    """Calculates next goal and renders an ASCII progress bar."""
    next_goal = targets[-1]
    for target in targets:
        if current < target:
            next_goal = target
            break

    percent = min(100, int((current / next_goal) * 100)) if next_goal > 0 else 100
    filled = int((percent / 100) * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)
    return f"[{bar}] {percent}% ({current}/{next_goal})"


def get_milestone_checklist(views: int) -> str:
    """Generates a checklist of view milestones."""
    milestones = [1, 5, 25, 100, 500, 1000]
    checks = []
    for m in milestones:
        status = "✓" if views >= m else " "
        label = f"{m} View" if m == 1 else f"{m:,} Views"
        checks.append(f"[{status}] {label}")
    return " | ".join(checks)


def format_uptime(start_time: datetime) -> str:
    """Calculates human-readable uptime string."""
    diff = datetime.now() - start_time
    total_seconds = int(diff.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}h {minutes:02d}m {seconds:02d}s"
    return f"{minutes}m {seconds:02d}s"


def build_dynamic_description(
    views: int,
    likes: int,
    comments_count: int,
    latest_comments: list,
    top_comment: dict,
    github_url: str,
    start_time: datetime,
    config: dict
) -> str:
    """Builds the comprehensive interactive description."""
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sections = []

    # 1. Header & Live Stats
    stats_section = f"""🔥 THIS VIDEO'S TITLE & DESCRIPTION UPDATE AUTOMATICALLY EVERY 30 SECONDS!

📊 LIVE VIDEO STATS:
• 👁️ Current Views    : {views:,}
• 👍 Total Likes      : {likes:,}
• 💬 Total Comments   : {comments_count:,}
• ⏱️ Last Synced      : {timestamp_str}"""
    sections.append(stats_section)

    # 2. Progress Bars (if enabled)
    if config.get("show_progress_bars", True):
        like_bar = make_progress_bar(likes, targets=(5, 10, 25, 50, 100, 500, 1000))
        comment_bar = make_progress_bar(comments_count, targets=(5, 10, 25, 50, 100, 500, 1000))
        progress_section = f"""📈 LIVE COMMUNITY GOALS:
• 👍 Likes Goal    : {like_bar}
• 💬 Comments Goal : {comment_bar}"""
        sections.append(progress_section)

    # 3. Top Comment Hall of Fame (if enabled and exists)
    if config.get("show_top_comment", True) and top_comment:
        top_section = f"""👑 TOP LIKED COMMENT (HALL OF FAME):
• {top_comment['author']} ({top_comment['likes']} 👍): "{top_comment['text']}" """
        sections.append(top_section)

    # 4. Latest 3 Comments (if enabled)
    if config.get("show_latest_comments", True):
        if latest_comments:
            c_lines = "\n".join(f"• {c['author']}: \"{c['text']}\"" for c in latest_comments)
        else:
            c_lines = "• No comments yet. Leave a comment to get featured!"
        comments_section = f"""💬 LATEST 3 COMMENTS:
{c_lines}"""
        sections.append(comments_section)

    # 5. Uptime & Milestones (if enabled)
    if config.get("show_uptime_and_milestones", True):
        uptime_str = format_uptime(start_time)
        milestones_str = get_milestone_checklist(views)
        uptime_section = f"""⏳ BOT UPTIME & MILESTONES:
• ⏱️ Server Live Uptime : {uptime_str} (100% Active)
• 🏆 Milestone Tracker  : {milestones_str}"""
        sections.append(uptime_section)

    # 6. Creator & GitHub Footer
    footer = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 CREATOR & GITHUB:
• Profile: {github_url}
• Leave a comment below! The bot will instantly reply with ❤️ and your exact commenter number!

🤖 Fully Automated with Python & YouTube Data API v3.
#Python #YouTubeAutomation #Coding #LiveStats #GitHub"""
    sections.append(footer)

    return "\n\n".join(sections)


def process_smart_comment_replies(youtube, video_id: str, views: int, total_comments: int, github_url: str):
    """
    Auto-replies to every new comment with personalized details:
    Author name, commenter #, views at the time, heart ❤️, and GitHub link.
    """
    replied_ids = load_replied_comments()
    try:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=15,
            order="time"
        ).execute()

        items = response.get("items", [])
        for item in items:
            top_obj = item.get("snippet", {}).get("topLevelComment", {})
            comment_id = top_obj.get("id")
            s = top_obj.get("snippet", {})
            author = s.get("authorDisplayName", "User")

            if comment_id and comment_id not in replied_ids:
                logger.info("New comment detected from %s. Sending smart personalized reply...", author)

                # Compose personalized message
                personalized_reply = (
                    f"Hey {author}! ❤️ Thanks for commenting on this video! "
                    f"You are commenter #{total_comments} (watched when the video had {views:,} views). "
                    f"Check out my GitHub: {github_url}"
                )

                try:
                    youtube.comments().insert(
                        part="snippet",
                        body={
                            "snippet": {
                                "parentId": comment_id,
                                "textOriginal": personalized_reply
                            }
                        }
                    ).execute()

                    replied_ids.add(comment_id)
                    save_replied_comments(replied_ids)
                    logger.info("Personalized reply sent to %s with ❤️!", author)

                except HttpError as e:
                    logger.error("Failed to post reply to %s: %s", author, e)
                    replied_ids.add(comment_id)
                    save_replied_comments(replied_ids)

    except HttpError as e:
        logger.warning("Error checking comments for replies: %s", e)


def update_video_metadata(youtube, video_id: str, new_title: str, new_description: str, current_snippet: dict) -> bool:
    """Updates video title and description."""
    try:
        updated_snippet = {
            "title": new_title,
            "description": new_description,
            "categoryId": current_snippet.get("categoryId", "28"),
        }

        if "tags" in current_snippet:
            updated_snippet["tags"] = current_snippet["tags"]
        if "defaultLanguage" in current_snippet:
            updated_snippet["defaultLanguage"] = current_snippet["defaultLanguage"]
        if "defaultAudioLanguage" in current_snippet:
            updated_snippet["defaultAudioLanguage"] = current_snippet["defaultAudioLanguage"]

        response = youtube.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": updated_snippet
            }
        ).execute()

        confirmed_title = response.get("snippet", {}).get("title", "")
        return confirmed_title == new_title

    except HttpError as e:
        raise RuntimeError(f"YouTube API Error updating metadata: {e}") from e
