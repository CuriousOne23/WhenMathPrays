"""
Primitive panel view - displays v, r, f, a, S curves with draggable points.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from .draggable_point import DraggablePoint


class PrimitivePanel:
    """
    Panel showing 5 primitive curves for one perspective.
    
    Each primitive (v, r, f, a, S) displayed as subplot with
    draggable control points.
    """
    
    PRIMITIVE_NAMES = ['v', 'r', 'f', 'a', 'S']
    PRIMITIVE_LABELS = {
        'v': 'Ego (v)',
        'r': 'Resonance (r)',
        'f': 'Fidelity (f)',
        'a': 'Vulnerability (a)',
        'S': 'Shared Breath (S)'
    }
    PRIMITIVE_COLORS = {
        'v': '#1f77b4',  # Blue
        'r': '#ff7f0e',  # Orange
        'f': '#2ca02c',  # Green
        'a': '#d62728',  # Red
        'S': '#9467bd'   # Purple (fixed lowercase)
    }
    
    def __init__(self, fig, grid_spec, on_primitive_changed, on_lock_toggle, on_primitive_preview=None, on_primitive_reset=None):
        """
        Initialize primitive panel.
        
        Args:
            fig: Matplotlib figure
            grid_spec: GridSpec or SubplotSpec for this panel
            on_primitive_changed: Callback(event_index, primitive, value) on release
            on_lock_toggle: Callback(event_index) for right-click lock toggle
            on_primitive_preview: Callback(event_index, primitive, value) during drag
            on_primitive_reset: Callback(event_index, primitive) for double-click reset
        """
        self.fig = fig
        self.on_primitive_changed = on_primitive_changed
        self.on_lock_toggle = on_lock_toggle
        self.on_primitive_preview = on_primitive_preview
        self.on_primitive_reset = on_primitive_reset
        
        # Create subplots for each primitive
        self.axes = {}
        self.lines = {}
        self.draggable_points = {}  # {(event_idx, primitive): DraggablePoint}
        self.marker_annotations = {}  # {(event_idx, primitive): Annotation} for numbered markers
        
        # Store manual x-axis limits for zoom
        self.manual_xlim = {}  # {prim: (xmin, xmax)}
        self.last_xlim = None  # For reset_view
        
        # Create 5 subplots stacked vertically
        # Use subgridspec for proper nesting
        from matplotlib.gridspec import GridSpecFromSubplotSpec
        inner_gs = GridSpecFromSubplotSpec(5, 1, subplot_spec=grid_spec, hspace=0.15)
        
        for i, prim in enumerate(self.PRIMITIVE_NAMES):
            ax = fig.add_subplot(inner_gs[i, 0])
            ax.set_ylabel(self.PRIMITIVE_LABELS[prim], fontsize=9)
            ax.set_ylim(-11, 11)
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5, alpha=0.5)
            
            # Only show x-axis label on bottom subplot
            if i == len(self.PRIMITIVE_NAMES) - 1:
                ax.set_xlabel('Time')
            else:
                ax.set_xticklabels([])
            
            # Initialize empty line
            line, = ax.plot([], [], '-', color=self.PRIMITIVE_COLORS[prim], 
                           linewidth=1.5, alpha=0.7)
            
            self.axes[prim] = ax
            self.lines[prim] = line
        
        # Context menu for lock/unlock (right-click)
        self.fig.canvas.mpl_connect('button_press_event', self._on_right_click)
    
    def update_from_model(self, primitives_data, events):
        """
        Update display from model data.
        
        Args:
            primitives_data: Dict with keys 'time', 'v', 'r', 'f', 'a', 'S'
            events: List of EventPoint objects for lock/marker info
        """
        times = primitives_data['time']
        
        # Update lines
        for prim in self.PRIMITIVE_NAMES:
            values = primitives_data[prim]
            self.lines[prim].set_data(times, values)
            
            # Auto-scale x-axis (unless manual zoom is active)
            if times and prim not in self.manual_xlim:
                xlim = (min(times) - 1, max(times) + 1)
                self.axes[prim].set_xlim(xlim)
                self.last_xlim = xlim  # Store for reset_view
        
        # Clear old draggable points
        for dp in self.draggable_points.values():
            dp.disconnect()
        self.draggable_points.clear()
        
        # Clear old annotations
        for ann in self.marker_annotations.values():
            ann.remove()
        self.marker_annotations.clear()
        
        # Create new draggable points
        for event_idx, event in enumerate(events):
            for prim in self.PRIMITIVE_NAMES:
                value = getattr(event, prim)
                
                dp = DraggablePoint(
                    ax=self.axes[prim],
                    x=event.time,
                    y=value,
                    event_index=event_idx,
                    primitive=prim,
                    callback=self._on_point_dragged,
                    preview_callback=self._on_point_preview if self.on_primitive_preview else None,
                    reset_callback=self._on_point_reset if self.on_primitive_reset else None,
                    locked=event.locked,
                    color=self.PRIMITIVE_COLORS[prim],
                    size=7
                )
                
                self.draggable_points[(event_idx, prim)] = dp
        
        # Redraw
        self.fig.canvas.draw_idle()
    
    def update_markers(self, marked_data):
        """
        Update numbered markers for specified events and primitives.
        Args:
            marked_data: Dict[event_idx, set of primitive names] or List[event_idx]
        """
        print(f"\n=== UPDATE_MARKERS called ===")
        print(f"marked_data: {marked_data}")
        # Clear old annotations safely
        print(f"Clearing {len(self.marker_annotations)} old annotations")
        for key, ann in list(self.marker_annotations.items()):
            try:
                if ann.axes is not None:
                    ann.remove()
                    print(f"  Removed annotation {key}")
            except Exception as e:
                print(f"  Error removing annotation {key}: {e}")
        self.marker_annotations.clear()

        # Add new annotations for marked events/primitives
        if marked_data:
            print(f"Adding markers for: {marked_data}")
            # If marked_data is a dict: {event_idx: set of primitives}
            if isinstance(marked_data, dict):
                for event_idx, prims in marked_data.items():
                    for prim in prims:
                        key = (event_idx, prim)
                        if key in self.draggable_points:
                            dp = self.draggable_points[key]
                            y_pos = dp.y if hasattr(dp, 'y') else dp.original_y
                            ann = self.axes[prim].annotate(
                                str(event_idx),
                                xy=(dp.x, y_pos),
                                xytext=(5, 5),
                                textcoords='offset points',
                                fontsize=8,
                                color=self.PRIMITIVE_COLORS[prim],
                                weight='bold',
                                bbox=dict(
                                    boxstyle='circle,pad=0.3',
                                    facecolor='white',
                                    edgecolor=self.PRIMITIVE_COLORS[prim],
                                    alpha=0.8
                                )
                            )
                            self.marker_annotations[key] = ann
                            print(f"    Created annotation {key}")
            # If marked_data is a list: [event_idx]
            elif isinstance(marked_data, list):
                for event_idx in marked_data:
                    for prim in self.PRIMITIVE_NAMES:
                        key = (event_idx, prim)
                        if key in self.draggable_points:
                            dp = self.draggable_points[key]
                            y_pos = dp.y if hasattr(dp, 'y') else dp.original_y
                            ann = self.axes[prim].annotate(
                                str(event_idx),
                                xy=(dp.x, y_pos),
                                xytext=(5, 5),
                                textcoords='offset points',
                                fontsize=8,
                                color=self.PRIMITIVE_COLORS[prim],
                                weight='bold',
                                bbox=dict(
                                    boxstyle='circle,pad=0.3',
                                    facecolor='white',
                                    edgecolor=self.PRIMITIVE_COLORS[prim],
                                    alpha=0.8
                                )
                            )
                            self.marker_annotations[key] = ann
                            print(f"    Created annotation {key}")
        print(f"=== END UPDATE_MARKERS ===\n")
        self.fig.canvas.draw_idle()
    def update_from_model(self, primitives_data, events):
        """
        Update display from model data.
        
        Args:
            primitives_data: Dict with keys 'time', 'v', 'r', 'f', 'a', 'S'
            events: List of EventPoint objects for lock/marker info
        """
        times = primitives_data['time']
        print("[DEBUG] update_from_model called")
        for prim in self.PRIMITIVE_NAMES:
            print(f"  {prim}: {primitives_data[prim]}")
        
        
        # Add annotations for marked events
        print(f"Creating annotations for {len(events)} events")
        for event_idx, event in enumerate(events):
            for prim in self.PRIMITIVE_NAMES:
                value = getattr(event, prim)
                # Assuming we want to create annotations for all primitives
                if value is not None:  # Only if the value is valid
                    print(f"  Event {event_idx}: primitive {prim} with value {value}")
                key = (event_idx, prim)
                if key in self.draggable_points:
                    dp = self.draggable_points[key]
                    # Use preview position if available, else committed position
                    y_pos = dp.y if dp.preview_point.get_visible() else dp.original_y
                    
                    ann = self.axes[prim].annotate(
                        str(event_idx),
                        xy=(dp.x, y_pos),
                        xytext=(5, 5),
                        textcoords='offset points',
                        fontsize=8,
                        color=self.PRIMITIVE_COLORS[prim],  # Match primitive color
                        weight='bold',
                        bbox=dict(
                            boxstyle='circle,pad=0.3',
                            facecolor='white',
                            edgecolor=self.PRIMITIVE_COLORS[prim],  # Match primitive color
                            alpha=0.8
                        )
                    )
                    self.marker_annotations[key] = ann
                    print(f"    Created annotation {key}")
        
        print(f"=== END UPDATE_MARKERS ===\n")
        
        # Redraw
        self.fig.canvas.draw_idle()
    
    def _on_point_dragged(self, event_index, primitive, new_value):
        """Handle point drag completion (release)."""
        self.on_primitive_changed(event_index, primitive, new_value)
    
    def _on_point_preview(self, event_index, primitive, new_value):
        """Handle point drag preview (during motion)."""
        if self.on_primitive_preview:
            self.on_primitive_preview(event_index, primitive, new_value)
    
    def _on_point_reset(self, event_index, primitive):
        """Handle double-click reset."""
        if self.on_primitive_reset:
            self.on_primitive_reset(event_index, primitive)
    
    def commit_all_previews(self):
        """Commit all preview points."""
        for dp in self.draggable_points.values():
            dp.commit_preview()
    
    def cancel_all_previews(self):
        """Cancel all preview points."""
        for dp in self.draggable_points.values():
            dp.cancel_preview()
    
    def _on_right_click(self, event):
        """Handle right-click for lock/unlock context menu."""
        if event.button != 3:  # Not right-click
            return
        
        # Find which point was clicked
        for (event_idx, prim), dp in self.draggable_points.items():
            if event.inaxes == dp.ax:
                contains, _ = dp.point.contains(event)
                if contains:
                    # Toggle lock for this event
                    self.on_lock_toggle(event_idx)
                    break
    
    def update_lock_status(self, event_index, locked):
        """Update lock visual for specific event."""
        for prim in self.PRIMITIVE_NAMES:
            key = (event_index, prim)
            if key in self.draggable_points:
                self.draggable_points[key].update_lock_status(locked)
    
    def zoom_in(self, factor=0.8):
        """Zoom in on all primitive subplots (x-axis only)."""
        for prim, ax in self.axes.items():
            xlim = self.manual_xlim.get(prim, ax.get_xlim())
            x_center = (xlim[0] + xlim[1]) / 2
            x_range = (xlim[1] - xlim[0]) * factor / 2
            new_xlim = (x_center - x_range, x_center + x_range)
            ax.set_xlim(new_xlim)
            self.manual_xlim[prim] = new_xlim
        self.fig.canvas.draw_idle()
    
    def zoom_out(self, factor=1.2):
        """Zoom out on all primitive subplots (x-axis only)."""
        for prim, ax in self.axes.items():
            xlim = self.manual_xlim.get(prim, ax.get_xlim())
            x_center = (xlim[0] + xlim[1]) / 2
            x_range = (xlim[1] - xlim[0]) * factor / 2
            new_xlim = (x_center - x_range, x_center + x_range)
            ax.set_xlim(new_xlim)
            self.manual_xlim[prim] = new_xlim
        self.fig.canvas.draw_idle()
    
    def reset_view(self):
        """Reset zoom to auto-fit all data."""
        print("\n=== RESET PRIMITIVE VIEW ===")
        print(f"manual_xlim before clear: {self.manual_xlim}")
        
        # Clear manual zoom state
        self.manual_xlim.clear()
        
        # Recompute auto-fit from current line data (both x and y axes)
        for prim, line in self.lines.items():
            xdata, ydata = line.get_data()
            if len(xdata) > 0:
                # Reset x-axis (time)
                xlim = (min(xdata) - 1, max(xdata) + 1)
                self.axes[prim].set_xlim(xlim)
                
                # Reset y-axis (value) - compute from data range
                if len(ydata) > 0:
                    y_min, y_max = min(ydata), max(ydata)
                    y_margin = max(1.0, (y_max - y_min) * 0.1)  # 10% margin or min 1.0
                    ylim = (y_min - y_margin, y_max + y_margin)
                    self.axes[prim].set_ylim(ylim)
                    print(f"  {prim}: x=[{min(xdata):.1f}, {max(xdata):.1f}], y=[{y_min:.1f}, {y_max:.1f}] → ylim={ylim}")
                else:
                    print(f"  {prim}: x=[{min(xdata):.1f}, {max(xdata):.1f}]")
        
        print("=== END RESET ===")
        self.fig.canvas.draw_idle()
