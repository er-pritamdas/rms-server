"""
Application Configuration
"""

from pathlib import Path
from logger.logger import logger

logger.info("Application configuration loaded.")

# --------------------------------------------------
# Logging
# --------------------------------------------------

LOG_FILE = "logs/slack_events.json"
MAX_LOGS = 100

# --------------------------------------------------
# Downloads
# --------------------------------------------------

DOWNLOAD_DIR = Path("downloads")

INSTAGRAM_DOWNLOAD_DIR = DOWNLOAD_DIR / "instagram"