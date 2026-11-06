<div align="center">

<!-- Animated Title -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=35&pause=1000&color=FF0000&center=true&vCenter=true&multiline=true&width=800&height=100&lines=%F0%9F%94%A5+This+Video+Has+X+Views;YouTube+Real-Time+Automation+Bot" alt="Typing SVG" />

<br/>

<!-- YouTube Video Live Badge -->
<a href="https://www.youtube.com/watch?v=dINikoQUm6k">
  <img src="https://img.shields.io/badge/▶_WATCH_LIVE-YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube"/>
</a>

<!-- Live Metrics Badges -->
<br/><br/>
<img src="badges/views.svg" alt="Views"/>
<img src="badges/likes.svg" alt="Likes"/>
<img src="badges/comments.svg" alt="Comments"/>
<img src="badges/status.svg" alt="Bot Status"/>

<br/><br/>

<!-- Tech Stack Badges -->
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![YouTube API](https://img.shields.io/badge/YouTube_Data_API-v3-FF0000?style=flat-square&logo=youtube&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Bot-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

<br/>

**A fully automated YouTube bot that dynamically updates your video's Title and Description in real-time based on live view count, likes, comments, and more — running 24/7 via GitHub Actions!**

<br/>

[🚀 Quick Start](#-quick-start) •
[✨ Features](#-features) •
[⚙️ Configuration](#%EF%B8%8F-configuration) •
[🤖 GitHub Actions](#-github-actions-cicd) •
[📸 Screenshots](#-live-demo) •
[👨‍💻 Author](#-author)

</div>

---

## 📸 Live Demo

> **🔴 Watch the bot in action!** The title and description of this video updates automatically:
>
> ### 👉 [youtube.com/watch?v=dINikoQUm6k](https://www.youtube.com/watch?v=dINikoQUm6k)

**What happens when you watch, like, or comment:**

```
📺 Title Updates:
   Before: "This Video Has 4 Views"
   After:  "This Video Has 5 Views"  ← Updates within 30 seconds!

📝 Description Updates:
   📊 LIVE VIDEO STATS:
   • 👁️ Current Views    : 5
   • 👍 Total Likes      : 3
   • 💬 Total Comments   : 12
   • ⏱️ Last Synced      : 2026-11-06 11:30:45

   📈 LIVE COMMUNITY GOALS:
   • 👍 Likes Goal    : [████████░░] 80% (8/10)
   • 💬 Comments Goal : [██████░░░░] 60% (12/25)

   👑 TOP LIKED COMMENT (HALL OF FAME):
   • @viewer (5 👍): "This bot is insane!"

   💬 LATEST 3 COMMENTS:
   • @user1: "Amazing automation!"
   • @user2: "How does this work?"
   • @user3: "Mind blown 🤯"

💬 Auto-Reply:
   "Hey @user1! ❤️ You are commenter #12 (watched when the video had 5 views).
    Check out my GitHub: https://github.com/diwaskhatri07"
```

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Features
- **Dynamic Title** — Updates to `This Video Has X Views` every 30 seconds
- **Live Description Dashboard** — Real-time Views, Likes, Comments counter
- **Auto Comment Reply** — Personalized reply with ❤️, commenter #, and GitHub link
- **Smart Caching** — Only calls YouTube update API when stats actually change

</td>
<td width="50%">

### 🔥 Advanced Features
- **👑 Top Comment Hall of Fame** — Most liked comment gets featured
- **📊 ASCII Progress Bars** — Visual like & comment goals
- **⏳ Live Bot Uptime** — Shows how long the bot has been active
- **🏆 Milestone Tracker** — Checkbox for 1, 5, 25, 100, 500, 1K views

</td>
</tr>
</table>

### 🤖 Deployment Options

| Platform | Status | Description |
|----------|--------|-------------|
| **GitHub Actions** | ✅ Recommended | Free, runs every 5 minutes via cron |
| **Pterodactyl Panel** | ✅ Supported | For game hosting panels |
| **Docker / VPS** | ✅ Supported | For self-hosted servers |
| **Local PC** | ✅ Supported | For development and testing |

---

## 📁 Project Structure

```
📦 youtube-live-view-counter/
├── 🤖 .github/
│   └── workflows/
│       ├── youtube-updater.yml      # ← Main bot: runs every 5 min
│       └── update-badges.yml        # ← Live metrics badge generator
├── 📊 badges/
│   ├── views.svg                    # Live view count badge
│   ├── likes.svg                    # Live like count badge
│   ├── comments.svg                 # Live comment count badge
│   └── status.svg                   # Bot online status badge
├── 🔧 scripts/
│   └── generate_badges.py           # Badge SVG generator
├── 🐍 auth.py                       # OAuth 2.0 authentication
├── 🐍 title.py                      # Stats engine + description builder
├── 🐍 main.py                       # Core automation daemon
├── 🐍 generate_video.py             # Sample video generator (OpenCV)
├── ⚙️ config.json                   # All bot settings (zero-input)
├── 📊 metrics.json                  # Latest fetched metrics
├── 🐳 Dockerfile                    # Docker deployment
├── 🐳 docker-compose.yml            # Docker Compose config
├── 🔧 deploy_vps.sh                 # One-click VPS deployment
├── 🔧 youtube-updater.service       # Systemd service file
├── 📜 requirements.txt              # Python dependencies
├── 📜 LICENSE                        # MIT License
└── 📖 README.md                     # You are here!
```

---

## 🚀 Quick Start

### Option 1: GitHub Actions (Recommended — Free & Always On)

> **No server needed!** GitHub Actions runs the bot for free.

**Step 1:** Fork this repository

**Step 2:** Set up YouTube API credentials ([detailed guide below](#-youtube-api-setup))

**Step 3:** Add GitHub Secrets:

| Secret Name | Value |
|------------|-------|
| `YOUTUBE_TOKEN_PICKLE_B64` | Base64 encoded `token.pickle` |
| `YOUTUBE_CLIENT_SECRET_JSON` | Contents of `client_secret.json` |

```bash
# Generate base64 of your token.pickle:
base64 -w 0 token.pickle
# (On Windows PowerShell):
[Convert]::ToBase64String([IO.File]::ReadAllBytes("token.pickle"))
```

**Step 4:** Enable GitHub Actions in your fork → The bot will start automatically!

---

### Option 2: Local / Server Panel / VPS

```bash
# Clone the repo
git clone https://github.com/DiwasKhatri07/youtube-live-view-counter.git
cd youtube-live-view-counter

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.\.venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Place your client_secret.json and token.pickle in this directory

# Run the bot!
python main.py
```

---

## 🔑 YouTube API Setup

<details>
<summary><b>📋 Click to expand step-by-step guide</b></summary>

### 1. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g., `YouTube-Bot`)

### 2. Enable YouTube Data API v3
1. Navigate to **APIs & Services** → **Library**
2. Search for **YouTube Data API v3**
3. Click **Enable**

### 3. Create OAuth 2.0 Credentials
1. Go to **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Application type: **Desktop app**
4. Download the JSON file → rename to `client_secret.json`

### 4. Configure OAuth Consent Screen
1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** → Fill in required details
3. Under **Test users**, add your Gmail address
4. Click **PUBLISH APP** (to remove testing restrictions)

### 5. Generate token.pickle
```bash
# Run once on your local PC to authenticate via browser:
python auth.py
# This opens a browser for Google login.
# After login, token.pickle is generated automatically!
```

### 6. Upload to GitHub Secrets (for GitHub Actions)
```bash
# Base64 encode token.pickle:
base64 -w 0 token.pickle
# Copy the output → Add as GitHub Secret: YOUTUBE_TOKEN_PICKLE_B64

# Copy client_secret.json content → Add as GitHub Secret: YOUTUBE_CLIENT_SECRET_JSON
```

</details>

---

## ⚙️ Configuration

All settings are in `config.json` — **zero manual input required**:

```json
{
    "video_id": "dINikoQUm6k",
    "check_interval": 30,
    "github_url": "https://github.com/diwaskhatri07",
    "auto_reply_enabled": true,
    "show_top_comment": true,
    "show_latest_comments": true,
    "show_progress_bars": true,
    "show_uptime_and_milestones": true,
    "max_comments_in_description": 3
}
```

| Key | Type | Description |
|-----|------|-------------|
| `video_id` | `string` | Your YouTube Video ID |
| `check_interval` | `int` | Seconds between each check (default: `30`) |
| `github_url` | `string` | Your GitHub profile URL |
| `auto_reply_enabled` | `bool` | Auto-reply to new comments with ❤️ |
| `show_top_comment` | `bool` | Show 👑 most-liked comment in description |
| `show_latest_comments` | `bool` | Show latest 3 comments in description |
| `show_progress_bars` | `bool` | Show ASCII like & comment goal bars |
| `show_uptime_and_milestones` | `bool` | Show bot uptime and milestone checklist |
| `max_comments_in_description` | `int` | Number of recent comments to feature |

---

## 🤖 GitHub Actions CI/CD

### Workflows

| Workflow | Schedule | Purpose |
|----------|----------|---------|
| `youtube-updater.yml` | Every 5 minutes | Fetches YouTube stats, updates title, description, and auto-replies |
| `update-badges.yml` | Every 10 minutes | Generates live SVG metric badges for README |

> **ℹ️ Note:** GitHub Actions cron has a minimum interval of 5 minutes. For 30-second updates, use a VPS or server panel.

### Required GitHub Secrets

| Secret | How to Get |
|--------|-----------|
| `YOUTUBE_TOKEN_PICKLE_B64` | `base64 -w 0 token.pickle` |
| `YOUTUBE_CLIENT_SECRET_JSON` | Contents of `client_secret.json` |

---

## 📊 API Quota & Safety

| Metric | Value |
|--------|-------|
| YouTube Daily Quota | 10,000 units/day (free) |
| `videos.list` cost | 1 unit per call |
| `videos.update` cost | 50 units per call |
| `commentThreads.list` cost | 1 unit per call |
| `comments.insert` cost | 50 units per call |
| **GitHub Actions (5 min interval)** | ~300 list + ~50 updates = **~2,800 units/day** ✅ |
| **Panel/VPS (30 sec interval)** | ~2,880 list + ~200 updates = **~12,880 units/day** ⚠️ |

> 💡 **Smart Optimization**: The bot only calls `videos.update` when stats actually change, significantly reducing quota usage.

---

## 🐳 Docker Deployment

```bash
# Build and run
docker compose up -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

---

## 🔧 VPS Deployment (Ubuntu/Debian)

```bash
# Upload files to VPS
scp -r . root@YOUR_VPS_IP:/opt/youtube-bot

# SSH and run installer
ssh root@YOUR_VPS_IP
cd /opt/youtube-bot
chmod +x deploy_vps.sh
sudo ./deploy_vps.sh

# Manage
systemctl status youtube-updater   # Check status
journalctl -u youtube-updater -f   # Live logs
systemctl restart youtube-updater  # Restart
```

---

## 🛠️ Tech Stack

<div align="center">

| Technology | Purpose |
|:----------:|:-------:|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | Core Language |
| ![YouTube](https://img.shields.io/badge/YouTube_API_v3-FF0000?style=for-the-badge&logo=youtube&logoColor=white) | Video Stats & Management |
| ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white) | CI/CD Automation |
| ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) | Containerization |
| ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Server Deployment |

</div>

---

## 👨‍💻 Author

<div align="center">

<img src="https://github.com/DiwasKhatri07.png" width="120" style="border-radius: 50%;" alt="Diwas Khatri"/>

### **Diwas Khatri** 🇳🇵

*Developer • Automator • Open Source Enthusiast*

[![GitHub](https://img.shields.io/badge/GitHub-DiwasKhatri07-181717?style=for-the-badge&logo=github)](https://github.com/DiwasKhatri07)
[![YouTube](https://img.shields.io/badge/YouTube-@DiwasOP-FF0000?style=for-the-badge&logo=youtube)](https://www.youtube.com/@DiwasOP)

</div>

---

## ⭐ Support

If you found this project interesting or useful:

- 🌟 **Star** this repository
- 🍴 **Fork** it and create your own version
- 👁️ **Watch** the [live video](https://www.youtube.com/watch?v=dINikoQUm6k) and leave a comment
- 💬 **Share** it with your developer friends

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ and 🐍 in Nepal 🇳🇵**

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=14&pause=1000&color=888888&center=true&vCenter=true&width=500&lines=Thanks+for+visiting!+Star+⭐+if+you+liked+it!" alt="Footer"/>

</div>
