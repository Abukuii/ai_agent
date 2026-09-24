"""Logging configuration.

Phase 1 uses a plain structured console formatter (timestamp | level |
logger name | message). Later phases will extend this with request/user/
agent-execution IDs (see project roadmap, section 17: Observability) once
those concepts exist in the codebase.
"""

import logging
import sys

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Third-party loggers that are noisy at INFO/DEBUG and rarely useful here.
_QUIET_LOGGERS = {
    "aiogram.event": logging.WARNING,
    "httpx": logging.WARNING,
    "httpcore": logging.WARNING,
}


def setup_logging(level: str = "INFO") -> None:
    """Configure the root logger for console output.

    Idempotent: safe to call more than once (e.g. in tests), since it
    replaces rather than accumulates handlers.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=_LOG_FORMAT, datefmt=_DATE_FORMAT))

    root = logging.getLogger()
    root.setLevel(level.upper())
    root.handlers.clear()
    root.addHandler(handler)

    for logger_name, quiet_level in _QUIET_LOGGERS.items():
        logging.getLogger(logger_name).setLevel(quiet_level)
