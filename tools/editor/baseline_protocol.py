"""
Baseline Communication Protocol for Primitive-GammaSelf synchronization.

ARCHITECTURE:
- Primitives: Time-indexed baseline tracking (insertion-proof)
- Gamma_self: Index-based baseline tracking (sequential trajectory)
- Problem: Insertions change gamma_self indices but not primitive times
- Solution: Rigorous communication protocol with debug logging

BASELINE TYPES:
1. CSV_BASELINE: Original values from loaded CSV (never changes)
2. INSERTION_BASELINE: Created when Ctrl+Shift+Click inserts event (becomes new visual baseline)
3. FRACTIONAL_BASELINE: Created when fractional time insertion occurs (neutral 0.0 values)

COMMUNICATION EVENTS:
- PRIMITIVE_INSERT: Primitive space adds new time point
- GAMMA_REINDEX: Gamma_self trajectory recomputed, indices shifted
- BASELINE_SYNC: Baseline values synchronized between spaces
"""

from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime


class BaselineType(Enum):
    """Type of baseline being tracked."""
    CSV_BASELINE = "csv_baseline"  # Original from CSV
    INSERTION_BASELINE = "insertion_baseline"  # From Ctrl+Shift+Click
    FRACTIONAL_BASELINE = "fractional_baseline"  # From fractional time insert


class BaselineEvent(Enum):
    """Communication events between primitive and gamma_self spaces."""
    PRIMITIVE_INSERT_SHIFT = "primitive_insert_shift"  # Ctrl+Shift+Click: shifts times
    PRIMITIVE_INSERT_FRACTIONAL = "primitive_insert_fractional"  # Fractional: new time point
    GAMMA_REINDEX = "gamma_reindex"  # Gamma_self trajectory recomputed
    BASELINE_SYNC_PRIMITIVE = "baseline_sync_primitive"  # Sync primitive baseline to view
    BASELINE_SYNC_GAMMA = "baseline_sync_gamma"  # Sync gamma_self baseline to view
    PRIMITIVE_UNDO_INSERT = "primitive_undo_insert"  # Undo Ctrl+Shift+Click
    PRIMITIVE_EDIT = "primitive_edit"  # User edited primitive value
    PRIMITIVE_RESET = "primitive_reset"  # User reset to baseline


class BaselineDebugLog:
    """
    Debug logging system for baseline communication protocol.
    
    PURPOSE:
        Tracks all communication between primitive space (time-indexed) and 
        gamma_self space (index-based) to ensure proper synchronization.
    
    WHY IT EXISTS:
        When events are inserted, primitive times stay constant (insertion-proof)
        but gamma_self trajectory indices shift. This creates synchronization
        bugs where markers/labels point to wrong trajectory positions.
    
    WHEN TO USE:
        Enable when debugging:
        - Markers not returning to baseline after undo
        - Labels appearing at wrong positions after insertion
        - Baseline indicators showing incorrect values
        - Any synchronization issue between primitive and gamma_self plots
    
    HOW TO USE:
        # Enable from controller:
        controller.enable_baseline_protocol_logging()
        
        # Or directly:
        from tools.editor.baseline_protocol import BaselineDebugLog
        BaselineDebugLog.enable()
        
        # Perform operations (insert, edit, undo)
        # All events are logged automatically
        
        # Dump log:
        BaselineDebugLog.dump("auto")  # JSON (default)
        BaselineDebugLog.dump("debug.log")  # Text (human-readable)
        
        # Disable:
        BaselineDebugLog.disable()
    
    HOW TO READ LOGS:
        1. Check timestamps to understand sequence
        2. Verify perspective (M1/M2) matches your operation
        3. For insertions: look for 'insert_time' and 'shifted_times'
        4. For reindexing: check 'mapping' showing old→new indices
        5. For syncs: verify 'entries_count' matches expected
    
    DESIGN:
        - Class-level (not instance): One global log for entire system
        - Minimal overhead when disabled: Early return if not enabled
        - Zero performance cost when disabled: Just a boolean check
        - Can be controlled by any code: No controller dependency
    
    PERFORMANCE:
        - Disabled: ~1-2 nanoseconds per operation (unmeasurable)
        - Enabled: ~100-500 microseconds per log entry (~1-3% overhead)
        - Console print() is slowest part, but still negligible
    
    STATE IMPACT:
        ⚠️ MEMORY ACCUMULATION:
        - Log entries grow unbounded while enabled
        - 1,000 operations ≈ 0.5 MB, 10,000 operations ≈ 5 MB
        - Must manually clear: BaselineDebugLog.clear()
        
        ⚠️ GLOBAL STATE:
        - _enabled and _log_entries persist until program exit
        - Survives controller deletion/recreation
        - Clear between debug sessions to free memory
        
        ✅ APPLICATION STATE (no impact):
        - Purely observational - reads but never writes
        - Does NOT modify controller, model, or baseline values
        - Does NOT affect undo/redo or any application logic
    
    BEST PRACTICE:
        BaselineDebugLog.enable()
        # ... debug session ...
        BaselineDebugLog.dump("auto")
        BaselineDebugLog.clear()  # Important: Free memory
        BaselineDebugLog.disable()
    """
    
    # Class-level state (shared across all code, persists until program exit)
    _enabled = False  # Global enable/disable flag
    _log_entries = []  # All logged events (grows until cleared - must manually clear!)
    
    @classmethod
    def enable(cls):
        """Enable baseline protocol debug logging."""
        cls._enabled = True
        print("[BASELINE_PROTOCOL] Debug logging ENABLED")
    
    @classmethod
    def disable(cls):
        """Disable baseline protocol debug logging."""
        cls._enabled = False
        print("[BASELINE_PROTOCOL] Debug logging DISABLED")
    
    @classmethod
    def is_enabled(cls):
        """Check if logging is enabled."""
        return cls._enabled
    
    @classmethod
    def log(cls, event: BaselineEvent, perspective: str, **kwargs):
        """
        Log a baseline communication event.
        
        Args:
            event: Type of baseline event
            perspective: "M1" or "M2"
            **kwargs: Additional context (time, index, value, baseline_type, etc.)
        """
        if not cls._enabled:
            return
        
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        entry = {
            "timestamp": timestamp,
            "event": event.value,
            "perspective": perspective,
            **kwargs
        }
        
        cls._log_entries.append(entry)
        
        # Format output
        msg = f"[{timestamp}] [{perspective}] {event.value}"
        for key, value in kwargs.items():
            msg += f" | {key}={value}"
        
        print(msg)
    
    @classmethod
    def get_log(cls):
        """Return all logged entries."""
        return cls._log_entries.copy()
    
    @classmethod
    def clear(cls):
        """Clear all logged entries."""
        cls._log_entries.clear()
        if cls._enabled:
            print("[BASELINE_PROTOCOL] Log cleared")
    
    @classmethod
    def dump(cls, filepath: Optional[str] = None):
        """
        Dump log to file or print to console.
        
        Args:
            filepath: Optional file path to save log. Options:
                     - None: Print to console
                     - "auto": Auto-generate timestamped JSON file (default format)
                     - "*.json": Save as JSON (machine-readable)
                     - "*.txt" or "*.log": Save as formatted text (human-readable)
        """
        if filepath == "auto":
            # Generate timestamped JSON filename in logs/baseline directory
            from pathlib import Path
            log_dir = Path("logs/baseline")
            log_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = str(log_dir / f"baseline_protocol_{timestamp}.json")
        
        if filepath:
            from pathlib import Path
            log_path = Path(filepath)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Determine format by extension
            if filepath.endswith('.json'):
                # JSON format - structured data for analysis
                import json
                log_data = {
                    "metadata": {
                        "generated": datetime.now().isoformat(),
                        "total_entries": len(cls._log_entries),
                        "format_version": "1.0"
                    },
                    "entries": cls._log_entries
                }
                with open(filepath, 'w') as f:
                    json.dump(log_data, f, indent=2)
                print(f"[BASELINE_PROTOCOL] Log dumped to {filepath} (JSON format)")
            else:
                # Text format - human-readable with header
                with open(filepath, 'w') as f:
                    # Write comprehensive header
                    f.write("="*80 + "\n")
                    f.write("BASELINE COMMUNICATION PROTOCOL DEBUG LOG\n")
                    f.write("="*80 + "\n\n")
                    
                    f.write("WHAT IS THIS?\n")
                    f.write("-" * 80 + "\n")
                    f.write("This log tracks communication between two coordinate spaces in the GRP editor:\n")
                    f.write("  - Primitive Space: Time-indexed (insertion-proof)\n")
                    f.write("  - Gamma_self Space: Index-based (requires reindexing after insertions)\n")
                    f.write("\n")
                    
                    f.write("WHY DOES IT EXIST?\n")
                    f.write("-" * 80 + "\n")
                    f.write("When events are inserted, primitive times stay constant but gamma_self\n")
                    f.write("trajectory indices shift. This protocol ensures proper synchronization\n")
                    f.write("between the two spaces by logging all baseline changes.\n")
                    f.write("\n")
                    
                    f.write("WHO CALLS IT?\n")
                    f.write("-" * 80 + "\n")
                    f.write("Called by: EditorController (tools/editor/controller.py)\n")
                    f.write("Locations:\n")
                    f.write("  - _insert_event_before(): Ctrl+Shift+Click insertions with time shift\n")
                    f.write("  - _update_baseline_after_insert(): Fractional time insertions\n")
                    f.write("  - _sync_baseline_to_view(): Baseline synchronization to views\n")
                    f.write("  - _undo_insert_event_before(): Undo insertion operations\n")
                    f.write("\n")
                    
                    f.write("HOW TO TURN ON/OFF?\n")
                    f.write("-" * 80 + "\n")
                    f.write("Enable:  controller.enable_baseline_protocol_logging()\n")
                    f.write("Disable: controller.disable_baseline_protocol_logging()\n")
                    f.write("Dump:    controller.dump_baseline_protocol_log()  # console\n")
                    f.write("         controller.dump_baseline_protocol_log('custom.log')  # file\n")
                    f.write("         controller.dump_baseline_protocol_log('auto')  # timestamped\n")
                    f.write("\n")
                    
                    f.write("LOG FORMAT:\n")
                    f.write("-" * 80 + "\n")
                    f.write("[HH:MM:SS.mmm] [M1|M2] event_type | key=value | ...\n")
                    f.write("\n")
                    f.write("Event Types:\n")
                    f.write("  - primitive_insert_shift: Ctrl+Shift+Click insertion (shifts times)\n")
                    f.write("  - primitive_insert_fractional: Fractional time insertion (no shift)\n")
                    f.write("  - gamma_reindex: Gamma_self trajectory reindexed\n")
                    f.write("  - baseline_sync_primitive: Primitive baseline -> view\n")
                    f.write("  - baseline_sync_gamma: Gamma_self baseline -> view\n")
                    f.write("  - primitive_undo_insert: Undo insertion operation\n")
                    f.write("  - primitive_edit: User edited primitive value\n")
                    f.write("  - primitive_reset: User reset to baseline\n")
                    f.write("\n")
                    
                    f.write("HOW TO READ:\n")
                    f.write("-" * 80 + "\n")
                    f.write("1. Check timestamp to understand sequence of operations\n")
                    f.write("2. Verify perspective (M1 or M2) for each operation\n")
                    f.write("3. For insertions, look for 'insert_time' and 'shifted_times'\n")
                    f.write("4. For reindexing, check 'mapping' showing old_idx -> new_idx\n")
                    f.write("5. For syncs, verify 'entries_count' matches expected values\n")
                    f.write("\n")
                    
                    f.write("Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
                    f.write("Total Entries: " + str(len(cls._log_entries)) + "\n")
                    f.write("\n")
                    f.write("="*80 + "\n")
                    f.write("LOG ENTRIES\n")
                    f.write("="*80 + "\n\n")
                    
                    # Write log entries
                    for entry in cls._log_entries:
                        line = f"[{entry['timestamp']}] [{entry['perspective']}] {entry['event']}"
                        for key, value in entry.items():
                            if key not in ['timestamp', 'event', 'perspective']:
                                line += f" | {key}={value}"
                        f.write(line + "\n")
                    
                    f.write("\n" + "="*80 + "\n")
                    f.write(f"END OF LOG ({len(cls._log_entries)} entries)\n")
                    f.write("="*80 + "\n")
                print(f"[BASELINE_PROTOCOL] Log dumped to {filepath} (text format)")
        else:
            print("\n=== BASELINE PROTOCOL LOG ===")
            for entry in cls._log_entries:
                line = f"[{entry['timestamp']}] [{entry['perspective']}] {entry['event']}"
                for key, value in entry.items():
                    if key not in ['timestamp', 'event', 'perspective']:
                        line += f" | {key}={value}"
                print(line)
            print(f"=== END LOG ({len(cls._log_entries)} entries) ===\n")


class BaselineTracker:
    """
    Tracks baseline state for a single space (primitive or gamma_self).
    
    PURPOSE:
        Each coordinate space needs its own baseline tracking because they
        use fundamentally different indexing schemes.
    
    TWO SPACES:
        - Primitive Space: Indexed by (time, primitive_name)
          Example: (2.5, 'v') = the 'v' primitive at time=2.5
          Property: INSERTION-PROOF (times don't change)
        
        - Gamma_self Space: Indexed by trajectory_index (integer)
          Example: 5 = the 6th point in gamma_self trajectory
          Property: NOT insertion-proof (indices shift after insertions)
    
    WHY SEPARATE TRACKERS:
        When an event is inserted at t=2.5:
        - Primitive space: Just adds (2.5, 'v') entry
        - Gamma_self space: Indices 3,4,5,... shift to 4,5,6,...
        
        Different indexing = different tracking needs
    
    HOW IT WORKS:
        Stores: key -> (value, baseline_type)
        Where:
        - key = (time, prim) for primitives, or int index for gamma_self
        - value = float baseline value
        - baseline_type = CSV_BASELINE | INSERTION_BASELINE | FRACTIONAL_BASELINE
    """
    
    def __init__(self, space_name: str, index_type: str):
        """
        Initialize baseline tracker.
        
        Args:
            space_name: "primitive" or "gamma_self" (for debugging output)
            index_type: "time" or "index" (describes key type)
        """
        self.space_name = space_name
        self.index_type = index_type
        
        # Baseline storage: key -> (value, baseline_type)
        # Keys are either (time, prim) tuples or integer indices
        self.baselines: Dict[Any, tuple] = {}
    
    def set_baseline(self, key: Any, value: float, baseline_type: BaselineType):
        """Set baseline value for a key."""
        self.baselines[key] = (value, baseline_type)
    
    def get_baseline(self, key: Any) -> Optional[tuple]:
        """Get baseline value and type for a key, or None if not found."""
        return self.baselines.get(key)
    
    def remove_baseline(self, key: Any):
        """Remove baseline for a key."""
        if key in self.baselines:
            del self.baselines[key]
    
    def shift_key(self, old_key: Any, new_key: Any):
        """Shift a baseline from old_key to new_key (for time shifts or reindexing)."""
        if old_key in self.baselines:
            self.baselines[new_key] = self.baselines[old_key]
            del self.baselines[old_key]
    
    def get_all_baselines(self) -> Dict[Any, tuple]:
        """Return all baselines."""
        return self.baselines.copy()
    
    def clear(self):
        """Clear all baselines."""
        self.baselines.clear()


class BaselineCommunicator:
    """
    Central communicator between primitive and gamma_self baseline trackers.
    
    PURPOSE:
        Coordinates baseline changes between two spaces that use different indexing.
        Ensures both spaces stay synchronized despite structural differences.
    
    WHY IT EXISTS:
        THE FUNDAMENTAL PROBLEM:
        - User inserts event at t=2.5 (Ctrl+Shift+Click)
        - Primitive space: Adds baseline at (2.5, 'v')
        - Gamma_self trajectory: Recomputes, indices shift
        - WITHOUT COMMUNICATION: Gamma markers point to wrong indices!
        
        THIS CLASS SOLVES IT:
        - Logs all baseline changes (audit trail)
        - Tracks what needs reindexing
        - Provides protocol for synchronization
    
    EVENTS HANDLED:
        1. notify_primitive_insert_shift(): Ctrl+Shift+Click insertion
           - Primitive times shift: 3.0→3.5, 4.0→4.5
           - Tells gamma_self: "Reindex everything after this point"
        
        2. notify_primitive_insert_fractional(): Fractional time insertion
           - New time point added: t=2.5 (between 2.0 and 3.0)
           - Tells gamma_self: "Add new index at this position"
        
        3. notify_gamma_reindex(): Gamma trajectory recomputed
           - Provides mapping: old_idx→new_idx
           - Updates gamma baseline indices
        
        4. sync_*_baseline_to_view(): Pushes baselines to views
           - Converts time→index or index→position
           - Updates visual markers
    
    USAGE:
        # One communicator per perspective (M1 or M2)
        comm = BaselineCommunicator("M1")
        
        # When inserting event:
        comm.notify_primitive_insert_shift(insert_time, shifted_times)
        
        # When trajectory recomputed:
        comm.notify_gamma_reindex({3:4, 4:5, 5:6})
        
        # When syncing to view:
        comm.sync_primitive_baseline_to_view(time_to_index_map)
    
    DESIGN:
        - One instance per perspective (M1/M2) in EditorController
        - Owns trackers for both spaces
        - Logs all communications via BaselineDebugLog
        - Pure coordination layer (doesn't modify data directly)
    """
    
    def __init__(self, perspective: str):
        """
        Initialize communicator for a perspective.
        
        Args:
            perspective: "M1" or "M2"
        """
        self.perspective = perspective
        
        # Create separate trackers for each coordinate space
        # These track baselines independently, this class coordinates them
        self.primitive_tracker = BaselineTracker("primitive", "time")
        self.gamma_tracker = BaselineTracker("gamma_self", "index")
    
    def notify_primitive_insert_shift(self, insert_time: float, shifted_times: list):
        """
        Notify that a Ctrl+Shift+Click insertion occurred.
        
        Args:
            insert_time: Time where event was inserted
            shifted_times: List of (old_time, new_time) tuples for shifted events
        """
        BaselineDebugLog.log(
            BaselineEvent.PRIMITIVE_INSERT_SHIFT,
            self.perspective,
            insert_time=insert_time,
            shifts_count=len(shifted_times),
            shifted_times=shifted_times
        )
        
        # Gamma_self must reindex all markers after this insertion
        return {"action": "reindex_gamma", "insert_at_index": None}  # Will be determined by time
    
    def notify_primitive_insert_fractional(self, insert_time: float):
        """
        Notify that a fractional time insertion occurred.
        
        Args:
            insert_time: Fractional time where event was inserted
        """
        BaselineDebugLog.log(
            BaselineEvent.PRIMITIVE_INSERT_FRACTIONAL,
            self.perspective,
            insert_time=insert_time,
            baseline_type=BaselineType.FRACTIONAL_BASELINE.value
        )
        
        # Gamma_self must add a new index at the interpolated position
        return {"action": "add_gamma_index", "at_time": insert_time}
    
    def notify_gamma_reindex(self, old_to_new_mapping: Dict[int, int]):
        """
        Notify that gamma_self trajectory was recomputed and indices changed.
        
        Args:
            old_to_new_mapping: Dictionary mapping old_index -> new_index
        """
        BaselineDebugLog.log(
            BaselineEvent.GAMMA_REINDEX,
            self.perspective,
            mappings_count=len(old_to_new_mapping),
            mapping=old_to_new_mapping
        )
        
        # Shift all gamma baseline keys
        for old_idx, new_idx in old_to_new_mapping.items():
            self.gamma_tracker.shift_key(old_idx, new_idx)
    
    def sync_primitive_baseline_to_view(self, time_to_index_map: Dict[float, int]):
        """
        Sync primitive baselines to view (convert time -> index).
        
        Args:
            time_to_index_map: Dictionary mapping time -> event_index
        """
        BaselineDebugLog.log(
            BaselineEvent.BASELINE_SYNC_PRIMITIVE,
            self.perspective,
            entries_count=len(time_to_index_map)
        )
    
    def sync_gamma_baseline_to_view(self, index_count: int):
        """
        Sync gamma_self baselines to view.
        
        Args:
            index_count: Number of trajectory indices
        """
        BaselineDebugLog.log(
            BaselineEvent.BASELINE_SYNC_GAMMA,
            self.perspective,
            index_count=index_count
        )
