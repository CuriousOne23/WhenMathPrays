"""
Trajectory panel view - displays gamma_self on complex plane.
"""

import matplotlib.pyplot as plt
import numpy as np


class TrajectoryPanel:
    """
    Panel showing gamma_self trajectory on complex plane.
    
    Displays Ego↔We (horizontal) and Hate↔Love (vertical) axes
    with quadrant labels and trajectory line.
    """
    
    def __init__(self, fig, grid_spec):
        """
        Initialize trajectory panel.
        
        Args:
            fig: Matplotlib figure
            grid_spec: GridSpec cell for this panel
        """
        self.fig = fig
        self.ax = fig.add_subplot(grid_spec)
        
        # View control
        self.fixed_view = False  # If True, don't auto-scale during edits
        self.manual_xlim = None
        self.manual_ylim = None
        self.original_xlim = None  # Store initial view for reset
        self.original_ylim = None
        
        # Marker tracking
        self.committed_markers = {}  # {event_idx: (x, y)}
        self.preview_marker_pos = None  # (x, y) for current preview
        
        # Setup axes
        self.ax.set_xlabel('Ego ← → We', fontsize=10)
        self.ax.set_ylabel('Hate ← → Love', fontsize=10)
        self.ax.set_title('Gamma_Self Trajectory', fontsize=11, fontweight='bold')
        self.ax.grid(True, alpha=0.3)
        # Note: Not using equal aspect to allow flexible y-axis scaling
        
        # Draw quadrant lines
        self.ax.axhline(y=0, color='k', linestyle='-', linewidth=1, alpha=0.4)
        self.ax.axvline(x=0, color='k', linestyle='-', linewidth=1, alpha=0.4)
        
        # Quadrant labels
        label_offset = 0.5
        self.ax.text(label_offset, label_offset, 'Q1', 
                    ha='left', va='bottom', fontsize=9, alpha=0.6, weight='bold')
        self.ax.text(-label_offset, label_offset, 'Q2',
                    ha='right', va='bottom', fontsize=9, alpha=0.6, weight='bold')
        self.ax.text(-label_offset, -label_offset, 'Q3',
                    ha='right', va='top', fontsize=9, alpha=0.6, weight='bold')
        self.ax.text(label_offset, -label_offset, 'Q4',
                    ha='left', va='top', fontsize=9, alpha=0.6, weight='bold')
        
        # Initialize empty trajectory line
        self.trajectory_line, = self.ax.plot([], [], 'b-', linewidth=2, 
                                             label='M1', alpha=0.8)
        self.start_marker, = self.ax.plot([], [], 'go', markersize=10, 
                                          label='Start', zorder=10)
        self.end_marker, = self.ax.plot([], [], 'rs', markersize=10,
                                        label='End', zorder=10)
        
        # Event markers (for modified points)
        self.event_markers, = self.ax.plot([], [], 'o', color='orange',
                                           markersize=5, alpha=0.6, zorder=5,
                                           label='Modified')
        
        # Preview marker (hollow, shown during drag)
        self.preview_marker, = self.ax.plot([], [], 'o', color='orange',
                                            markersize=7, markerfacecolor='none',
                                            markeredgecolor='orange', markeredgewidth=2,
                                            zorder=6, visible=False)
        
        # Computing indicator
        self.computing_text = self.ax.text(0.5, 0.5, 'Computing...',
                                           transform=self.ax.transAxes,
                                           ha='center', va='center',
                                           fontsize=14, color='red',
                                           weight='bold', visible=False,
                                           bbox=dict(boxstyle='round', 
                                                    facecolor='yellow', 
                                                    alpha=0.8))
        
        self.ax.legend(loc='upper right', fontsize=8)
    
    def update_trajectory(self, gamma_x, gamma_y, marked_data=None, pinned_markers=None, preview_gamma=None, preserve_view=False):
        """
        Update trajectory display.
        
        Args:
            gamma_x: Array of real components (Ego↔We axis)
            gamma_y: Array of imaginary components (Hate↔Love axis)
            marked_data: Dict[event_idx, set of primitives] or List[event_idx]
            pinned_markers: List of dicts with 'event_idx', 'primitive', 'x', 'y', 'color', 'label'
            preview_gamma: Tuple (x, y) for preview position marker (hollow)
            preserve_view: If True, keep current view limits
        """
        print(f"\n[TRAJECTORY PANEL] update_trajectory called:")
        print(f"  preserve_view={preserve_view}, fixed_view={self.fixed_view}")
        print(f"  gamma_x range: [{min(gamma_x):.2f}, {max(gamma_x):.2f}]")
        print(f"  gamma_y range: [{min(gamma_y):.2f}, {max(gamma_y):.2f}]")
        print(f"  Final point: ({gamma_x[-1]:.2f}, {gamma_y[-1]:.2f})")
        
        if len(gamma_x) == 0:
            return
        
        # Store for reset_view
        self._last_gamma_x = gamma_x
        self._last_gamma_y = gamma_y
        
        # Store current view if preserving
        if preserve_view or self.fixed_view:
            self.manual_xlim = self.ax.get_xlim()
            self.manual_ylim = self.ax.get_ylim()
        else:
            # Clear manual view to allow auto-scaling
            self.manual_xlim = None
            self.manual_ylim = None
        
        # Update trajectory line
        self.trajectory_line.set_data(gamma_x, gamma_y)
        
        # Update start/end markers
        self.start_marker.set_data([gamma_x[0]], [gamma_y[0]])
        self.end_marker.set_data([gamma_x[-1]], [gamma_y[-1]])
        
        # Clear old annotations - check validity before removal
        if hasattr(self, 'marker_annotations'):
            for ann in self.marker_annotations:
                try:
                    if ann.axes is not None:
                        ann.set_visible(False)
                        ann.remove()
                except:
                    pass  # Annotation already removed or orphaned
            self.marker_annotations = []
        else:
            self.marker_annotations = []
        
        # Display pinned markers (at their original gamma_self positions)
        if pinned_markers:
            print(f"\n=== TRAJECTORY PANEL: Received {len(pinned_markers)} markers ===")
            for m in pinned_markers:
                print(f"  Marker: {m}")
            
            # Group markers by position to offset overlapping labels
            position_groups = {}
            for marker in pinned_markers:
                pos_key = (round(marker['x'], 1), round(marker['y'], 1))
                if pos_key not in position_groups:
                    position_groups[pos_key] = []
                position_groups[pos_key].append(marker)
            
            # Display markers with offset labels for overlaps
            for pos_key, markers in position_groups.items():
                for idx, marker in enumerate(markers):
                    # Offset labels if multiple at same position
                    offset_x = 5 + (idx * 15)  # Shift right for each additional marker
                    offset_y = 5 + (idx * 0)   # Keep same vertical offset
                    
                    # Show event_idx/primitive (e.g., "2/v", "2/r")
                    label = f"{marker['event_idx']}/{marker['primitive']}"
                    
                    ann = self.ax.annotate(
                        label,
                        xy=(marker['x'], marker['y']),
                        xytext=(offset_x, offset_y),
                        textcoords='offset points',
                        fontsize=7,
                        color=marker['color'],
                        weight='bold',
                        bbox=dict(
                            boxstyle='round,pad=0.3',
                            facecolor='white',
                            edgecolor=marker['color'],
                            alpha=0.9,
                            linewidth=1.5
                        )
                    )
                    self.marker_annotations.append(ann)
            
            # Update event markers (small dots at pinned positions)
            marker_xs = [m['x'] for m in pinned_markers]
            marker_ys = [m['y'] for m in pinned_markers]
            self.event_markers.set_data(marker_xs, marker_ys)
        else:
            # No pinned markers
            self.event_markers.set_data([], [])
        
        # Show preview marker if provided (hollow orange)
        if preview_gamma and hasattr(self, 'preview_marker'):
            self.preview_marker.set_data([preview_gamma[0]], [preview_gamma[1]])
            self.preview_marker.set_visible(True)
            self.preview_marker_pos = preview_gamma
        elif hasattr(self, 'preview_marker'):
            self.preview_marker.set_visible(False)
            self.preview_marker_pos = None
        
        # Auto-scale or restore manual view
        if self.manual_xlim and self.manual_ylim:
            print(f"  Using manual view: x={self.manual_xlim}, y={self.manual_ylim}")
            self.ax.set_xlim(self.manual_xlim)
            self.ax.set_ylim(self.manual_ylim)
        else:
            # Auto-scale to fit trajectory with padding
            margin = 2.0
            x_min, x_max = min(gamma_x) - margin, max(gamma_x) + margin
            y_min, y_max = min(gamma_y) - margin, max(gamma_y) + margin
            
            # Ensure axes include origin
            x_min = min(x_min, -1)
            x_max = max(x_max, 1)
            y_min = min(y_min, -1)
            y_max = max(y_max, 1)
            
            print(f"  Auto-scaling view: x=[{x_min:.1f}, {x_max:.1f}], y=[{y_min:.1f}, {y_max:.1f}]")
            self.ax.set_xlim(x_min, x_max)
            self.ax.set_ylim(y_min, y_max)
            
            # Store as original view ONLY on first display (before any edits)
            if self.original_xlim is None and self.original_ylim is None:
                self.original_xlim = (x_min, x_max)
                self.original_ylim = (y_min, y_max)
                print(f"Stored original view: x:[{x_min:.1f}, {x_max:.1f}], y:[{y_min:.1f}, {y_max:.1f}]")
        
        # Redraw
        self.fig.canvas.draw_idle()
    
    def show_computing(self, computing=True):
        """Show/hide 'Computing...' overlay."""
        self.computing_text.set_visible(computing)
        self.fig.canvas.draw_idle()
    
    def zoom_in(self, factor=0.8):
        """Zoom in by reducing axis limits."""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        x_range = (xlim[1] - xlim[0]) * factor / 2
        y_range = (ylim[1] - ylim[0]) * factor / 2
        
        self.ax.set_xlim(x_center - x_range, x_center + x_range)
        self.ax.set_ylim(y_center - y_range, y_center + y_range)
        
        # Store manual limits
        self.manual_xlim = self.ax.get_xlim()
        self.manual_ylim = self.ax.get_ylim()
        self.fixed_view = True
        
        self.fig.canvas.draw_idle()
    
    def zoom_out(self, factor=1.2):
        """Zoom out by expanding axis limits."""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        x_range = (xlim[1] - xlim[0]) * factor / 2
        y_range = (ylim[1] - ylim[0]) * factor / 2
        
        self.ax.set_xlim(x_center - x_range, x_center + x_range)
        self.ax.set_ylim(y_center - y_range, y_center + y_range)
        
        # Store manual limits
        self.manual_xlim = self.ax.get_xlim()
        self.manual_ylim = self.ax.get_ylim()
        self.fixed_view = True
        
        self.fig.canvas.draw_idle()
    
    def reset_view(self):
        """Reset to original full view (when editor first opened)."""
        self.manual_xlim = None
        self.manual_ylim = None
        self.fixed_view = False
        
        # Restore original view if available
        if self.original_xlim and self.original_ylim:
            self.ax.set_xlim(self.original_xlim)
            self.ax.set_ylim(self.original_ylim)
            self.fig.canvas.draw_idle()
            print(f"Reset gamma_self to original view: x:[{self.original_xlim[0]:.1f}, {self.original_xlim[1]:.1f}], y:[{self.original_ylim[0]:.1f}, {self.original_ylim[1]:.1f}]")
        else:
            # Fallback: compute full trajectory view
            gamma_x, gamma_y = self.trajectory_line.get_data()
            
            if len(gamma_x) > 0 and len(gamma_y) > 0:
                margin = 2.0
                x_min, x_max = min(gamma_x) - margin, max(gamma_x) + margin
                y_min, y_max = min(gamma_y) - margin, max(gamma_y) + margin
                
                x_min = min(x_min, -1)
                x_max = max(x_max, 1)
                y_min = min(y_min, -1)
                y_max = max(y_max, 1)
                
                self.ax.set_xlim(x_min, x_max)
                self.ax.set_ylim(y_min, y_max)
                self.fig.canvas.draw_idle()
                print(f"Reset gamma_self view to x:[{x_min:.1f}, {x_max:.1f}], y:[{y_min:.1f}, {y_max:.1f}]")
            else:
                # No data, reset to default
                self.ax.set_xlim(-5, 15)
                self.ax.set_ylim(-5, 30)
                self.fig.canvas.draw_idle()
                print("Reset gamma_self view to default")
    
    def clear(self):
        """Clear trajectory display."""
        self.trajectory_line.set_data([], [])
        self.start_marker.set_data([], [])
        self.end_marker.set_data([], [])
        self.event_markers.set_data([], [])
        self.fig.canvas.draw_idle()
