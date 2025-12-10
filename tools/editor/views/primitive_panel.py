"""
Primitive panel view - displays v, r, f, a, S curves with draggable points.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from .draggable_point import DraggablePoint
from .canvas_utils import force_canvas_draw
from ..primitives import PRIMITIVE_NAMES, PRIMITIVE_LABELS, PRIMITIVE_COLORS


class PrimitivePanel:
    PRIMITIVE_NAMES = PRIMITIVE_NAMES
    PRIMITIVE_LABELS = PRIMITIVE_LABELS
    PRIMITIVE_COLORS = PRIMITIVE_COLORS

    def __init__(self, fig, grid_spec, on_primitive_changed, on_lock_toggle, on_primitive_preview=None, on_primitive_reset=None, layout=None):
        """
        Initialize primitive panel.
        Args:
            fig: Matplotlib figure
            grid_spec: GridSpec or SubplotSpec for this panel
            on_primitive_changed: Callback(event_index, primitive, value) on release
            on_lock_toggle: Callback(event_index) for right-click lock toggle
            on_primitive_preview: Callback(event_index, primitive, value) during drag
            on_primitive_reset: Callback(event_index, primitive) for double-click reset
            layout: Layout configuration dict (optional)
        """
        self.fig = fig
        self.on_primitive_changed = on_primitive_changed
        self.on_lock_toggle = on_lock_toggle
        self.on_primitive_preview = on_primitive_preview
        self.on_primitive_reset = on_primitive_reset
        self.on_insert_event = None  # Will be set by controller
        self.layout = layout or {}  # Store layout config

        # Create subplots for each primitive
        self.axes = {}
        self.lines = {}
        self.draggable_points = {}  # {(event_idx, primitive): DraggablePoint}
        self.original_markers = {}  # {(event_idx, primitive): matplotlib artist} - static filled markers at baseline
        self.baseline_values = {}  # {(event_idx, primitive): float} - original CSV values
        self.marker_annotations = {}  # {(event_idx, primitive): Annotation} for numbered markers
        self.insertion_lines = []  # Vertical dashed lines marking inserted events

        # Store manual x-axis limits for zoom
        self.manual_xlim = {}  # {prim: (xmin, xmax)}
        self.last_xlim = None  # For reset_view
        
        # Readout display for last edited marker
        self.readout_text = None  # Will be created after axes are set up

        # Create 5 subplots stacked vertically
        from matplotlib.gridspec import GridSpecFromSubplotSpec
        inner_gs = GridSpecFromSubplotSpec(5, 1, subplot_spec=grid_spec, hspace=0.15)
        for i, prim in enumerate(self.PRIMITIVE_NAMES):
            ax = fig.add_subplot(inner_gs[i, 0])
            ax.set_ylabel(self.PRIMITIVE_LABELS[prim], fontsize=9)
            ax.set_ylim(-11, 11)
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5, alpha=0.5)
            if i == len(self.PRIMITIVE_NAMES) - 1:
                ax.set_xlabel('Time')
            else:
                ax.set_xticklabels([])
            line, = ax.plot([], [], '-', color=self.PRIMITIVE_COLORS[prim], linewidth=1.5, alpha=0.7)
            self.axes[prim] = ax
            self.lines[prim] = line
        
        # Create readout text display (positioned to the left of fidelity plot)
        f_ax = self.axes['f']
        gauge_x = self.layout.get('primitive_gauge_x', -0.25)
        gauge_y = self.layout.get('primitive_gauge_y', 0.35)  # Moved down from 0.5
        self.readout_text = f_ax.text(
            gauge_x, gauge_y, '',  # Use layout config
            transform=f_ax.transAxes,
            fontsize=10,
            verticalalignment='center',
            horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='black', alpha=0.8)
        )
        
        # Connect click event for sampling primitive values
        self.events_data = []  # Store events for nearest-marker lookup
        self.fig.canvas.mpl_connect('button_press_event', self._on_click_sample)

    def _on_click_sample(self, event):
        """Handle click on primitive plot to sample value and show nearest marker."""
        # Only handle left-click (button 1) and when not dragging
        if event.button != 1 or not event.inaxes:
            return
        
        # Check if click is on any of our primitive axes
        clicked_prim = None
        for prim, ax in self.axes.items():
            if event.inaxes == ax:
                clicked_prim = prim
                break
        
        if not clicked_prim:
            return
        
        # Check for Shift+Click to insert event
        # In matplotlib, modifier keys are in event.key when combined with click
        # Shift modifier shows as 'shift' or the key includes 'shift+'
        is_shift_click = False
        if event.key:
            # Check if 'shift' is in the key string
            is_shift_click = 'shift' in event.key.lower()
        
        # Also check Qt modifiers as backup (PySide6)
        if not is_shift_click and hasattr(event, 'guiEvent'):
            try:
                from PySide6.QtCore import Qt
                gui_event = event.guiEvent
                if hasattr(gui_event, 'modifiers'):
                    is_shift_click = bool(gui_event.modifiers() & Qt.ShiftModifier)
            except:
                pass
        
        if is_shift_click and event.xdata:
            # Trigger event insertion callback (rounding done by caller)
            if hasattr(self, 'on_insert_event') and self.on_insert_event:
                self.on_insert_event(event.xdata)
            return
        
        # Check if clicking on a draggable point (if so, let the drag handler take over)
        for (event_idx, prim), dp in self.draggable_points.items():
            if prim == clicked_prim:
                # Check if clicking near this point
                contains_filled, _ = dp.point.contains(event)
                contains_preview = False
                if dp.preview_point.get_visible():
                    contains_preview, _ = dp.preview_point.contains(event)
                if contains_filled or contains_preview:
                    # Let drag handler take over
                    return
        
        # Not clicking on a marker - sample the value at this location
        click_time = event.xdata
        click_value = event.ydata
        
        # Find nearest event marker
        if not self.events_data:
            return
        
        nearest_event_idx = None
        min_distance = float('inf')
        for idx, evt in enumerate(self.events_data):
            dist = abs(evt.time - click_time)
            if dist < min_distance:
                min_distance = dist
                nearest_event_idx = idx
        
        # Update readout with click location and nearest marker
        if nearest_event_idx is not None:
            marker_id = f"{nearest_event_idx}{clicked_prim}"
            self._update_readout(nearest_event_idx, clicked_prim, click_value)

    def update_from_model(self, events):
        """
        Update display from model data using Event and Marker objects.
        Args:
            events: List of Event objects
        """
        # Store events for click sampling
        self.events_data = events
        
        # Always cancel all previews before updating
        self.cancel_all_previews()
        # Get modified_primitives from model
        model = getattr(self.controller, 'model', None) if hasattr(self, 'controller') else None
        mod_prims = getattr(model, 'modified_primitives', {}) if model else {}
        
        for prim in self.PRIMITIVE_NAMES:
            times = [event.time for event in events]
            values = [event.markers[prim].value for event in events]
            self.lines[prim].set_data(times, values)
            if times and prim not in self.manual_xlim:
                xlim = (min(times) - 1, max(times) + 1)
                self.axes[prim].set_xlim(xlim)
                self.last_xlim = xlim
        for dp in self.draggable_points.values():
            dp.disconnect()
        self.draggable_points.clear()
        
        # Remove old original markers
        for artist in self.original_markers.values():
            if artist:
                artist.remove()
        self.original_markers.clear()
        
        # Store baseline values on first load (if not already stored)
        if not self.baseline_values:
            for event_idx, event in enumerate(events):
                for prim in self.PRIMITIVE_NAMES:
                    self.baseline_values[(event_idx, prim)] = event.markers[prim].value
        
        # Don't clear marker_annotations here - they are managed by update_markers()
        # Only that method should add/remove numbered markers
        
        for event_idx, event in enumerate(events):
            for prim in self.PRIMITIVE_NAMES:
                marker = event.markers[prim]
                # Determine if marker has been edited
                edited = event_idx in mod_prims and prim in mod_prims.get(event_idx, set())
                
                # If edited, show original marker (filled, non-draggable) at baseline position
                if edited:
                    baseline_val = self.baseline_values.get((event_idx, prim), marker.value)
                    if abs(baseline_val - marker.value) > 0.001:  # Only if actually different
                        original_marker, = self.axes[prim].plot(
                            [marker.time], [baseline_val], 'o',
                            color=self.PRIMITIVE_COLORS[prim],
                            markerfacecolor=self.PRIMITIVE_COLORS[prim],
                            markeredgecolor=self.PRIMITIVE_COLORS[prim],
                        markersize=7,
                        alpha=0.5,  # Semi-transparent to show it's the "old" position
                        zorder=5  # Below the draggable points
                    )
                    self.original_markers[(event_idx, prim)] = original_marker
                
                # Create DraggablePoint for current (possibly modified) position
                baseline_val = self.baseline_values.get((event_idx, prim), marker.value)
                dp = DraggablePoint(
                    ax=self.axes[prim],
                    x=marker.time,
                    y=marker.value,
                    event_index=event_idx,
                    primitive=prim,
                    callback=self._on_point_dragged,
                    preview_callback=self._on_point_preview if self.on_primitive_preview else None,
                    reset_callback=self._on_point_reset if self.on_primitive_reset else None,
                    locked=False,
                    color=self.PRIMITIVE_COLORS[prim],
                    size=7,
                    baseline_y=baseline_val
                )
                
                # Set marker appearance based on edit state
                if edited:
                    # Show hollow marker for modified points
                    dp.point.set_markerfacecolor('none')
                    dp.point.set_markeredgecolor(self.PRIMITIVE_COLORS[prim])
                    dp.point.set_markeredgewidth(2)
                else:
                    # Show filled marker for unmodified points
                    dp.point.set_markerfacecolor(self.PRIMITIVE_COLORS[prim])
                    dp.point.set_markeredgecolor(self.PRIMITIVE_COLORS[prim])
                
                # Ensure preview point is hidden (it's only shown during active dragging)
                dp.preview_point.set_visible(False)
                
                self.draggable_points[(event_idx, prim)] = dp
        
        # Draw vertical dashed lines for inserted events (all primitives at 0)
        self._update_insertion_lines(events)
        
        # Use non-blocking draw
        self.fig.canvas.draw_idle()
    
    def _update_insertion_lines(self, events):
        """
        Draw vertical dashed lines for inserted events (where all primitives are 0).
        
        Args:
            events: List of Event objects
        """
        # Remove old insertion lines
        for line in self.insertion_lines:
            line.remove()
        self.insertion_lines.clear()
        
        # Find events where all primitives are 0 (inserted events)
        for event_idx, event in enumerate(events):
            all_zero = all(abs(event.markers[prim].value) < 0.001 for prim in self.PRIMITIVE_NAMES)
            if all_zero and event_idx > 0 and event_idx < len(events) - 1:  # Don't mark first/last
                # Draw vertical dashed line across all primitive plots
                for prim in self.PRIMITIVE_NAMES:
                    line = self.axes[prim].axvline(
                        x=event.time,
                        color='gray',
                        linestyle='--',
                        linewidth=1.5,
                        alpha=0.6,
                        zorder=1  # Behind markers
                    )
                    self.insertion_lines.append(line)
    
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
        print(f"=== END UPDATE_MARKERS ===")
        force_canvas_draw(self.fig.canvas)
    
    def _on_point_dragged(self, event_index, primitive, new_value):
        """Handle point drag completion (release)."""
        print(f"[DEBUG] _on_point_dragged called: event={event_index}, prim={primitive}, new_value={new_value}")
        # Update readout display with marker ID and value
        self._update_readout(event_index, primitive, new_value)
        # Commit the new value to the model and let the controller handle UI refresh
        self.on_primitive_changed(event_index, primitive, new_value)
    
    def _on_point_preview(self, event_index, primitive, new_value):
        """Handle point drag preview (during motion)."""
        # Update readout display during drag
        self._update_readout(event_index, primitive, new_value)
        
        if self.on_primitive_preview:
            self.on_primitive_preview(event_index, primitive, new_value)
        # Update the curve in real time to pass through the hollow marker
        dp = self.draggable_points.get((event_index, primitive))
        if dp:
            # Update the corresponding value in the line data
            line = self.lines[primitive]
            xdata, ydata = line.get_data()
            if 0 <= event_index < len(ydata):
                ydata = list(ydata)
                ydata[event_index] = new_value
                line.set_data(xdata, ydata)
            force_canvas_draw(self.fig.canvas)
    
    def _on_point_reset(self, event_index, primitive):
        """Handle double-click reset."""
        if self.on_primitive_reset:
            self.on_primitive_reset(event_index, primitive)
        # After reset, hide all preview markers and refresh UI
        self.cancel_all_previews()
        force_canvas_draw(self.fig.canvas)
    
    def _update_readout(self, event_index, primitive, value):
        """Update the readout display with marker ID and value.
        
        Args:
            event_index: Event index (marker number)
            primitive: Primitive name (v, r, f, a, S)
            value: Y value
        """
        if self.readout_text:
            marker_id = f"{event_index}{primitive}"
            self.readout_text.set_text(f"{marker_id}\n{value:.2f}")
            self.readout_text.set_visible(True)
            force_canvas_draw(self.fig.canvas)
    
    def clear_readout(self):
        """Clear the readout display."""
        if self.readout_text:
            self.readout_text.set_visible(False)
            force_canvas_draw(self.fig.canvas)
    
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
    
    def zoom_in(self, factor=0.8, target_axes=None):
        """Zoom in on specific primitive subplot or all if target_axes not specified.
        
        Args:
            factor: Zoom factor (0.8 = zoom in to 80% of current range)
            target_axes: Specific matplotlib axes to zoom, or None for all
        """
        if target_axes:
            # Zoom only the specific subplot
            for prim, ax in self.axes.items():
                if ax == target_axes:
                    xlim = self.manual_xlim.get(prim, ax.get_xlim())
                    x_center = (xlim[0] + xlim[1]) / 2
                    x_range = (xlim[1] - xlim[0]) * factor / 2
                    new_xlim = (x_center - x_range, x_center + x_range)
                    ax.set_xlim(new_xlim)
                    self.manual_xlim[prim] = new_xlim
                    break
        else:
            # Zoom all subplots (legacy behavior)
            for prim, ax in self.axes.items():
                xlim = self.manual_xlim.get(prim, ax.get_xlim())
                x_center = (xlim[0] + xlim[1]) / 2
                x_range = (xlim[1] - xlim[0]) * factor / 2
                new_xlim = (x_center - x_range, x_center + x_range)
                ax.set_xlim(new_xlim)
                self.manual_xlim[prim] = new_xlim
        force_canvas_draw(self.fig.canvas)
    
    def zoom_out(self, factor=1.2, target_axes=None):
        """Zoom out on specific primitive subplot or all if target_axes not specified.
        
        Args:
            factor: Zoom factor (1.2 = zoom out to 120% of current range)
            target_axes: Specific matplotlib axes to zoom, or None for all
        """
        if target_axes:
            # Zoom only the specific subplot
            for prim, ax in self.axes.items():
                if ax == target_axes:
                    # Initialize manual_xlim if not set (first zoom_out)
                    if prim not in self.manual_xlim:
                        self.manual_xlim[prim] = ax.get_xlim()
                    
                    xlim = self.manual_xlim[prim]
                    x_center = (xlim[0] + xlim[1]) / 2
                    x_range = (xlim[1] - xlim[0]) * factor / 2
                    new_xlim = (x_center - x_range, x_center + x_range)
                    ax.set_xlim(new_xlim)
                    self.manual_xlim[prim] = new_xlim
                    break
        else:
            # Zoom all subplots (legacy behavior)
            for prim, ax in self.axes.items():
                # Initialize manual_xlim if not set (first zoom_out)
                if prim not in self.manual_xlim:
                    self.manual_xlim[prim] = ax.get_xlim()
                
                xlim = self.manual_xlim[prim]
                x_center = (xlim[0] + xlim[1]) / 2
                x_range = (xlim[1] - xlim[0]) * factor / 2
                new_xlim = (x_center - x_range, x_center + x_range)
                ax.set_xlim(new_xlim)
                self.manual_xlim[prim] = new_xlim
        force_canvas_draw(self.fig.canvas)
    
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
        force_canvas_draw(self.fig.canvas)
    
    def save_plot(self, filepath: str):
        """Save the primitive panel plots to a PNG file.
        
        Args:
            filepath: Output PNG file path
        """
        # Create a new figure with just the primitive subplots
        save_fig = plt.figure(figsize=(10, 12))
        
        for i, prim in enumerate(self.PRIMITIVE_NAMES):
            ax = save_fig.add_subplot(5, 1, i+1)
            
            # Copy the line data
            if prim in self.lines:
                line = self.lines[prim]
                xdata, ydata = line.get_data()
                ax.plot(xdata, ydata, color=self.PRIMITIVE_COLORS[prim], linewidth=2)
            
            # Copy markers (both baseline and modified)
            for (event_idx, p), marker in self.original_markers.items():
                if p == prim and marker.axes == self.axes[prim]:
                    xdata, ydata = marker.get_data()
                    ax.plot(xdata, ydata, marker='o', color=self.PRIMITIVE_COLORS[prim],
                           markersize=8, markeredgewidth=1.5, markeredgecolor='black',
                           linestyle='none')
            
            for (event_idx, p), dp in self.draggable_points.items():
                if p == prim:
                    ax.plot([dp.x], [dp.y], marker='o', color=self.PRIMITIVE_COLORS[prim],
                           markersize=8, markerfacecolor='white', markeredgewidth=1.5,
                           markeredgecolor=self.PRIMITIVE_COLORS[prim], linestyle='none')
            
            # Copy axis properties
            ax.set_ylabel(self.PRIMITIVE_LABELS[prim], fontsize=10, fontweight='bold')
            ax.set_ylim(self.axes[prim].get_ylim())
            ax.set_xlim(self.axes[prim].get_xlim())
            ax.grid(True, alpha=0.3)
            
            if i == 4:  # Last subplot
                ax.set_xlabel('Time', fontsize=10)
        
        save_fig.tight_layout()
        save_fig.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close(save_fig)
    
    # === Phase 2: Incremental Update Methods ===
    
    def update_marker(self, event_idx: int, prim: str, value: float, is_modified: bool):
        """
        Update single marker incrementally (Phase 2 refactor).
        
        Args:
            event_idx: Event index
            prim: Primitive name
            value: New value to display
            is_modified: Whether to show as modified from baseline
        """
        # Get the marker object
        marker_key = (event_idx, prim)
        if marker_key not in self.draggable_points:
            print(f"[WARNING] Marker {marker_key} not found in draggable_points")
            return
        
        marker = self.draggable_points[marker_key]
        
        # Update position
        marker.y = value
        marker.original_y = value
        marker.point.set_ydata([value])
        
        # Update the line plot data at this event index
        if prim in self.lines:
            line = self.lines[prim]
            xdata, ydata = line.get_data()
            if event_idx < len(ydata):
                ydata_list = list(ydata)
                ydata_list[event_idx] = value
                line.set_ydata(ydata_list)
        
        # Update modified state visual
        marker.set_modified(is_modified)
        
        # Hide preview point if visible
        if marker.preview_point.get_visible():
            marker.preview_point.set_visible(False)
        
        # Efficient partial redraw
        force_canvas_draw(self.fig.canvas)
    
    def clear_all_modified(self):
        """
        Clear modified visual state from all markers (after save).
        """
        for marker in self.draggable_points.values():
            marker.set_modified(False)
        
        force_canvas_draw(self.fig.canvas)
    
    def remove_marker_label(self, event_idx: int, prim: str):
        """
        Remove label annotation for a specific marker immediately.
        
        Args:
            event_idx: Event index
            prim: Primitive name
        """
        marker_key = (event_idx, prim)
        if marker_key in self.marker_annotations:
            ann = self.marker_annotations[marker_key]
            try:
                if ann.axes is not None:
                    ann.remove()
                    print(f"[DEBUG] Removed label annotation {marker_key}")
            except Exception as e:
                print(f"[WARNING] Error removing label annotation {marker_key}: {e}")
            del self.marker_annotations[marker_key]
            force_canvas_draw(self.fig.canvas)
