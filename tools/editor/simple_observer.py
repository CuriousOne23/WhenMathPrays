"""
Simple Observer - Lightweight observability for editor operations.

Provides visibility into controller and application operations without
performance overhead. Single grep point for debugging.

Usage:
    observer = SimpleObserver()
    observer.log('INSERT_EVENT', time=3.5, perspective='M1')
    
    # Output: [OBS:INSERT_EVENT] time=3.5, perspective='M1'
"""

import logging

class SimpleObserver:
    """
    Lightweight observer for editor operations.
    
    Logs operations at boundaries (entry/exit points) to provide
    visibility into application flow without cluttering inner loops.
    
    Attributes:
        enabled: Boolean flag to enable/disable logging (default True)
    """
    
    def __init__(self, enabled: bool = True):
        """
        Initialize observer.
        
        Args:
            enabled: Whether logging is enabled (default True)
        """
        self.enabled = enabled
        self.logger = logging.getLogger('WhenMathPrays')
        
    def log(self, operation: str, **kwargs):
        """
        Log an operation with context.
        
        Args:
            operation: Operation name (e.g., 'INSERT_EVENT', 'DELETE_EVENT')
            **kwargs: Context information (time, perspective, index, etc.)
        
        Example:
            observer.log('INSERT_EVENT', time=3.5, perspective='M1')
            # Output: [OBS:INSERT_EVENT] time=3.5, perspective='M1'
        """
        if not self.enabled:
            return
            
        # Format context as key=value pairs
        context = ', '.join(f'{k}={v}' for k, v in kwargs.items())
        self.logger.info(f"[OBS:{operation}] {context}")
