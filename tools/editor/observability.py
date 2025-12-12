"""
Observability infrastructure for interactive editor debugging.

This module provides centralized, toggle-able logging for debugging complex
event-driven interactions in the editor, particularly for perspective switching
and state synchronization.

Design Principles:
- Separate from business logic
- Zero performance impact when disabled
- Structured output for analysis
- Production-safe (can ship with product)

Usage:
    # Initialize at application startup
    from tools.editor.observability import ObservabilityLog
    ObservabilityLog.initialize()  # Reads EDITOR_DEBUG env var
    
    # Or force enable for debugging:
    ObservabilityLog.initialize(enabled=True)
    
    # Log events anywhere in code:
    ObservabilityLog.event("perspective_switch", old="M1", new="M2")
    ObservabilityLog.event("label_created", time=42.0, primitive="v", perspective="M1")

Environment Variable:
    EDITOR_DEBUG=true    Enable observability logging
    EDITOR_DEBUG=false   Disable observability logging (default)

Log Location:
    logs/editor_debug_YYYYMMDD_HHMMSS.log
"""

import logging
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class ObservabilityLog:
    """
    Centralized observability system for editor debugging.
    
    Provides structured, timestamped logging of editor events for debugging
    complex interactions. Can be enabled/disabled without code changes.
    """
    
    _enabled: bool = False
    _logger: Optional[logging.Logger] = None
    _log_file: Optional[Path] = None
    _initialized: bool = False
    
    @classmethod
    def initialize(cls, enabled: Optional[bool] = None) -> None:
        """
        Initialize observability system.
        
        Args:
            enabled: True/False to override, None to read from EDITOR_DEBUG env var
        
        Example:
            # Read from environment
            ObservabilityLog.initialize()
            
            # Force enable for debugging session
            ObservabilityLog.initialize(enabled=True)
        """
        if cls._initialized:
            return  # Already initialized
        
        # Determine if enabled
        if enabled is None:
            env_value = os.environ.get("EDITOR_DEBUG", "false").lower()
            enabled = env_value in ("true", "1", "yes", "on")
        
        cls._enabled = enabled
        cls._initialized = True
        
        if cls._enabled:
            cls._setup_logger()
    
    @classmethod
    def _setup_logger(cls) -> None:
        """Setup file logger with structured format."""
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Create timestamped log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cls._log_file = log_dir / f"editor_debug_{timestamp}.log"
        
        # Setup logger
        cls._logger = logging.getLogger("EditorObservability")
        cls._logger.setLevel(logging.DEBUG)
        cls._logger.handlers.clear()  # Clear any existing handlers
        
        # File handler with minimal formatting (we handle structure in JSON)
        handler = logging.FileHandler(cls._log_file, encoding='utf-8')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s.%(msecs)03d | %(message)s',
            datefmt='%H:%M:%S'
        ))
        cls._logger.addHandler(handler)
        
        # Log initialization
        cls._logger.info("=" * 80)
        cls._logger.info(f"Editor Observability Initialized")
        cls._logger.info(f"Log file: {cls._log_file}")
        cls._logger.info(f"Timestamp: {datetime.now().isoformat()}")
        cls._logger.info("=" * 80)
    
    @classmethod
    def event(cls, event_type: str, **kwargs: Any) -> None:
        """
        Log a structured event.
        
        Args:
            event_type: Event identifier (e.g., "perspective_switch_start")
            **kwargs: Event-specific data (must be JSON-serializable)
        
        Example:
            ObservabilityLog.event("label_created", 
                                  time=42.0, 
                                  primitive="v",
                                  perspective="M1")
        """
        if not cls._enabled or cls._logger is None:
            return
        
        event_data = {
            "event": event_type,
            **kwargs
        }
        
        try:
            # Log as JSON for easy parsing
            cls._logger.info(json.dumps(event_data, default=str))
        except (TypeError, ValueError) as e:
            # Fallback if JSON serialization fails
            cls._logger.warning(f"Failed to serialize event {event_type}: {e}")
            cls._logger.info(f"{{\"event\": \"{event_type}\", \"error\": \"serialization_failed\"}}")
    
    @classmethod
    def is_enabled(cls) -> bool:
        """
        Check if observability is enabled.
        
        Returns:
            True if observability logging is active, False otherwise
        """
        return cls._enabled
    
    @classmethod
    def get_log_file(cls) -> Optional[Path]:
        """
        Get path to current log file.
        
        Returns:
            Path to log file if observability is enabled, None otherwise
        """
        return cls._log_file
    
    @classmethod
    def reset(cls) -> None:
        """
        Reset observability system (mainly for testing).
        
        Closes logger and clears state. Call initialize() again to re-enable.
        """
        if cls._logger is not None:
            for handler in cls._logger.handlers[:]:
                handler.close()
                cls._logger.removeHandler(handler)
        
        cls._enabled = False
        cls._logger = None
        cls._log_file = None
        cls._initialized = False
    
    @classmethod
    def section(cls, title: str) -> None:
        """
        Log a section separator for readability.
        
        Args:
            title: Section title
        
        Example:
            ObservabilityLog.section("Perspective Switch M1 -> M2")
        """
        if not cls._enabled or cls._logger is None:
            return
        
        cls._logger.info("")
        cls._logger.info("=" * 80)
        cls._logger.info(f"  {title}")
        cls._logger.info("=" * 80)


# Convenience function for common event patterns
def log_component_event(component: str, event: str, **kwargs: Any) -> None:
    """
    Log an event with automatic component tagging.
    
    Args:
        component: Component name (e.g., "PrimitivePanel", "Controller")
        event: Event type (e.g., "perspective_change", "label_created")
        **kwargs: Additional event data
    
    Example:
        log_component_event("PrimitivePanel", "label_created",
                          time=42.0, primitive="v")
    """
    ObservabilityLog.event(f"{component}_{event}", component=component, **kwargs)
