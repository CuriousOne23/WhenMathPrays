#!/usr/bin/env python3
"""
Interactive Scenario Editor

Visual diagnostic tool for GRP scenario primitives with real-time
gamma_self trajectory preview.

Usage:
    python tools/interactive_editor.py <csv_file>

Example:
    python tools/interactive_editor.py data/single_dating_to_love_M1.csv

Layout System:
    The UI layout is controlled by the LAYOUT dictionary in InteractiveEditor class.
    All positioning constants are defined there for easy adjustment:
    
    - margin_left: Left edge space (for primitive readout gauge)
    - margin_right: Right edge space
    - margin_top: Top edge space (for Save button area)
    - margin_bottom: Bottom edge space
    - panel_gap: Horizontal space between primitive and gamma_self panels
    - subplot_gap: Vertical space between primitive subplots
    - save_button_*: Position and size of Save button
    - save_info_*: Position of instruction text
    
    To adjust layout:
    1. Modify values in LAYOUT dictionary
    2. All derived positions update automatically
    3. No need to hunt for magic numbers throughout the code
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
    
    # Layout constants for easy adjustment
    LAYOUT = {
        # Main margins (figure edges)
        'margin_left': 0.14,      # Space for primitive readout gauge
        'margin_right': 0.02,     # Right edge margin
        'margin_top': 0.08,       # Space for Save button and title
        'margin_bottom': 0.08,    # Bottom edge margin
        
        # Panel spacing
        'panel_gap': 0.35,        # Horizontal gap between primitive and gamma_self panels
        'subplot_gap': 0.3,       # Vertical gap between primitive subplots
        
        # Primitive readout gauge (in axes transform coordinates, relative to fidelity plot)
        'primitive_gauge_x': -0.18,  # Negative = left of plot, 0 = left edge, 1 = right edge
        'primitive_gauge_y': 0.5,    # 0 = bottom, 0.5 = middle, 1 = top
        
        # Trajectory readout (in axes transform coordinates, relative to gamma_self plot)
        'trajectory_readout_x': -0.15,  # Position left of Y axis
        'trajectory_readout_y': 0.5,    # Middle vertically
        
        # Header elements (in figure coordinates, 0-1)
        'save_button_left': 0.16,     # Left side, indented from primitive left edge
        'save_button_bottom': 0.96,
        'save_button_width': 0.06,
        'save_button_height': 0.035,
        'save_info_x': 0.92,          # Position of instruction text (will be calculated relative to button)
        'save_info_y': 0.965,
    }
    
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
        gs = GridSpec(
            5, 2, 
            figure=self.fig, 
            hspace=self.LAYOUT['subplot_gap'], 
            wspace=self.LAYOUT['panel_gap'],
            left=self.LAYOUT['margin_left'], 
            right=1.0 - self.LAYOUT['margin_right'], 
            top=1.0 - self.LAYOUT['margin_top'], 
            bottom=self.LAYOUT['margin_bottom']
        )
        
        # Initialize model (structured: uses Event/Marker)
        self.model = EditorModel()

        # Initialize views (pass structured callbacks)
        self.primitive_panel = PrimitivePanel(
            fig=self.fig,
            grid_spec=gs[:, 0],
            on_primitive_changed=self._on_primitive_changed,
            on_lock_toggle=self._on_lock_toggle,
            on_primitive_preview=self._on_primitive_preview,
            on_primitive_reset=self._on_primitive_reset,
            layout=self.LAYOUT  # Pass layout config
        )

        self.trajectory_panel = TrajectoryPanel(
            fig=self.fig,
            grid_spec=gs[:, 1],
            layout=self.LAYOUT  # Pass layout config
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
        
        # Disable the toolbar's save button (we have our own)
        self._disable_toolbar_save_button()
    
    def _disable_toolbar_save_button(self):
        """Disable the matplotlib toolbar's save button."""
        toolbar = self.fig.canvas.toolbar
        if toolbar:
            # Remove save button from toolbar
            try:
                # For NavigationToolbar2Tk (Tkinter backend)
                if hasattr(toolbar, '_buttons'):
                    # Find and disable the save button
                    for name, button in toolbar._buttons.items():
                        if name == 'Save':
                            button.config(state='disabled')
                # Alternative: hide it completely by removing from toolbar
                # This works for most backends
                toolbar.children['!button3'].config(state='disabled')  # Save is typically the 3rd button
            except:
                # If disabling fails, just continue - not critical
                pass
    
    def _setup_toolbar(self):
        """Setup custom toolbar buttons."""
        toolbar = self.fig.canvas.toolbar
        if toolbar:
            # Add Save button to the toolbar
            import matplotlib
            from matplotlib.widgets import Button
            
            # Place button in a new axes on the figure
            save_ax = self.fig.add_axes([
                self.LAYOUT['save_button_left'], 
                self.LAYOUT['save_button_bottom'], 
                self.LAYOUT['save_button_width'], 
                self.LAYOUT['save_button_height']
            ])
            self._save_button = Button(save_ax, 'Save', color='#e0e0e0', hovercolor='#b0ffb0')
            self._save_button.on_clicked(self._on_save_button)
            save_ax._button = self._save_button  # Prevent garbage collection
            
            # Add informational text about modifier keys (to the right of Save button)
            # Calculate position to the right of the button
            info_x = self.LAYOUT['save_button_left'] + self.LAYOUT['save_button_width'] + 0.005
            info_text = self.fig.text(
                info_x, 
                self.LAYOUT['save_info_y'], 
                'Click=CSV | Shift=PNG | Ctrl=Both', 
                fontsize=8, color='#666666', ha='left', va='center'  # Changed ha to 'left'
            )
            self._save_info_text = info_text

    def _on_save_button(self, event):
        """Handle Save button click: commit previews and save based on modifier keys.
        
        Click = CSV only
        Shift+Click = PNG only
        Ctrl+Click = Both CSV and PNG
        """
        self.controller.commit_changes()
        
        # Detect modifier keys from the mouse event
        # In matplotlib button events, we need to check the canvas's current key modifiers
        import matplotlib.backend_bases as backend_bases
        guiEvent = event.guiEvent if hasattr(event, 'guiEvent') else None
        
        save_csv = True
        save_png = False
        
        # Check for modifier keys
        if guiEvent:
            # Check if Shift or Ctrl is pressed
            if hasattr(guiEvent, 'keysym'):
                # Tkinter event
                shift = bool(guiEvent.state & 0x0001)
                ctrl = bool(guiEvent.state & 0x0004)
            elif hasattr(guiEvent, 'modifiers'):
                # Qt event
                from matplotlib.backend_bases import MouseEvent
                shift = 'shift' in str(guiEvent.modifiers()).lower()
                ctrl = 'control' in str(guiEvent.modifiers()).lower() or 'ctrl' in str(guiEvent.modifiers()).lower()
            else:
                shift = False
                ctrl = False
            
            if ctrl:
                # Ctrl = Both
                save_csv = True
                save_png = True
            elif shift:
                # Shift = PNG only
                save_csv = False
                save_png = True
            # else: default is CSV only
        
        # Determine if current file is the original (in data/ and does not end with _modified.csv)
        original = (
            self.csv_file.parent.name == 'data' and
            not self.csv_file.stem.endswith('_modified')
        )
        
        # Determine base name for output files (without _modified suffix and without extension)
        if self.csv_file.stem.endswith('_modified'):
            base_name = self.csv_file.stem[:-9]  # Remove '_modified'
        else:
            base_name = self.csv_file.stem
        
        # Output directory is data/
        data_dir = self.csv_file.parent if self.csv_file.parent.name == 'data' else self.csv_file.parent.parent / 'data'
        
        # Determine output paths
        csv_path = data_dir / f"{base_name}_modified.csv"
        combined_png = data_dir / f"{base_name}_modified.png"
        
        # Save CSV if requested
        if save_csv:
            self.controller.save_scenario(str(csv_path))
            print(f"Saved CSV to: {csv_path}")
            # Update self.csv_file to point to the new file for future saves
            self.csv_file = csv_path
            self.fig.canvas.manager.set_window_title(
                f'Interactive Scenario Editor - {self.csv_file.name}')
        
        # Save PNG plots if requested (combined primitives + trajectory)
        if save_png:
            self._save_combined_plot(str(combined_png))
            print(f"Saved combined plot to: {combined_png}")
        
        if not save_csv and not save_png:
            print("No save operation performed.")
    
    def _save_combined_plot(self, filepath: str):
        """Save a combined PNG with primitives on the left and trajectory on the right.
        
        Args:
            filepath: Output PNG file path
        """
        # Create a new figure with the same layout as the main figure
        save_fig = plt.figure(figsize=(14, 8))
        gs = GridSpec(5, 2, figure=save_fig, hspace=0.3, wspace=0.3,
                     left=0.08, right=0.95, top=0.94, bottom=0.08)
        
        # Copy primitive plots (left column)
        for i, prim in enumerate(self.primitive_panel.PRIMITIVE_NAMES):
            ax = save_fig.add_subplot(gs[i, 0])
            
            # Copy the line data
            if prim in self.primitive_panel.lines:
                line = self.primitive_panel.lines[prim]
                xdata, ydata = line.get_data()
                ax.plot(xdata, ydata, color=self.primitive_panel.PRIMITIVE_COLORS[prim], linewidth=2)
            
            # Copy markers (both baseline and modified)
            for (event_idx, p), marker in self.primitive_panel.original_markers.items():
                if p == prim and marker.axes == self.primitive_panel.axes[prim]:
                    mx, my = marker.get_data()
                    ax.plot(mx, my, marker='o', color=self.primitive_panel.PRIMITIVE_COLORS[prim],
                           markersize=8, markeredgewidth=1.5, markeredgecolor='black',
                           linestyle='none')
            
            for (event_idx, p), dp in self.primitive_panel.draggable_points.items():
                if p == prim:
                    ax.plot([dp.x], [dp.y], marker='o', color=self.primitive_panel.PRIMITIVE_COLORS[prim],
                           markersize=8, markerfacecolor='white', markeredgewidth=1.5,
                           markeredgecolor=self.primitive_panel.PRIMITIVE_COLORS[prim], linestyle='none')
            
            # Copy axis properties
            ax.set_ylabel(self.primitive_panel.PRIMITIVE_LABELS[prim], fontsize=10, fontweight='bold')
            ax.set_ylim(self.primitive_panel.axes[prim].get_ylim())
            ax.set_xlim(self.primitive_panel.axes[prim].get_xlim())
            ax.grid(True, alpha=0.3)
            
            if i == 4:  # Last subplot
                ax.set_xlabel('Time', fontsize=10)
        
        # Copy trajectory plot (right column, spanning all rows)
        ax_traj = save_fig.add_subplot(gs[:, 1])
        
        # Copy the trajectory line
        xdata, ydata = self.trajectory_panel.trajectory_line.get_data()
        ax_traj.plot(xdata, ydata, color='#1f77b4', linewidth=2, alpha=0.7, label='γ_self trajectory')
        
        # Copy start/end markers
        start_x, start_y = self.trajectory_panel.start_marker.get_data()
        if len(start_x) > 0:
            ax_traj.plot(start_x, start_y, marker='o', color='green', markersize=12,
                   markeredgewidth=2, markeredgecolor='darkgreen', label='Start', linestyle='none')
        
        end_x, end_y = self.trajectory_panel.end_marker.get_data()
        if len(end_x) > 0:
            ax_traj.plot(end_x, end_y, marker='s', color='red', markersize=12,
                   markeredgewidth=2, markeredgecolor='darkred', label='End', linestyle='none')
        
        # Copy event markers
        event_x, event_y = self.trajectory_panel.event_markers.get_data()
        if len(event_x) > 0:
            ax_traj.plot(event_x, event_y, marker='o', color='orange', markersize=8,
                   markeredgewidth=1.5, markeredgecolor='darkorange', linestyle='none')
        
        # Copy annotations
        if hasattr(self.trajectory_panel, 'marker_annotations'):
            for ann in self.trajectory_panel.marker_annotations:
                if ann.axes == self.trajectory_panel.ax:
                    ax_traj.annotate(
                        ann.get_text(),
                        xy=ann.xy,
                        xytext=ann.xyann,
                        textcoords=ann.anncoords,
                        fontsize=7,
                        color=ann.get_color(),
                        weight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                edgecolor=ann.get_color(), alpha=0.9, linewidth=1.5)
                    )
        
        # Copy axis properties
        ax_traj.set_xlabel('Re(γ_self) — Ego ← → We', fontsize=12, fontweight='bold')
        ax_traj.set_ylabel('Im(γ_self) — Hate ← → Love', fontsize=12, fontweight='bold')
        ax_traj.set_title('Gamma Self Trajectory (γ_self)', fontsize=14, fontweight='bold')
        ax_traj.set_xlim(self.trajectory_panel.ax.get_xlim())
        ax_traj.set_ylim(self.trajectory_panel.ax.get_ylim())
        ax_traj.grid(True, alpha=0.3)
        ax_traj.axhline(y=0, color='k', linewidth=0.5, alpha=0.5)
        ax_traj.axvline(x=0, color='k', linewidth=0.5, alpha=0.5)
        ax_traj.legend(loc='upper left', fontsize=10)
        
        # Save and close
        save_fig.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close(save_fig)

    
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
            # Clear readouts as well
            self.controller.primitive_panel.clear_readout()
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
