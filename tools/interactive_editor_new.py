#!/usr/bin/env python3
"""
Interactive Scenario Editor - Entry Point

Visual diagnostic tool for GRP scenario primitives with real-time
gamma_self trajectory preview.

Usage:
    python tools/interactive_editor.py <csv_file>

Example:
    python tools/interactive_editor.py data/single_dating_to_love_M1.csv

Phase 3.5 Architecture Refactoring:
    - Slim entry point (~100 lines, down from 1094 lines)
    - Application logic moved to EditorApplication (application.py)
    - File path management moved to FileManager (file_manager.py)
    - Widget creation moved to UIBuilder (ui_builder.py)
    - Window management moved to EditorMainWindow (main_window.py)
    
    Benefits:
        - Clean separation of concerns
        - Testable components
        - Phase 4 ready (multi-window architecture)
        - Eliminates "god class" anti-pattern
"""

import sys
import argparse
from pathlib import Path

# PySide6 imports
from PySide6.QtWidgets import QApplication

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.editor.application import EditorApplication


def main():
    """Main entry point for interactive scenario editor."""
    parser = argparse.ArgumentParser(
        description='Interactive Scenario Editor for GRP',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/interactive_editor.py data/single_dating_to_love_M1.csv
  
Features:
  ✓ Dual-perspective editing (M1 and M2 with overlay visualization)
  ✓ Drag primitives (v, r, f, a, S) with real-time trajectory preview
  ✓ Lock/unlock events (right-click)
  ✓ Undo/redo (Ctrl+Z / Ctrl+Y)
  ✓ Delete events (Ctrl+Click)
  ✓ Insert events (Ctrl+Shift+Click or via time entry widget)
  ✓ Diagnostic "what-if" markers (Shift+Click)
  ✓ Edit gamma_self_0 initial position
  ✓ Flexible workspace with dockable panels
  ✓ Automatic M1/M2 file discovery
  
Keyboard Shortcuts:
  - Ctrl+S: Save CSV
  - Ctrl+Z: Undo
  - Ctrl+Y: Redo
  - +/-: Zoom in/out (context-aware)
  - 0: Reset view
  - F: Toggle fixed view
  - G: Edit gamma_self_0
  - Tab/Space: Switch perspective (M1 ↔ M2)
  
Mouse Interactions:
  - Drag marker: Edit primitive value (shows preview)
  - Click hollow marker: Commit preview
  - Double-click hollow: Cancel preview
  - Right-click marker: Lock/unlock
  - Ctrl+Click marker: Delete event
  - Ctrl+Shift+Click: Insert event before
  - Shift+Click: Place diagnostic "what-if" marker
  
File Handling:
  - Load M1 → Automatically looks for M2
  - Load M2 → Automatically looks for M1
  - M1-only → Load into both perspectives (M1 selected)
  - M2-only → Load into both perspectives (M2 selected)
  - Save respects active perspective (M1 → M1_modified.csv, M2 → M2_modified.csv)
  
Phase Status:
  ✅ Phase 1: Single-perspective editing (COMPLETE)
  ✅ Phase 2.0: PySide6 migration, undo/redo (COMPLETE)
  ✅ Phase 2.1: Diagnostic markers, gamma_self0, insert events (COMPLETE)
  ✅ Phase 2.2: Delete events (COMPLETE)
  ✅ Phase 3.1: QDockWidget flexible workspace (COMPLETE)
  ✅ Phase 3.2: Perspective switcher (COMPLETE)
  ✅ Phase 3.3: M2 overlay rendering (COMPLETE)
  ✅ Phase 3.4: State management refactoring (COMPLETE)
  ✅ Phase 3.5: Architecture refactoring (COMPLETE)
  ⏳ Phase 4: Advanced features (inverse editing, sensitivity analysis, analysis window)
        """
    )
    
    parser.add_argument('csv_file', type=str, 
                       help='Path to CSV file to edit (M1, M2, or single-perspective)')
    
    args = parser.parse_args()
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName('GRP Interactive Scenario Editor')
    
    try:
        # Create and run editor application
        # All complexity delegated to EditorApplication
        editor = EditorApplication(args.csv_file, app)
        sys.exit(editor.run())
    except ValueError as e:
        # File validation error (from FileManager)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Unexpected error
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
