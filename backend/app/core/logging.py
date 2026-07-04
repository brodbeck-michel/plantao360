import logging
import json
import sys
from datetime import datetime, timezone
from typing import Any

from app.common.context import get_request_id, get_correlation_id


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        request_id = get_request_id() or ""
        correlation_id = get_correlation_id() or ""

        log_entry: dict[str, Any] = {
            "event": getattr(record, "event", record.levelname),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id,
            "correlation_id": correlation_id,
        }

        if hasattr(record, "method"):
            log_entry["method"] = record.method
        if hasattr(record, "path"):
            log_entry["path"] = record.path
        if hasattr(record, "status"):
            log_entry["status"] = record.status
        if hasattr(record, "duration_ms"):
            log_entry["duration_ms"] = record.duration_ms
        if hasattr(record, "request_id") and record.request_id:
            log_entry["request_id"] = record.request_id
        if hasattr(record, "correlation_id") and record.correlation_id:
            log_entry["correlation_id"] = record.correlation_id

        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, ensure_ascii=False)


def setup_logging(log_level: str = "INFO") -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
