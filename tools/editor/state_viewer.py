"""
State Viewer - Runtime state transition tracking and logging.

Provides visibility into program behavior for debugging and learning.
Minimal overhead (~100ns per operation), fixed memory (ring buffer).
"""

import os
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class StateChange:
    """Record of a single state transition."""
    id: int
    timestamp: datetime
    operation: str
    entity: Tuple[Any, ...]  # (event_id, primitive, perspective) or similar
    location: str  # file:line
    changes: Dict[str, Tuple[Any, Any]]  # {field: (before, after)}
    
    def has_warning(self) -> bool:
        """Check if this operation has any warnings."""
        for field, (before, after) in self.changes.items():
            # Check for unchanged fields that should have changed
            if field == 'gamma_position' and self.operation == 'reset_primitive':
                if after is not None:  # Should be None after reset
                    return True
            if field == 'in_modified_dict' and self.operation == 'reset_primitive':
                if after is True:  # Should be False after reset
                    return True
        return False
    
    def get_warning_message(self) -> Optional[str]:
        """Get warning message if any."""
        if not self.has_warning():
            return None
        
        messages = []
        for field, (before, after) in self.changes.items():
            if field == 'gamma_position' and self.operation == 'reset_primitive':
                if after is not None:
                    messages.append(f"Expected gamma_position to change to None, but remained {after}")
            if field == 'in_modified_dict' and self.operation == 'reset_primitive':
                if after is True:
                    messages.append(f"Expected in_modified_dict to be False, but remained True")
        
        return "; ".join(messages) if messages else None


class StateViewer:
    """
    Central state transition tracker.
    
    Zero-overhead when disabled, minimal overhead when enabled.
    Fixed memory footprint (ring buffer).
    """
    
    # Configuration
    _enabled = os.environ.get('STATE_VIEWER', '1') == '1'
    MAX_HISTORY = 1000  # Ring buffer size
    
    # Storage
    _buffer: List[Optional[StateChange]] = [None] * MAX_HISTORY
    _write_pos = 0
    _counter = 0
    
    # File loading metadata
    _loaded_file_m1: Optional[str] = None
    _loaded_file_m2: Optional[str] = None
    
    @classmethod
    def record(cls, operation: str, entity: Tuple[Any, ...], 
               changes: Dict[str, Tuple[Any, Any]], location: str = None):
        """
        Record a state transition.
        
        Args:
            operation: Operation name ('reset_primitive', 'update_primitive', etc.)
            entity: What was affected (e.g., (event_id, prim, perspective))
            changes: Dict of {field: (before_value, after_value)}
            location: File:line where operation occurred (auto-detected if None)
        """
        if not cls._enabled:
            return
        
        # Auto-detect location if not provided
        if location is None:
            stack = traceback.extract_stack()
            if len(stack) >= 2:
                frame = stack[-2]  # Calling frame
                location = f"{frame.filename.split('\\')[-1]}:{frame.lineno}"
            else:
                location = "unknown"
        
        # Create state change record
        change = StateChange(
            id=cls._counter,
            timestamp=datetime.now(),
            operation=operation,
            entity=entity,
            location=location,
            changes=changes
        )
        
        # Store in ring buffer
        cls._buffer[cls._write_pos] = change
        cls._write_pos = (cls._write_pos + 1) % cls.MAX_HISTORY
        cls._counter += 1
        
        # Debug output for warnings
        if change.has_warning():
            print(f"⚠️  [STATE_VIEWER] Warning in operation #{change.id}: {change.get_warning_message()}")
    
    @classmethod
    def get_recent(cls, n: int = 10) -> List[StateChange]:
        """Get last N state changes."""
        # Collect non-None entries in order
        result = []
        for i in range(cls.MAX_HISTORY):
            idx = (cls._write_pos - 1 - i) % cls.MAX_HISTORY
            if cls._buffer[idx] is not None:
                result.append(cls._buffer[idx])
                if len(result) >= n:
                    break
        
        return list(reversed(result))  # Return in chronological order
    
    @classmethod
    def get_warnings(cls) -> List[StateChange]:
        """Get all state changes with warnings."""
        return [c for c in cls._buffer if c and c.has_warning()]
    
    @classmethod
    def export_to_file(cls, filepath: str):
        """
        Export state log to file.
        
        Args:
            filepath: Path to write log file
        """
        import sys
        import platform
        
        # Get session info
        warnings = cls.get_warnings()
        total_ops = sum(1 for c in cls._buffer if c is not None)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Header
            f.write("STATE VIEWER LOG\n")
            f.write("=" * 80 + "\n")
            f.write(f"Session: {datetime.now().isoformat()}\n")
            f.write(f"Python: {sys.version.split()[0]}\n")
            f.write(f"Platform: {platform.platform()}\n")
            f.write(f"Working directory: {cls._sanitize_path(os.getcwd())}\n")
            
            # File loading info
            if cls._loaded_file_m1 or cls._loaded_file_m2:
                f.write("\nLoaded files:\n")
                if cls._loaded_file_m1 and cls._loaded_file_m2:
                    if cls._loaded_file_m1 == cls._loaded_file_m2:
                        f.write(f"  Single file: {cls._sanitize_path(cls._loaded_file_m1)}\n")
                        f.write(f"    → M1 and M2 (both perspectives)\n")
                    else:
                        f.write(f"  Dual-file mode:\n")
                        f.write(f"    M1: {cls._sanitize_path(cls._loaded_file_m1)}\n")
                        f.write(f"    M2: {cls._sanitize_path(cls._loaded_file_m2)}\n")
                elif cls._loaded_file_m1:
                    f.write(f"  M1 only: {cls._sanitize_path(cls._loaded_file_m1)}\n")
                elif cls._loaded_file_m2:
                    f.write(f"  M2 only: {cls._sanitize_path(cls._loaded_file_m2)}\n")
            
            f.write(f"\nTotal operations: {total_ops}\n")
            f.write(f"Warnings: {len(warnings)}\n")
            f.write("=" * 80 + "\n\n")
            
            # Warnings section
            if warnings:
                f.write("⚠️  WARNINGS DETECTED\n")
                f.write("-" * 80 + "\n")
                for w in warnings:
                    f.write(f"  #{w.id:04d}: {w.operation} at {w.location}\n")
                f.write("\n")
            
            # Operation log
            f.write("OPERATION LOG\n")
            f.write("=" * 80 + "\n\n")
            
            # Get all changes in chronological order
            changes = []
            for i in range(cls.MAX_HISTORY):
                idx = (cls._write_pos - cls.MAX_HISTORY + i) % cls.MAX_HISTORY
                if cls._buffer[idx] is not None:
                    changes.append(cls._buffer[idx])
            
            # Write each change
            for change in changes:
                f.write(f"[{change.id:04d}] {change.operation}\n")
                f.write(f"Time: {change.timestamp.isoformat()}\n")
                f.write(f"Entity: {change.entity}\n")
                f.write(f"Location: {change.location}\n")
                
                if change.changes:
                    f.write("Changes:\n")
                    for field, (before, after) in change.changes.items():
                        if before != after:
                            f.write(f"  {field}: {before} → {after}  ✓\n")
                        else:
                            f.write(f"  {field}: {before} → {after}  ⚠️  UNCHANGED\n")
                
                if change.has_warning():
                    f.write(f"⚠️  WARNING: {change.get_warning_message()}\n")
                
                f.write("\n")
    
    @classmethod
    def set_loaded_files(cls, m1_path: Optional[str] = None, m2_path: Optional[str] = None):
        """
        Record which files were loaded for each perspective.
        
        Args:
            m1_path: Path to CSV file loaded for M1 perspective
            m2_path: Path to CSV file loaded for M2 perspective
        """
        if m1_path:
            cls._loaded_file_m1 = m1_path
        if m2_path:
            cls._loaded_file_m2 = m2_path
    
    @classmethod
    def _sanitize_path(cls, path: str) -> str:
        """
        Sanitize path to remove username for privacy.
        Replaces Windows usernames in paths with 'user'.
        
        Args:
            path: Path string to sanitize
            
        Returns:
            Sanitized path with username replaced
        """
        import re
        # Replace C:\Users\<username>\ pattern with C:\Users\user\
        path = re.sub(r'C:\\Users\\[^\\]+\\', r'C:\\Users\\user\\', path, flags=re.IGNORECASE)
        # Also handle forward slashes
        path = re.sub(r'C:/Users/[^/]+/', r'C:/Users/user/', path, flags=re.IGNORECASE)
        return path
    
    @classmethod
    def clear(cls):
        """Clear all recorded state changes."""
        cls._buffer = [None] * cls.MAX_HISTORY
        cls._write_pos = 0
        cls._counter = 0
        cls._loaded_file_m1 = None
        cls._loaded_file_m2 = None
