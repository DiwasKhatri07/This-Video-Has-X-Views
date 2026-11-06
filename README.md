# 🚀 YouTube Real-Time Automation Bot (Panel Ready)

Fully automated YouTube bot designed to run on any Server Panel (Pterodactyl, aaPanel, cPanel Python App, Docker, or VPS) with **zero manual inputs**.

---

## 🎯 Features

1. **Dynamic Video Title**:
   - Updates every 30 seconds to:
     `"This Video Has X Views"`
2. **Dynamic Live Description**:
   - Live Views, Likes, and Total Comments counter.
   - **Last 3 Comments**: Automatically displays the newest comments and user names in the description.
   - **GitHub Link**: Features creator profile `https://github.com/diwaskhatri07`.
3. **Auto-Reply to Comments**:
   - Automatically replies to any new comment:
     `"Thanks for your comment! ❤️ Check out my GitHub: https://github.com/diwaskhatri07"`
   - Uses `replied_comments.json` to guarantee no comment is ever replied to twice.
4. **100% Zero-Input**:
   - No prompts or terminal questions. Reads everything directly from [`config.json`](file:///c:/Users/Diwas/Desktop/youtube%20views/config.json).

---

## ⚙️ Configuration (`config.json`)

```json
{
    "video_id": "dINikoQUm6k",
    "check_interval": 30,
    "github_url": "https://github.com/diwaskhatri07",
    "reply_message": "Thanks for your comment! ❤️ Check out my GitHub: https://github.com/diwaskhatri07",
    "auto_reply_enabled": true,
    "max_comments_in_description": 3
}
```

---

## 🚀 How to Run in Any Server Panel

### For Web Hosting / Server Panels (Pterodactyl, aaPanel, cPanel):
1. Upload this entire folder to your server panel directory.
   *(Make sure `token.pickle`, `client_secret.json`, and `config.json` are included)*.
2. Set the startup command to:
   ```bash
   python main.py
   ```
   *(Or `python3 main.py`)*

### For Local / Terminal Run:
```powershell
.\.venv\Scripts\python.exe main.py
```
*(Or `python main.py`)*
