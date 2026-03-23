#!/bin/bash
# ============================================
# GitHub Contribution Bot - VPS Setup
# ============================================
# Run this on your VPS to set everything up.

set -e

REPO_URL="https://github.com/Mossab28/Mossab28.git"
INSTALL_DIR="$HOME/github-contrib-bot"

echo "=== GitHub Contribution Bot Setup ==="

# 1. Clone repo
if [ -d "$INSTALL_DIR" ]; then
    echo "Directory exists, pulling latest..."
    cd "$INSTALL_DIR" && git pull
else
    echo "Cloning repo..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# 2. Configure git identity
git config user.name "Mossab28"
git config user.email "mossab.mirandeney1@gmail.com"

# 3. Set up cron (daily at random hour between 10h-20h)
CRON_CMD="0 $(shuf -i 10-20 -n 1) * * * cd $INSTALL_DIR && /usr/bin/python3 contribution-bot/bot.py >> $INSTALL_DIR/contribution-bot/cron.log 2>&1"

# Remove old cron if exists, then add new one
(crontab -l 2>/dev/null | grep -v "github-contrib-bot" || true; echo "$CRON_CMD") | crontab -

echo ""
echo "=== Setup complete ==="
echo "Install dir: $INSTALL_DIR"
echo "Cron installed (runs daily)"
echo ""
echo "Commands:"
echo "  Backfill last year:  cd $INSTALL_DIR && python3 contribution-bot/bot.py --backfill"
echo "  Test daily run:      cd $INSTALL_DIR && python3 contribution-bot/bot.py"
echo "  Check cron:          crontab -l"
echo "  View logs:           tail -f $INSTALL_DIR/contribution-bot/cron.log"
