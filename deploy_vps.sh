#!/usr/bin/env bash
# ==============================================================================
# YouTube Dynamic Title & Views Automation - VPS Auto Deployment Script
# Supports: Ubuntu 20.04+, Debian 10+, CentOS / Rocky / AlmaLinux
# ==============================================================================

set -e

APP_DIR="/opt/youtube-views"
SERVICE_NAME="youtube-updater"

echo "=========================================================="
echo "   Setting up YouTube Views Automation on VPS..."
echo "=========================================================="

# 1. Update packages and install Python3 & venv
if command -v apt-get >/dev/null 2>&1; then
    echo "[1/5] Installing dependencies via apt..."
    apt-get update -y
    apt-get install -y python3 python3-pip python3-venv git
elif command -v dnf >/dev/null 2>&1; then
    echo "[1/5] Installing dependencies via dnf..."
    dnf install -y python3 python3-pip git
fi

# 2. Setup application folder
echo "[2/5] Setting up directory: $APP_DIR..."
mkdir -p "$APP_DIR"

# If current directory is not $APP_DIR, copy files over
if [ "$PWD" != "$APP_DIR" ]; then
    echo "Copying files to $APP_DIR..."
    cp -r * "$APP_DIR"/ 2>/dev/null || true
fi

cd "$APP_DIR"

# 3. Create virtualenv and install requirements
echo "[3/5] Setting up Python virtual environment..."
python3 -m venv .venv
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

# 4. Configure systemd service
echo "[4/5] Installing systemd service..."
cp youtube-updater.service /etc/systemd/system/${SERVICE_NAME}.service
systemctl daemon-reload
systemctl enable ${SERVICE_NAME}.service
systemctl restart ${SERVICE_NAME}.service

echo "[5/5] Service started!"
echo "=========================================================="
echo " Status Check  : systemctl status ${SERVICE_NAME}"
echo " Live Logs     : journalctl -u ${SERVICE_NAME} -f"
echo " File Logs     : tail -f $APP_DIR/automation.log"
echo " Restart       : systemctl restart ${SERVICE_NAME}"
echo " Stop          : systemctl stop ${SERVICE_NAME}"
echo "=========================================================="
