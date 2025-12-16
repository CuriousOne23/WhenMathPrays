"""
Centralized debug configuration for WhenMathPrays editor.

Provides category-based logging that can route to terminal, file, or both.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

# ============================================================================
# Master Debug Controls
# ============================================================================

DEBUG_ENABLED = True      # Master switch - disables ALL debug output when False
DEBUG_TO_FILE = True      # True=file, False=terminal
DEBUG_TO_TERMINAL = False # Set True to enable terminal output alongside file

# ============================================================================
# Category Flags - Enable/disable specific debug categories
# ============================================================================

DEBUG_SPINBOX = False      # Spinbox primitive editor signal flow
DEBUG_TRAJECTORY = False   # Trajectory computation and display
DEBUG_LABELS = False       # Label synchronization and management
DEBUG_LABELS_ASSIGNMENT = False  # Label assignment block (fine-grained)
# When True, enables only the label assignment block debug output in trajectory_panel_pyqtgraph.py.
# Use this for deep debugging of label placement logic without enabling all label debug output.
DEBUG_GAMMA = False        # Gamma_self calculations
DEBUG_STATE = False        # State save/restore operations
DEBUG_UNDO = False         # Undo/redo operations
DEBUG_DRAG = False         # Drag and drop operations
DEBUG_BASELINE = False     # Baseline protocol
DEBUG_SYNC = False         # Label sync operations

# ============================================================================
# Logger Setup
# ============================================================================

_loggers = {}  # Cache for created loggers

def get_debug_logger(category: str):
    """
    Get or create a logger for the specified category.
    
    Args:
        category: Debug category (e.g., 'SPINBOX', 'TRAJECTORY')
    
    Returns:
        Logger instance that respects category flags and routing settings
    
    Example:
        logger = get_debug_logger('SPINBOX')
        if DEBUG_SPINBOX:
            logger.debug("Connection established")
    """
    if category in _loggers:
        return _loggers[category]
    
    logger = logging.getLogger(f"WhenMathPrays.{category}")
    logger.setLevel(logging.DEBUG if DEBUG_ENABLED else logging.CRITICAL)
    logger.handlers.clear()  # Remove any existing handlers
    
    if DEBUG_ENABLED:
        # Create formatter
        formatter = logging.Formatter('[%(name)s] %(message)s')
        
        # Add file handler if enabled
        if DEBUG_TO_FILE:
            # Create logs directory if it doesn't exist
            log_dir = Path(__file__).parent.parent.parent / 'logs'
            log_dir.mkdir(exist_ok=True)
            
            # Use timestamped log file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = log_dir / f'debug_{timestamp}.log'
            
            file_handler = logging.FileHandler(log_file, mode='a')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        # Add terminal handler if enabled
        if DEBUG_TO_TERMINAL:
            terminal_handler = logging.StreamHandler(sys.stdout)
            terminal_handler.setFormatter(formatter)
            logger.addHandler(terminal_handler)
    
    # Cache the logger
    _loggers[category] = logger
    return logger


# ============================================================================
# Convenience Functions
# ============================================================================

def debug_print(category: str, message: str, enabled_flag: bool = True):
    """
    Print debug message if category is enabled.
    
    Args:
        category: Debug category
        message: Message to print
        enabled_flag: Category-specific flag (e.g., DEBUG_SPINBOX)
    
    Example:
        debug_print('SPINBOX', f"Value changed: {value}", DEBUG_SPINBOX)
    """
    if DEBUG_ENABLED and enabled_flag:
        logger = get_debug_logger(category)
        logger.debug(message)
