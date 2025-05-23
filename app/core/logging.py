"""
Logging configuration for the Cartouche Bot Service.
Sets up structured logging with loguru.
"""

import sys
import os
from pathlib import Path
from loguru import logger

from app.core.settings import LOG_LEVEL, LOG_FILE


def setup_logging():
    """
    Configure logging for the application.
    - Console output with colors
    - File output with rotation
    """
    # Ensure log directory exists
    log_file_path = Path(LOG_FILE)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Remove default logger
    logger.remove()

    # Add console logger
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=LOG_LEVEL,
        colorize=True,
    )

    # Add file logger with rotation
    logger.add(
        LOG_FILE,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=LOG_LEVEL,
        rotation="10 MB",
        retention="1 week",
    )

    return logger
