#!/usr/bin/env python3
"""
Interactive Scenario Editor

Visual diagnostic tool for GRP scenario primitives with real-time
gamma_self trajectory preview.

Usage:
    python tools/interactive_editor.py <csv_file>

Example:
    python tools/interactive_editor.py data/single_dating_to_love_M1.csv

Phase 2 Update:
    Migrated to PySide6 for professional UI framework with native
    toolbars, dialogs, and undo/redo support.
"""

import sys
import argparse
from pathlib import Path
from matplotlib.gridspec import GridSpec

# PySide6 imports (Phase 2)
from PySide6.QtWidgets import QApplication

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.editor.model import EditorModel
from tools.editor.controller import EditorController
from tools.editor.views.primitive_panel import PrimitivePanel
from tools.editor.views.trajectory_panel import TrajectoryPanel
from tools.editor.config import get_config
from tools.editor.qt_window import EditorMainWindow


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
    
    def __init__(self, csv_file: str, qt_app: QApplication):
        """
        Initialize interactive editor.
        
        Args:
            csv_file: Path to CSV file to load
            qt_app: QApplication instance
        """
        self.csv_file = Path(csv_file)
        self.qt_app = qt_app
        
        # Load configuration (with fallback to defaults)
        config = get_config()
        self.LAYOUT = config.get_layout()
        
        # Create Qt main window (Phase 2)
        self.window = EditorMainWindow(self.csv_file)
        self.fig = self.window.fig  # Use figure from Qt window
        
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
            trajectory_panel=self.trajectory_panel,
            undo_stack=self.window.undo_stack
        )

        # Load scenario (structured: Event/Marker)
        self.controller.load_scenario(str(self.csv_file))

        # Track last mouse position for context-aware zoom
        self.last_mouse_axes = None
        self.fig.canvas.mpl_connect('motion_notify_event', self._on_mouse_move)
        
        # Set up callbacks AFTER panels and controller are initialized
        self.window.save_callback = self._handle_save_request
        self.window.cleanup_callback = self._handle_cleanup
        
        # Connect zoom toolbar buttons (will zoom both panels)
        self.window.zoom_in_action.triggered.connect(self._handle_zoom_in)
        self.window.zoom_out_action.triggered.connect(self._handle_zoom_out)
        self.window.zoom_reset_action.triggered.connect(self._handle_zoom_reset)
        
        # Connect keyboard shortcuts and scroll wheel
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
        self.fig.canvas.mpl_connect('scroll_event', self._on_scroll)
        self.fig.canvas.mpl_connect('button_press_event', self._on_mouse_press)
        self.fig.canvas.mpl_connect('button_release_event', self._on_mouse_release)
        
        # Pan state
        self.pan_active = False
        self.pan_start = None
        self.pan_axes = None
    
    def _handle_save_request(self, options: dict):
        """
        Handle save request from Qt toolbar.
        
        Args:
            options: Dict with 'csv' and 'png' boolean flags
        """
        # Commit any preview changes first
        self.controller.commit_changes()
        
        save_csv = options.get('csv', True)
        save_png = options.get('png', False)
        
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
            self.window.show_message(f"Saved CSV to: {csv_path}")
            # Update self.csv_file to point to the new file for future saves
            self.csv_file = csv_path
            self.window.update_window_title(self.csv_file)
        
        # Save PNG plots if requested (combined primitives + trajectory)
        if save_png:
            self._save_combined_plot(str(combined_png))
            self.window.show_message(f"Saved combined plot to: {combined_png}")
        
        if not save_csv and not save_png:
            self.window.show_message("No save operation performed", 'warning')
    
    def _on_mouse_move(self, event):
        """Track mouse position for context-aware toolbar zoom and handle panning."""
        if event.inaxes:
            self.last_mouse_axes = event.inaxes
        
        # Handle pan dragging
        if self.pan_active and event.inaxes == self.pan_axes and self.pan_start:
            # Calculate distance moved in data coordinates
            dx = self.pan_start[0] - event.xdata
            dy = self.pan_start[1] - event.ydata
            
            # Get current limits
            xlim = self.pan_axes.get_xlim()
            ylim = self.pan_axes.get_ylim()
            
            # Pan by shifting limits
            self.pan_axes.set_xlim(xlim[0] + dx, xlim[1] + dx)
            self.pan_axes.set_ylim(ylim[0] + dy, ylim[1] + dy)
            
            # Update stored manual limits
            if self.pan_axes == self.controller.trajectory_panel.ax:
                self.controller.trajectory_panel.manual_xlim = self.pan_axes.get_xlim()
                self.controller.trajectory_panel.manual_ylim = self.pan_axes.get_ylim()
            else:
                # Check which primitive subplot
                for prim, ax in self.controller.primitive_panel.axes.items():
                    if ax == self.pan_axes:
                        self.controller.primitive_panel.manual_xlim[prim] = self.pan_axes.get_xlim()
                        break
            
            self.fig.canvas.draw_idle()
    
    def _on_mouse_press(self, event):
        """Start panning on middle or right-click in empty space."""
        # Right-click (button 3) or middle-click (button 2) to pan
        if event.button in [2, 3] and event.inaxes and event.xdata and event.ydata:
            # Check if clicking on a marker in primitive panel
            if event.inaxes in self.controller.primitive_panel.axes.values():
                # Check if we're clicking on a draggable point
                for dp in self.controller.primitive_panel.draggable_points.values():
                    if dp.ax == event.inaxes:
                        contains, _ = dp.point.contains(event)
                        if contains:
                            return  # Don't pan, let marker handle it
            
            # Start panning
            self.pan_active = True
            self.pan_start = (event.xdata, event.ydata)
            self.pan_axes = event.inaxes
            self.fig.canvas.set_cursor(1)  # Hand cursor
    
    def _on_mouse_release(self, event):
        """Stop panning."""
        if self.pan_active:
            self.pan_active = False
            self.pan_start = None
            self.pan_axes = None
            self.fig.canvas.set_cursor(0)  # Default cursor
    
    def _on_scroll(self, event):
        """Handle scroll wheel zoom - zoom in/out centered on cursor position."""
        if not event.inaxes:
            return
        
        # Determine zoom factor based on scroll direction
        # Scroll up (event.button == 'up') = zoom in
        # Scroll down (event.button == 'down') = zoom out
        if event.button == 'up':
            zoom_factor = 0.8  # Zoom in to 80% of current range
        elif event.button == 'down':
            zoom_factor = 1.25  # Zoom out to 125% of current range
        else:
            return
        
        # Get cursor position in data coordinates
        x_cursor, y_cursor = event.xdata, event.ydata
        
        # Check if scroll is in gamma_self panel
        if event.inaxes == self.controller.trajectory_panel.ax:
            ax = self.controller.trajectory_panel.ax
            
            # Get current limits
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            
            # Calculate new limits centered on cursor
            x_range = (xlim[1] - xlim[0]) * zoom_factor
            y_range = (ylim[1] - ylim[0]) * zoom_factor
            
            # Calculate cursor position as fraction of current range
            x_frac = (x_cursor - xlim[0]) / (xlim[1] - xlim[0])
            y_frac = (y_cursor - ylim[0]) / (ylim[1] - ylim[0])
            
            # Set new limits preserving cursor position
            new_xlim = (x_cursor - x_range * x_frac, x_cursor + x_range * (1 - x_frac))
            new_ylim = (y_cursor - y_range * y_frac, y_cursor + y_range * (1 - y_frac))
            
            ax.set_xlim(new_xlim)
            ax.set_ylim(new_ylim)
            
            # Store manual zoom state
            self.controller.trajectory_panel.manual_xlim = new_xlim
            self.controller.trajectory_panel.manual_ylim = new_ylim
            
            self.fig.canvas.draw_idle()
            
        else:
            # Scroll is in primitive panel - find which subplot
            for prim, ax in self.controller.primitive_panel.axes.items():
                if ax == event.inaxes:
                    # Get current limits
                    xlim = ax.get_xlim()
                    ylim = ax.get_ylim()
                    
                    # Calculate new limits centered on cursor
                    x_range = (xlim[1] - xlim[0]) * zoom_factor
                    y_range = (ylim[1] - ylim[0]) * zoom_factor
                    
                    # Calculate cursor position as fraction of current range
                    x_frac = (x_cursor - xlim[0]) / (xlim[1] - xlim[0])
                    y_frac = (y_cursor - ylim[0]) / (ylim[1] - ylim[0])
                    
                    # Set new limits preserving cursor position
                    new_xlim = (x_cursor - x_range * x_frac, x_cursor + x_range * (1 - x_frac))
                    new_ylim = (y_cursor - y_range * y_frac, y_cursor + y_range * (1 - y_frac))
                    
                    ax.set_xlim(new_xlim)
                    ax.set_ylim(new_ylim)
                    
                    # Store manual zoom state for this primitive
                    self.controller.primitive_panel.manual_xlim[prim] = new_xlim
                    
                    self.fig.canvas.draw_idle()
                    break
    
    def _handle_zoom_in(self):
        """Handle zoom in toolbar button - zoom all panels uniformly."""
        self.controller.trajectory_panel.zoom_in()
        self.controller.primitive_panel.zoom_in()
        self.window.show_message("Zoomed in (all panels)")
    
    def _handle_zoom_out(self):
        """Handle zoom out toolbar button - zoom all panels uniformly."""
        self.controller.trajectory_panel.zoom_out()
        self.controller.primitive_panel.zoom_out()
        self.window.show_message("Zoomed out (all panels)")
    
    def _handle_zoom_reset(self):
        """Handle reset view toolbar button - reset both panels."""
        self.controller.trajectory_panel.reset_view()
        self.controller.primitive_panel.reset_view()
        self.controller.primitive_panel.clear_readout()
        self.window.show_message("Reset all views")
    
    def _handle_cleanup(self):
        """Handle application cleanup before exit."""
        if hasattr(self, 'controller'):
            self.controller.cleanup()
    
    def _save_combined_plot(self, filepath: str):
        """Save a combined PNG with primitives on the left and trajectory on the right.
        
        Args:
            filepath: Output PNG file path
        """
        import matplotlib.pyplot as plt
        from matplotlib.gridspec import GridSpec
        
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
            self.window.show_message(f"Fixed view: {status}")
    
    def _edit_gamma_self_0(self):
        """Edit initial gamma_self position."""
        from PySide6.QtWidgets import QInputDialog
        
        current = self.controller.model.gamma_self_0
        
        # Get real part
        real_part, ok = QInputDialog.getDouble(
            self.window,
            "Edit Gamma_self_0",
            f"Enter REAL part (Ego↔We axis):\n\nCurrent: {current.real:+.1f}{current.imag:+.1f}j\n\nExamples:\n  Strangers: 0\n  Friends: +5\n  Exes (hurt): -5",
            value=current.real,
            decimals=1
        )
        
        if not ok:
            return
        
        # Get imaginary part
        imag_part, ok = QInputDialog.getDouble(
            self.window,
            "Edit Gamma_self_0",
            f"Enter IMAGINARY part (Hate↔Love axis):\n\nCurrent: {current.real:+.1f}{current.imag:+.1f}j\n\nExamples:\n  Strangers: 0\n  Friends: +8\n  Exes (hurt): -3",
            value=current.imag,
            decimals=1
        )
        
        if not ok:
            return
        
        # Update gamma_self_0
        self.controller.model.gamma_self_0 = complex(real_part, imag_part)
        
        # Recompute trajectory from new starting point
        self.controller._recompute_trajectory_immediate()
        
        self.window.show_message(f"Gamma_self_0 set to {real_part:+.1f}{imag_part:+.1f}j")
    
    def _save_as(self):
        """Open Save As dialog and save CSV."""
        from PySide6.QtWidgets import QFileDialog
        
        # Suggest filename with _modified suffix
        original_stem = self.csv_file.stem
        original_parent = self.csv_file.parent
        suggested_name = original_parent / f"{original_stem}_modified.csv"
        
        # Open Qt file dialog
        filepath, _ = QFileDialog.getSaveFileName(
            self.window,
            "Save Modified Scenario",
            str(suggested_name),
            "CSV files (*.csv);;All files (*.*)"
        )
        
        if filepath:
            self.controller.save_scenario(filepath)
            self.window.show_message(f"Saved to: {filepath}")
    
    def run(self):
        """Show UI and enter Qt event loop."""
        self.window.show()
        return self.qt_app.exec()


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
    
    # Create Qt application (Phase 2)
    app = QApplication(sys.argv)
    app.setApplicationName('GRP Interactive Scenario Editor')
    
    # Create and run editor
    editor = InteractiveEditor(args.csv_file, app)
    sys.exit(editor.run())


if __name__ == '__main__':
    main()
