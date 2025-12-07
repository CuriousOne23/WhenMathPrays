"""
Trajectory panel view - displays gamma_self on complex plane.
"""

import matplotlib.pyplot as plt
import numpy as np
from .canvas_utils import force_canvas_draw


class TrajectoryPanel:
    """
    Panel showing gamma_self trajectory on complex plane.
    
    Displays Ego↔We (horizontal) and Hate↔Love (vertical) axes
    with quadrant labels and trajectory line.
    """
    
    def __init__(self, fig, grid_spec, layout=None):
        """
        Initialize trajectory panel.
        
        Args:
            fig: Matplotlib figure
            grid_spec: GridSpec cell for this panel
            layout: Layout configuration dict (optional)
        """
        self.fig = fig
        self.ax = fig.add_subplot(grid_spec)
        self.layout = layout or {}  # Store layout config
        
        # View control
        self.fixed_view = False  # If True, don't auto-scale during edits
        self.manual_xlim = None
        self.manual_ylim = None
        self.original_xlim = None  # Store initial view for reset
        self.original_ylim = None
        
        # Marker tracking
        self.committed_markers = {}  # {event_idx: (x, y)}
        self.preview_marker_pos = None  # (x, y) for current preview
        self.insertion_lines = []  # Vertical lines marking inserted events
        
        # Track if readout is being used for drag preview (don't let click handler override)
        self.readout_locked_for_drag = False
        
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
        
        # Insertion point markers (small gray diamonds at inserted event positions)
        self.insertion_markers, = self.ax.plot([], [], 'D', color='gray',
                                               markersize=4, alpha=0.7, zorder=4,
                                               label='Inserted')
        
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
        
        # Position readout display - positioned at bottom-left corner overlapping the plot
        self.position_readout = self.ax.text(
            0.02, 0.02, '',  # Bottom-left corner inside the plot
            transform=self.ax.transAxes,  # Use axes transform coordinates
            fontsize=10,
            verticalalignment='bottom',
            horizontalalignment='left',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', edgecolor='black', alpha=0.8),
            visible=False,
            zorder=100  # Draw on top
        )
    
    def update_gamma_self_readout(self, x, y):
        """Update gamma_self readout display with complex plane coordinates."""
        print(f"[GAMMA_SELF READOUT] Showing: x={x:.2f}, y={y:.2f}")
        # Lock readout to prevent click handler from overriding position
        self.readout_locked_for_drag = True
        # Set position at bottom-left corner
        self.position_readout.set_position((0.02, 0.02))
        self.position_readout.set_text(f'γ_self\n{x:.2f} + {y:.2f}i')
        # Ensure alignment is correct
        self.position_readout.set_horizontalalignment('left')
        self.position_readout.set_verticalalignment('bottom')
        self.position_readout.set_visible(True)
        force_canvas_draw(self.fig.canvas)
    
    def clear_gamma_self_readout(self):
        """Clear gamma_self readout display."""
        print(f"[GAMMA_SELF READOUT] Clearing")
        self.readout_locked_for_drag = False
        self.position_readout.set_visible(False)
        force_canvas_draw(self.fig.canvas)
        
        # Connect click event
        self.fig.canvas.mpl_connect('button_press_event', self._on_click)
        self.fig.canvas.mpl_connect('button_release_event', self._on_release)
        self._click_pos = None  # Store position on press
        
        self.ax.legend(loc='upper right', fontsize=8)
    
    def update_trajectory(self, gamma_x, gamma_y, marked_data=None, pinned_markers=None, preview_gamma=None, preserve_view=False, inserted_event_times=None, inserted_events=None):
        """
        Update trajectory display.
        
        Args:
            gamma_x: Array of real components (Ego↔We axis)
            gamma_y: Array of imaginary components (Hate↔Love axis)
            marked_data: Dict[event_idx, set of primitives] or List[event_idx]
            pinned_markers: List of marker dicts with 'event_idx', 'primitive', 'x', 'y', 'color', 'label'
            preview_gamma: (x, y) tuple for live-drag preview marker
            preserve_view: If True, maintain current zoom/pan
            inserted_event_times: List of time values where events were inserted (deprecated)
            inserted_events: List of dicts with 'index', 'time', 'x', 'y' for inserted events
        """
        if len(gamma_x) == 0:
            return
        
        # Store for reset_view
        self._last_gamma_x = gamma_x
        self._last_gamma_y = gamma_y
        
        # Handle view preservation logic
        if preserve_view or self.fixed_view:
            # Preserve current view (store if not already stored)
            if not self.manual_xlim or not self.manual_ylim:
                self.manual_xlim = self.ax.get_xlim()
                self.manual_ylim = self.ax.get_ylim()
        # If user has manually zoomed (via scroll wheel), keep that zoom
        # Don't clear manual zoom unless explicitly resetting view
        elif not self.manual_xlim and not self.manual_ylim:
            # No manual zoom exists and not preserving, so allow auto-scaling
            pass
        # else: manual zoom exists, keep it
        
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
            
            # Add label for preview marker
            preview_label = f"γ: {preview_gamma[0]:.1f} + {preview_gamma[1]:.1f}i"
            preview_ann = self.ax.annotate(
                preview_label,
                xy=(preview_gamma[0], preview_gamma[1]),
                xytext=(8, 8),
                textcoords='offset points',
                fontsize=8,
                color='orange',
                weight='bold',
                bbox=dict(
                    boxstyle='round,pad=0.4',
                    facecolor='white',
                    edgecolor='orange',
                    alpha=0.95,
                    linewidth=2
                )
            )
            self.marker_annotations.append(preview_ann)
        elif hasattr(self, 'preview_marker'):
            self.preview_marker.set_visible(False)
            self.preview_marker_pos = None
        
        # Auto-scale or restore manual view
        if self.manual_xlim and self.manual_ylim:
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
            
            self.ax.set_xlim(x_min, x_max)
            self.ax.set_ylim(y_min, y_max)
            
            # Store as original view ONLY on first display (before any edits)
            if self.original_xlim is None and self.original_ylim is None:
                self.original_xlim = (x_min, x_max)
                self.original_ylim = (y_min, y_max)
        
        # Draw markers for inserted events
        self._update_insertion_markers(inserted_events)
        
        # Use non-blocking draw for better performance
        self.fig.canvas.draw_idle()
    
    def _update_insertion_markers(self, inserted_events):
        """
        Mark trajectory points corresponding to inserted events with black diamonds and time labels.
        
        Args:
            inserted_events: List of dicts with 'index', 'time', 'x', 'y'
        """
        # Clear old annotations
        if hasattr(self, 'insertion_annotations'):
            for ann in self.insertion_annotations:
                try:
                    if ann.axes is not None:
                        ann.remove()
                except:
                    pass
        self.insertion_annotations = []
        
        if not inserted_events or len(inserted_events) == 0:
            self.insertion_markers.set_data([], [])
            return
        
        # Collect marker positions
        marker_x = [evt['x'] for evt in inserted_events]
        marker_y = [evt['y'] for evt in inserted_events]
        
        # Draw diamond markers
        self.insertion_markers.set_data(marker_x, marker_y)
        self.insertion_markers.set_color('black')
        self.insertion_markers.set_markersize(6)
        self.insertion_markers.set_alpha(0.8)
        
        # Add time labels to the right of each marker
        for evt in inserted_events:
            # Format time with appropriate decimals
            time_val = evt['time']
            if time_val == int(time_val):
                time_label = f"{int(time_val)}"
            else:
                time_label = f"{time_val:.2f}"
            
            ann = self.ax.annotate(
                time_label,
                xy=(evt['x'], evt['y']),
                xytext=(8, 0),  # 8 points to the right
                textcoords='offset points',
                fontsize=8,
                color='black',
                weight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black', alpha=0.7),
                zorder=10
            )
            self.insertion_annotations.append(ann)
    
    def _update_insertion_lines(self, inserted_times, gamma_x, gamma_y):
        """
        Deprecated: Now using _update_insertion_markers instead.
        """
        pass
    
    def show_computing(self, computing=True):
        """Show/hide 'Computing...' overlay."""
        self.computing_text.set_visible(computing)
        force_canvas_draw(self.fig.canvas)
    
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
        
        force_canvas_draw(self.fig.canvas)
    
    def zoom_out(self, factor=1.2):
        """Zoom out by expanding axis limits."""
        # Initialize manual limits if not set (first zoom_out without zoom_in)
        if self.manual_xlim is None or self.manual_ylim is None:
            self.manual_xlim = self.ax.get_xlim()
            self.manual_ylim = self.ax.get_ylim()
        
        xlim = self.manual_xlim
        ylim = self.manual_ylim
        
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
        
        force_canvas_draw(self.fig.canvas)
    
    def reset_view(self):
        """Reset to original full view (when editor first opened)."""
        self.manual_xlim = None
        self.manual_ylim = None
        self.fixed_view = False
        
        # Restore original view if available
        if self.original_xlim and self.original_ylim:
            self.ax.set_xlim(self.original_xlim)
            self.ax.set_ylim(self.original_ylim)
            force_canvas_draw(self.fig.canvas)
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
                force_canvas_draw(self.fig.canvas)
                print(f"Reset gamma_self view to x:[{x_min:.1f}, {x_max:.1f}], y:[{y_min:.1f}, {y_max:.1f}]")
            else:
                # No data, reset to default
                self.ax.set_xlim(-5, 15)
                self.ax.set_ylim(-5, 30)
                force_canvas_draw(self.fig.canvas)
                print("Reset gamma_self view to default")
    
    def clear(self):
        """Clear trajectory display."""
        self.trajectory_line.set_data([], [])
        self.start_marker.set_data([], [])
        self.end_marker.set_data([], [])
        self.event_markers.set_data([], [])
        force_canvas_draw(self.fig.canvas)
    
    def save_plot(self, filepath: str):
        """Save the trajectory panel plot to a PNG file.
        
        Args:
            filepath: Output PNG file path
        """
        # Create a new figure with just the trajectory plot
        save_fig = plt.figure(figsize=(10, 10))
        ax = save_fig.add_subplot(111)
        
        # Copy the trajectory line
        xdata, ydata = self.trajectory_line.get_data()
        ax.plot(xdata, ydata, color='#1f77b4', linewidth=2, alpha=0.7, label='γ_self trajectory')
        
        # Copy start/end markers
        start_x, start_y = self.start_marker.get_data()
        if len(start_x) > 0:
            ax.plot(start_x, start_y, marker='o', color='green', markersize=12,
                   markeredgewidth=2, markeredgecolor='darkgreen', label='Start', linestyle='none')
        
        end_x, end_y = self.end_marker.get_data()
        if len(end_x) > 0:
            ax.plot(end_x, end_y, marker='s', color='red', markersize=12,
                   markeredgewidth=2, markeredgecolor='darkred', label='End', linestyle='none')
        
        # Copy event markers (pinned positions)
        event_x, event_y = self.event_markers.get_data()
        if len(event_x) > 0:
            ax.plot(event_x, event_y, marker='o', color='orange', markersize=8,
                   markeredgewidth=1.5, markeredgecolor='darkorange', linestyle='none')
        
        # Copy annotations (marker labels)
        if hasattr(self, 'marker_annotations'):
            for ann in self.marker_annotations:
                if ann.axes == self.ax:
                    # Recreate annotation on new axes
                    ax.annotate(
                        ann.get_text(),
                        xy=ann.xy,
                        xytext=ann.xyann,
                        textcoords=ann.anncoords,
                        fontsize=ann.get_fontsize(),
                        color=ann.get_color(),
                        weight=ann.get_weight(),
                        bbox=ann.get_bbox_patch().get_boxstyle() if ann.get_bbox_patch() else None
                    )
        
        # Copy axis properties
        ax.set_xlabel('Re(γ_self) — Ego ← → We', fontsize=12, fontweight='bold')
        ax.set_ylabel('Im(γ_self) — Hate ← → Love', fontsize=12, fontweight='bold')
        ax.set_title('Gamma Self Trajectory (γ_self)', fontsize=14, fontweight='bold')
        ax.set_xlim(self.ax.get_xlim())
        ax.set_ylim(self.ax.get_ylim())
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linewidth=0.5, alpha=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5, alpha=0.5)
        ax.legend(loc='upper left', fontsize=10)
        
        save_fig.tight_layout()
        save_fig.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close(save_fig)
    
    def _on_click(self, event):
        """Handle mouse button press to record position."""
        if event.button == 1 and event.inaxes == self.ax:  # Left click in trajectory axes
            self._click_pos = (event.xdata, event.ydata)
    
    def _on_release(self, event):
        """Handle mouse button release to update gamma_self gauge."""
        # Don't override position if readout is locked for drag updates
        if self.readout_locked_for_drag:
            self._click_pos = None
            return
            
        if event.button == 1 and event.inaxes == self.ax and self._click_pos:  # Left click release
            # Only update if release is in same axes and close to press position
            if event.xdata is not None and event.ydata is not None:
                # Update gamma_self gauge with clicked position
                x, y = self._click_pos
                
                # Call the gamma_self gauge callback if available
                if hasattr(self, 'gamma_self_gauge_callback') and self.gamma_self_gauge_callback:
                    print(f"[TRAJECTORY CLICK] Updating gamma_self gauge with ({x:.2f}, {y:.2f})")
                    self.gamma_self_gauge_callback(x, y)
                
        # ALWAYS clear click position to prevent freezing
        self._click_pos = None
    
    def update_start_marker_style(self, is_modified: bool):
        """
        Update start marker appearance based on whether gamma_self_0 is modified.
        
        Args:
            is_modified: True if gamma_self_0 has been changed from CSV default
        """
        if is_modified:
            # Modified: Orange square
            self.start_marker.set_marker('s')  # Square
            self.start_marker.set_color('orange')
            self.start_marker.set_label('Start (Modified)')
        else:
            # Original: Green circle
            self.start_marker.set_marker('o')  # Circle
            self.start_marker.set_color('green')
            self.start_marker.set_label('Start')
        
        force_canvas_draw(self.fig.canvas)
