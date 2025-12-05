#!/usr/bin/env python3
"""
Interactive Scenario Editor

Visual diagnostic tool for GRP scenario primitives with real-time
gamma_self trajectory preview.

Usage:
    python tools/interactive_editor.py <csv_file>

Example:
    python tools/interactive_editor.py data/single_dating_to_love_M1.csv
"""

import sys
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from tkinter import filedialog
import tkinter as tk

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.editor.model import EditorModel
from tools.editor.controller import EditorController
from tools.editor.views.primitive_panel import PrimitivePanel
from tools.editor.views.trajectory_panel import TrajectoryPanel


class InteractiveEditor:
    """Main application class for interactive scenario editor."""
    
    def __init__(self, csv_file: str):
        """
        Initialize interactive editor.
        
        Args:
            csv_file: Path to CSV file to load
        """
        self.csv_file = Path(csv_file)
        
        # Create matplotlib figure with 2-panel layout
        self.fig = plt.figure(figsize=(14, 8))
        self.fig.canvas.manager.set_window_title(
            f'Interactive Scenario Editor - {self.csv_file.name}')
        
        # Create grid layout: 5 rows (primitives) x 2 columns
        # Left column: Primitives (5 subplots stacked)
        # Right column: Trajectory (spans all 5 rows)
        gs = GridSpec(5, 2, figure=self.fig, hspace=0.3, wspace=0.3,
                     left=0.08, right=0.95, top=0.94, bottom=0.08)
        
        # Initialize model (structured: uses Event/Marker)
        self.model = EditorModel()

        # Initialize views (pass structured callbacks)
        self.primitive_panel = PrimitivePanel(
            fig=self.fig,
            grid_spec=gs[:, 0],
            on_primitive_changed=self._on_primitive_changed,
            on_lock_toggle=self._on_lock_toggle,
            on_primitive_preview=self._on_primitive_preview,
            on_primitive_reset=self._on_primitive_reset
        )

        self.trajectory_panel = TrajectoryPanel(
            fig=self.fig,
            grid_spec=gs[:, 1]
        )

        # Initialize controller (structured)
        self.controller = EditorController(
            model=self.model,
            primitive_panel=self.primitive_panel,
            trajectory_panel=self.trajectory_panel
        )

        # Add toolbar buttons
        self._setup_toolbar()

        # Load scenario (structured: Event/Marker)
        self.controller.load_scenario(str(self.csv_file))

        # Connect keyboard shortcuts
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
    
    def _setup_toolbar(self):
        """Setup custom toolbar buttons."""
        toolbar = self.fig.canvas.toolbar
        if toolbar:
            # Add Save button to the toolbar
            import matplotlib
            from matplotlib.widgets import Button
            # Place button in a new axes on the figure
            save_ax = self.fig.add_axes([0.85, 0.96, 0.08, 0.035])  # [left, bottom, width, height]
            self._save_button = Button(save_ax, 'Save', color='#e0e0e0', hovercolor='#b0ffb0')
            self._save_button.on_clicked(self._on_save_button)
            save_ax._button = self._save_button  # Prevent garbage collection

    def _on_save_button(self, event):
        """Handle Save button click: commit previews and save to a non-original file."""
        self.controller.commit_changes()
        # Determine if current file is the original (in data/ and does not end with _modified.csv)
        original = (
            self.csv_file.parent.name == 'data' and
            not self.csv_file.stem.endswith('_modified')
        )
        if original:
            # Save to a new file with _modified suffix
            new_name = self.csv_file.parent / f"{self.csv_file.stem}_modified.csv"
            self.controller.save_scenario(str(new_name))
            print(f"Saved to: {new_name} (original not overwritten)")
            # Update self.csv_file to point to the new file for future saves
            self.csv_file = new_name
            # Optionally update window title
            self.fig.canvas.manager.set_window_title(
                f'Interactive Scenario Editor - {self.csv_file.name}')
        elif self.csv_file:
            self.controller.save_scenario(str(self.csv_file))
            print(f"Saved to: {self.csv_file}")
        else:
            print("No file path set. Use Save As.")

    
    def _on_primitive_changed(self, event_index, primitive, value):
        """Handle primitive change from primitive panel (on release)."""
        self.controller.on_primitive_changed(event_index, primitive, value)
    
    def _on_primitive_preview(self, event_index, primitive, value):
        """Handle primitive preview from primitive panel (during drag)."""
        self.controller.on_primitive_preview(event_index, primitive, value)
    
    def _on_primitive_reset(self, event_index, primitive):
        """Handle primitive reset from primitive panel (double-click)."""
        self.controller.on_primitive_reset(event_index, primitive)
    
    def _on_lock_toggle(self, event_index):
        """Handle lock toggle from primitive panel."""
        self.controller.on_lock_toggle(event_index)
    
    def _on_key_press(self, event):
        """Handle keyboard shortcuts."""
        if event.key == 'ctrl+s':
            self._on_save_button(event)
        elif event.key == 'c':
            # Commit previews
            self.controller.commit_changes()
        elif event.key == 'escape':
            # Cancel previews
            self.controller.cancel_changes()
        elif event.key == 'g':
            # Edit gamma_self_0 initial position
            self._edit_gamma_self_0()
        elif event.key == 'f':
            # Toggle fixed view mode
            self.controller.trajectory_panel.fixed_view = not self.controller.trajectory_panel.fixed_view
            status = "ON" if self.controller.trajectory_panel.fixed_view else "OFF"
            print(f"Fixed view: {status}")
        elif event.key in ['+', '=']:
            # Zoom in (context-aware: only the panel under cursor)
            if event.inaxes:
                # Check if cursor is in gamma_self panel
                if event.inaxes == self.controller.trajectory_panel.ax:
                    self.controller.trajectory_panel.zoom_in()
                    print("Zoomed in on gamma_self")
                else:
                    # Cursor is in primitive panel
                    self.controller.primitive_panel.zoom_in()
                    print("Zoomed in on primitives")
            else:
                # No axis under cursor, zoom both
                self.controller.trajectory_panel.zoom_in()
                self.controller.primitive_panel.zoom_in()
                print("Zoomed in")
        elif event.key == '-':
            # Zoom out (context-aware: only the panel under cursor)
            if event.inaxes:
                if event.inaxes == self.controller.trajectory_panel.ax:
                    self.controller.trajectory_panel.zoom_out()
                    print("Zoomed out on gamma_self")
                else:
                    self.controller.primitive_panel.zoom_out()
                    print("Zoomed out on primitives")
            else:
                self.controller.trajectory_panel.zoom_out()
                self.controller.primitive_panel.zoom_out()
                print("Zoomed out")
        elif event.key == '0':
            # Reset view - always reset both panels for convenience
            self.controller.trajectory_panel.reset_view()
            self.controller.primitive_panel.reset_view()
            print("Reset all views")
    
    def _edit_gamma_self_0(self):
        """Edit initial gamma_self position."""
        from tkinter import simpledialog
        
        current = self.controller.model.gamma_self_0
        
        # Create Tkinter root (hidden)
        root = tk.Tk()
        root.withdraw()
        
        # Get real part
        real_part = simpledialog.askfloat(
            "Edit Gamma_self_0",
            f"Enter REAL part (Ego↔We axis):\n\nCurrent: {current.real:+.1f}{current.imag:+.1f}j\n\nExamples:\n  Strangers: 0\n  Friends: +5\n  Exes (hurt): -5",
            initialvalue=current.real,
            parent=root
        )
        
        if real_part is None:
            root.destroy()
            return
        
        # Get imaginary part
        imag_part = simpledialog.askfloat(
            "Edit Gamma_self_0",
            f"Enter IMAGINARY part (Hate↔Love axis):\n\nCurrent: {current.real:+.1f}{current.imag:+.1f}j\n\nExamples:\n  Strangers: 0\n  Friends: +8\n  Exes (hurt): -3",
            initialvalue=current.imag,
            parent=root
        )
        
        root.destroy()
        
        if imag_part is None:
            return
        
        # Update gamma_self_0
        self.controller.model.gamma_self_0 = complex(real_part, imag_part)
        
        # Recompute trajectory from new starting point
        self.controller._recompute_trajectory_immediate()
        
        print(f"Gamma_self_0 set to {real_part:+.1f}{imag_part:+.1f}j")
    
    def _save_as(self):
        """Open Save As dialog and save CSV."""
        # Suggest filename with _modified suffix
        original_stem = self.csv_file.stem
        original_parent = self.csv_file.parent
        suggested_name = original_parent / f"{original_stem}_modified.csv"
        
        # Create Tkinter root (hidden)
        root = tk.Tk()
        root.withdraw()
        
        # Open file dialog
        filepath = filedialog.asksaveasfilename(
            title="Save Modified Scenario",
            initialdir=str(original_parent),
            initialfile=suggested_name.name,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        root.destroy()
        
        if filepath:
            self.controller.save_scenario(filepath)
            print(f"Saved to: {filepath}")
    
    def run(self):
        """Show UI and enter event loop."""
        plt.show()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Interactive Scenario Editor for GRP',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/interactive_editor.py data/single_dating_to_love_M1.csv
  
Usage:
  - Drag primitive points vertically to change values (shows hollow preview)
  - Click HOLLOW point to continue editing from preview position
  - Double-click HOLLOW point to cancel preview and return to original
  - Press 'C' to COMMIT changes (hollow → filled, pins marker at current gamma_self)
  - Press ESC to CANCEL changes (revert to committed)
  - Press 'G' to edit Gamma_self_0 initial position (strangers=0+0j, exes=-5-3j, etc.)
  - Right-click on point to lock/unlock
  - Press 'F' to toggle Fixed View (prevent auto-zoom during edits)
  - Press '+' or '=' to ZOOM IN (context-aware: zooms panel under cursor)
  - Press '-' to ZOOM OUT (context-aware: zooms panel under cursor)
  - Press '0' to RESET view (context-aware: resets panel under cursor)
  - Modified points marked with colored numbers (color = primitive type)
  - Gamma_self markers PINNED at commit time (stay at original position)
  - Watch gamma_self trajectory update in real-time
  - Press Ctrl+S to SAVE (commits all previews to CSV)
  
Phase 1.5 Features:
  ✓ Single perspective (M1) editing
  ✓ Drag primitives (v, r, f, a, S) with Fidelity label
  ✓ Preview (hollow) vs Commit (filled) workflow
  ✓ Click hollow to continue editing
  ✓ Lock/unlock events
  ✓ Auto-mark modified points with numbers
  ✓ Real-time trajectory preview
  ✓ Zoom in/out/reset controls
  ✓ Fixed view mode (preserve zoom during edits)
  ✓ Gamma_self_0 initial position support
  ✓ Save As with new filename (commits previews)
        """
    )
    
    parser.add_argument('csv_file', type=str, 
                       help='Path to CSV file to edit')
    
    args = parser.parse_args()
    
    # Validate file exists
    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        print(f"Error: File not found: {csv_path}", file=sys.stderr)
        sys.exit(1)
    
    # Create and run editor
    editor = InteractiveEditor(args.csv_file)
    editor.run()


if __name__ == '__main__':
    main()
