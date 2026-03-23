"""Minimal server-side usage analytics.

Append-only JSONL event log — no PII stored.
Session hash is derived from IP + User-Agent (not stored raw).

Events:
  evaluation_started   — request received at /api/evaluate/*
  evaluation_completed — evaluation pipeline returned successfully
  results_page_viewed  — GET to results page (if applicable)
"""
import asyncio
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

# Default to a writable path; override via ANALYTICS_LOG_PATH env var.
_DEFAULT_LOG_PATH = Path("/tmp/analytics.jsonl")
_LOG_PATH = Path(os.environ.get("ANALYTICS_LOG_PATH", str(_DEFAULT_LOG_PATH)))


def hash_session(ip: str, user_agent: str) -> str:
    """Return a short, non-reversible hex digest of IP + User-Agent."""
    raw = f"{ip}|{user_agent}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _write_event(record: dict) -> None:
    """Synchronous JSONL append (called via asyncio.to_thread)."""
    _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


async def log_event(event: str, session_hash: str, **extra) -> None:
    """Async-safe: write one event record to the JSONL log.

    Args:
        event:        Event name (e.g. 'evaluation_started').
        session_hash: Non-reversible session identifier.
        **extra:      Additional fields (e.g. latency_ms=120).
    """
    record = {
        "event": event,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_hash": session_hash,
        **extra,
    }
    await asyncio.to_thread(_write_event, record)
