"""
Centralized Logger Setup

Provides a logger instance configured to log to both console and a daily rolling file
located in the `log_collection` directory.
"""

import os
import logging
from datetime import datetime


class DailyFileHandler(logging.FileHandler):
    """
    A custom logging handler that dynamically creates and writes to a log file
    named YYYY-MM-DD.log under the specified log directory.
    """

    def __init__(self, log_dir, encoding="utf-8", delay=False):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.current_date = datetime.now().date()
        filename = os.path.join(self.log_dir, f"{self.current_date}.log")
        super().__init__(filename, mode="a", encoding=encoding, delay=delay)

    def emit(self, record):
        # Dynamically check and transition to a new file at midnight/next day
        now = datetime.now().date()
        if now != self.current_date:
            self.current_date = now
            self.close()
            self.baseFilename = os.path.abspath(
                os.path.join(self.log_dir, f"{self.current_date}.log")
            )
            self.stream = self._open()
        super().emit(record)


# Ensure log collection directory exists relative to the repository root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "log_collection")
os.makedirs(LOG_DIR, exist_ok=True)

# Logger setup
logger = logging.getLogger("rms_server")
logger.setLevel(logging.INFO)
logger.propagate = False

# Avoid duplicating handlers if logger module is imported multiple times
if not logger.handlers:
    # Formatter to include timestamp, level, filename, line number, and message
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 1. Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. Daily File Handler
    file_handler = DailyFileHandler(LOG_DIR, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a namespaced child logger that propagates to the root rms_server logger.
    """
    if name == "__main__":
        return logger
    if not name.startswith("rms_server"):
        return logging.getLogger(f"rms_server.{name}")
    return logging.getLogger(name)
