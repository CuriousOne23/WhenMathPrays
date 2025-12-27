"""
Centralized logging configuration for WhenMathPrays editor.

Uses Python's standard logging module with configurable levels and file-only output.
"""

import logging
import sys
import os
from pathlib import Path
from datetime import datetime

# ============================================================================
# Logging Configuration
# ============================================================================

# Get log level from environment variable, default to INFO
LOG_LEVEL_ENV = os.getenv('LOG_LEVEL', 'INFO').upper()
LOG_LEVEL = getattr(logging, LOG_LEVEL_ENV, logging.INFO)

# Create logs directory
LOG_DIR = Path(__file__).parent.parent.parent / 'logs'
LOG_DIR.mkdir(exist_ok=True)

# Generate timestamped log filename
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
LOG_FILE = LOG_DIR / f'interactive_editor_{TIMESTAMP}.log'

# ============================================================================
# Logger Setup
# ============================================================================

def setup_logging():
    """
    Configure Python logging for the application.
    - Logs to file only (no terminal output by default)
    - Uses configurable log level
    - Includes timestamps and module names
    """
    # Create logger
    logger = logging.getLogger('WhenMathPrays')
    logger.setLevel(LOG_LEVEL)

    # Remove any existing handlers
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler (always enabled)
    file_handler = logging.FileHandler(LOG_FILE, mode='a')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Terminal handler (only if explicitly enabled)
    if os.getenv('LOG_TO_TERMINAL', 'false').lower() == 'true':
        terminal_handler = logging.StreamHandler(sys.stdout)
        terminal_handler.setFormatter(formatter)
        logger.addHandler(terminal_handler)

    return logger

# Initialize logging
_root_logger = setup_logging()

# ============================================================================
# Convenience Functions
# ============================================================================

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for the specified module/component.

    Args:
        name: Logger name (e.g., 'controller', 'commands.spinbox')

    Returns:
        Configured logger instance

    Example:
        logger = get_logger('controller')
        logger.debug("Processing primitive change")
        logger.info("File saved successfully")
        logger.warning("Invalid input detected")
        logger.error("Failed to load scenario")
    """
    return _root_logger.getChild(name)

# ============================================================================
# Legacy Debug System (for backward compatibility)
# ============================================================================

# Keep legacy flags for now, but route through new logging system
DEBUG_ENABLED = LOG_LEVEL <= logging.DEBUG
DEBUG_TO_FILE = True
DEBUG_TO_TERMINAL = os.getenv('LOG_TO_TERMINAL', 'false').lower() == 'true'

# Category flags - map to logging levels
DEBUG_SPINBOX = LOG_LEVEL <= logging.DEBUG
DEBUG_TRAJECTORY = LOG_LEVEL <= logging.DEBUG
DEBUG_LABELS = LOG_LEVEL <= logging.DEBUG
DEBUG_LABELS_ASSIGNMENT = LOG_LEVEL <= logging.DEBUG
DEBUG_GAMMA = LOG_LEVEL <= logging.DEBUG
DEBUG_STATE = LOG_LEVEL <= logging.DEBUG
DEBUG_UNDO = LOG_LEVEL <= logging.DEBUG
DEBUG_DRAG = LOG_LEVEL <= logging.DEBUG
DEBUG_BASELINE = LOG_LEVEL <= logging.DEBUG
DEBUG_SYNC = LOG_LEVEL <= logging.DEBUG

_loggers = {}  # Cache for legacy loggers

def get_debug_logger(category: str):
    """
    Legacy function for backward compatibility.
    Use get_logger() for new code.
    """
    if category in _loggers:
        return _loggers[category]

    logger = get_logger(f'debug.{category.lower()}')
    _loggers[category] = logger
    return logger

def debug_print(category: str, message: str, enabled_flag: bool = True):
    """
    Legacy debug print function.
    Use logger.debug() for new code.

    Args:
        category: Debug category
        message: Message to print
        enabled_flag: Category-specific flag (e.g., DEBUG_SPINBOX)

    Example:
        debug_print('SPINBOX', f"Value changed: {value}", DEBUG_SPINBOX)
    """
    if enabled_flag:
        logger = get_debug_logger(category)
        logger.debug(message)
