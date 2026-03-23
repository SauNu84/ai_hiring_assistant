#!/usr/bin/env python3
"""Analytics query script.

Reads the JSONL analytics log and prints:
  1. Evaluations per week (last 8 weeks)
  2. 7-day return rate (sessions that ran ≥2 evaluations within any 7-day window)

Usage:
  python backend/scripts/query_analytics.py [--log /path/to/analytics.jsonl]
"""
import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


_DEFAULT_LOG = Path(os.environ.get("ANALYTICS_LOG_PATH", "/tmp/analytics.jsonl"))


def load_events(log_path: Path) -> list[dict]:
    if not log_path.exists():
        print(f"Log file not found: {log_path}", file=sys.stderr)
        return []
    events = []
    with log_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return events


def isoparse(ts: str) -> datetime:
    return datetime.fromisoformat(ts).astimezone(timezone.utc)


def evaluations_per_week(events: list[dict], weeks: int = 8) -> None:
    """Print evaluation counts grouped by ISO calendar week."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(weeks=weeks)

    week_counts: dict[str, int] = defaultdict(int)
    for e in events:
        if e.get("event") != "evaluation_completed":
            continue
        ts = isoparse(e["timestamp"])
        if ts < cutoff:
            continue
        iso_week = ts.strftime("%G-W%V")  # e.g. 2026-W12
        week_counts[iso_week] += 1

    print(f"\n=== Evaluations per week (last {weeks} weeks) ===")
    if not week_counts:
        print("  No data.")
        return
    for week in sorted(week_counts):
        print(f"  {week}: {week_counts[week]}")
    print(f"  Total: {sum(week_counts.values())}")


def seven_day_return_rate(events: list[dict]) -> None:
    """Print % of sessions that ran ≥2 evaluations within any 7-day window."""
    # Group evaluation_completed timestamps by session_hash
    session_ts: dict[str, list[datetime]] = defaultdict(list)
    for e in events:
        if e.get("event") != "evaluation_completed":
            continue
        session_ts[e["session_hash"]].append(isoparse(e["timestamp"]))

    total_sessions = len(session_ts)
    returning = 0
    for ts_list in session_ts.values():
        ts_list.sort()
        for i in range(len(ts_list) - 1):
            if (ts_list[i + 1] - ts_list[i]) <= timedelta(days=7):
                returning += 1
                break

    rate = (returning / total_sessions * 100) if total_sessions else 0.0
    print(f"\n=== 7-day return rate ===")
    print(f"  Total unique sessions:  {total_sessions}")
    print(f"  Returning sessions:     {returning}")
    print(f"  Return rate:            {rate:.1f}%")


def main() -> None:
    parser = argparse.ArgumentParser(description="Query usage analytics log.")
    parser.add_argument("--log", type=Path, default=_DEFAULT_LOG, help="Path to analytics.jsonl")
    parser.add_argument("--weeks", type=int, default=8, help="Number of past weeks to show")
    args = parser.parse_args()

    events = load_events(args.log)
    print(f"Loaded {len(events)} events from {args.log}")

    evaluations_per_week(events, weeks=args.weeks)
    seven_day_return_rate(events)


if __name__ == "__main__":
    main()
