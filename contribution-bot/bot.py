#!/usr/bin/env python3
"""
GitHub Contribution Bot
Fills your GitHub contribution graph with commits.

Usage:
  - Backfill past year:  python3 bot.py --backfill
  - Daily mode (cron):   python3 bot.py
"""

import os
import subprocess
import random
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# --- Config ---
REPO_DIR = Path(__file__).parent
DATA_FILE = REPO_DIR / "data.txt"


def run(cmd, env=None):
    merged = {**os.environ, **(env or {})}
    subprocess.run(cmd, cwd=REPO_DIR, shell=True, env=merged, check=True,
                   capture_output=True)


def make_commit(date: datetime, count: int = 1):
    """Create count commits at the given date."""
    iso = date.strftime("%Y-%m-%dT%H:%M:%S")
    env = {"GIT_AUTHOR_DATE": iso, "GIT_COMMITTER_DATE": iso}
    for i in range(count):
        ts = date.strftime("%Y-%m-%d %H:%M:%S")
        DATA_FILE.write_text(f"contribution: {ts} #{i}\n")
        run("git add data.txt", env)
        run(f'git commit -m "update: {ts}"', env)


def backfill(days: int = 365):
    """Fill the last N days with random commits."""
    today = datetime.now()
    for i in range(days, 0, -1):
        day = today - timedelta(days=i)
        weekday = day.weekday()

        # More commits on weekdays, fewer on weekends
        if weekday < 5:
            count = random.choices([0, 1, 2, 3, 4], weights=[10, 30, 35, 20, 5])[0]
        else:
            count = random.choices([0, 1, 2], weights=[40, 40, 20])[0]

        if count > 0:
            # Random hour between 9h-23h
            hour = random.randint(9, 23)
            minute = random.randint(0, 59)
            commit_date = day.replace(hour=hour, minute=minute, second=0)
            make_commit(commit_date, count)
            print(f"  {day.strftime('%Y-%m-%d')} -> {count} commits")
        else:
            print(f"  {day.strftime('%Y-%m-%d')} -> skip")

    run("git push origin main")
    print("\nDone! Backfill pushed.")


def daily():
    """Daily commit (for cron)."""
    now = datetime.now()
    weekday = now.weekday()

    if weekday < 5:
        count = random.choices([1, 2, 3, 4], weights=[30, 40, 20, 10])[0]
    else:
        count = random.choices([0, 1, 2], weights=[30, 50, 20])[0]

    if count > 0:
        make_commit(now, count)
        run("git push origin main")
        print(f"{now.strftime('%Y-%m-%d')}: {count} commits pushed")
    else:
        print(f"{now.strftime('%Y-%m-%d')}: rest day, no commits")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--backfill", action="store_true",
                        help="Fill the last 365 days")
    parser.add_argument("--days", type=int, default=365,
                        help="Number of days to backfill (default: 365)")
    args = parser.parse_args()

    if args.backfill:
        backfill(args.days)
    else:
        daily()
