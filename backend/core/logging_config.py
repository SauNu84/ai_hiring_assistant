"""Centralized logging configuration for AI Hiring Assistant backend.

Usage:
    from core.logging_config import get_logger
    logger = get_logger(__name__)
    logger.info("Something happened", extra={"event": "evaluation_started"})

Log levels (controlled via LOG_LEVEL env var, default: INFO):
    DEBUG   — verbose tracing (dev only)
    INFO    — normal operations
    WARNING — unexpected but recoverable conditions
    ERROR   — failures that affect a request
    CRITICAL — system-level failures

Output format (controlled via LOG_FORMAT env var):
    json   — structured JSON lines (default in production)
    text   — human-readable format (useful locally)
"""
import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any


# ── Configuration from environment ──────────────────────────────────────────
_LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
_LOG_FORMAT = os.environ.get("LOG_FORMAT", "json").lower()


class _JsonFormatter(logging.Formatter):
    """Emit each log record as a single JSON line."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Attach any extra fields the caller provided
        for key, value in record.__dict__.items():
            if key not in (
                "name", "msg", "args", "levelname", "levelno", "pathname",
                "filename", "module", "exc_info", "exc_text", "stack_info",
                "lineno", "funcName", "created", "msecs", "relativeCreated",
                "thread", "threadName", "processName", "process", "message",
            ):
                payload[key] = value

        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


class _TextFormatter(logging.Formatter):
    """Human-readable formatter: timestamp | LEVEL | logger — message."""

    FMT = "%(asctime)s | %(levelname)-8s | %(name)s — %(message)s"
    DATEFMT = "%Y-%m-%dT%H:%M:%S"

    def __init__(self) -> None:
        super().__init__(fmt=self.FMT, datefmt=self.DATEFMT)


def _build_handler() -> logging.Handler:
    handler = logging.StreamHandler(sys.stdout)
    if _LOG_FORMAT == "text":
        handler.setFormatter(_TextFormatter())
    else:
        handler.setFormatter(_JsonFormatter())
    return handler


def configure_logging() -> None:
    """Call once at application startup (main.py lifespan or module level).

    Idempotent — safe to call multiple times; only configures the root logger
    the first time.
    """
    root = logging.getLogger()
    if root.handlers:
        return  # already configured

    level = getattr(logging, _LOG_LEVEL, logging.INFO)
    root.setLevel(level)
    root.addHandler(_build_handler())

    # Silence noisy third-party loggers
    for noisy in ("httpx", "httpcore", "anthropic", "uvicorn.access"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    logging.getLogger(__name__).debug(
        "Logging configured",
        extra={"log_level": _LOG_LEVEL, "log_format": _LOG_FORMAT},
    )


def get_logger(name: str) -> logging.Logger:
    """Return a named logger (call configure_logging first)."""
    return logging.getLogger(name)
