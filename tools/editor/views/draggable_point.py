"""
Draggable control point widget for matplotlib.

Handles click-drag interaction for primitive editing.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.artist import Artist


class DraggablePoint:
    """
    Interactive control point for primitive editing.
    
    Allows vertical dragging (value change) while keeping time fixed.
    Respects lock status and value clamping.
    """
    
    def __init__(self, ax, x, y, event_index, primitive, callback, 
                 locked=False, color='blue', size=8, preview_callback=None, reset_callback=None):
        """
        Initialize draggable point.
        
        Args:
            ax: Matplotlib axes to draw on
            x: Time position
            y: Primitive value
            event_index: Index in events list
            primitive: 'v', 'r', 'f', 'a', or 'S'
            callback: Function(event_index, primitive, new_value) called on release
            locked: If True, point cannot be dragged
            color: Point color (grayed if locked)
            size: Point size in pixels
            preview_callback: Function(event_index, primitive, new_value) for live preview
            reset_callback: Function(event_index, primitive) for double-click reset
        """
        self.ax = ax
        self.x = x
        self.y = y
        self.original_y = y  # Store original committed value
        self.baseline_y = y  # Store CSV baseline (never changes)
        self.event_index = event_index
        self.primitive = primitive
        self.callback = callback
        self.preview_callback = preview_callback
        self.reset_callback = reset_callback
        self.locked = locked
        self.dragging = False
        
        # Visual appearance - filled point for committed
        point_color = 'gray' if locked else color
        self.point, = ax.plot([x], [y], 'o', color=point_color, 
                              markersize=size, picker=5, zorder=10,
                              markerfacecolor=point_color, markeredgecolor=point_color,
                              markeredgewidth=1.5)
        
        # Preview point (hollow) - initially invisible
        self.preview_point, = ax.plot([x], [y], 'o', color=color,
                                      markersize=size, zorder=11,
                                      markerfacecolor='none', markeredgecolor=color,
                                      markeredgewidth=2, visible=False)
        
        # Add hatching for locked points
        if locked:
            self.hatch_patch = ax.add_patch(
                plt.Circle((x, y), radius=0.3, facecolor='gray', 
                          alpha=0.3, hatch='///', zorder=9)
            )
        else:
            self.hatch_patch = None
        
        # Event connections
        self.cidpress = ax.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = ax.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = ax.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)
        
    def on_press(self, event):
        """Handle mouse button press."""
        if self.locked or event.inaxes != self.ax:
            return
        
        # Check if it's a double-click event (matplotlib built-in detection)
        if hasattr(event, 'dblclick') and event.dblclick:
            # For double-click, check if clicking near our position (x, y)
            # Use contains() check on the actual point artists since they account for picker tolerance
            on_point = False
            
            # Check preview point if visible
            if self.preview_point.get_visible():
                contains_preview, _ = self.preview_point.contains(event)
                if contains_preview:
                    on_point = True
            
            # Check committed point
            if not on_point:
                contains, _ = self.point.contains(event)
                if contains:
                    on_point = True
            
            # If not directly on a point, check if clicking near our stored position
            # Use a distance check but only within the same subplot (check event.inaxes)
            if not on_point and event.xdata is not None and event.ydata is not None:
                # Simple distance in data coordinates
                distance = ((event.xdata - self.x)**2 + (event.ydata - self.y)**2)**0.5
                # Use a more generous tolerance for double-clicks
                if distance < 1.5:
                    on_point = True
                    print(f"[DBLCLICK-PROXIMITY] {self.event_index}/{self.primitive}: distance={distance:.2f}")
            
            if on_point:
                print(f"Double-click detected on {self.event_index}/{self.primitive}")
                self.on_double_click()
                return
        
        # Single click - check if on either point
        on_preview = False
        on_committed = False
        
        if self.preview_point.get_visible():
            contains_preview, _ = self.preview_point.contains(event)
            on_preview = contains_preview
        
        if not on_preview:
            contains, _ = self.point.contains(event)
            on_committed = contains
        
        # If clicked on either point, start dragging
        if on_preview or on_committed:
            self.dragging = True
            self.original_y = self.y  # Store starting position
    
    def on_motion(self, event):
        """Handle mouse motion while dragging."""
        if not self.dragging or event.inaxes != self.ax:
            return
        
        # Update vertical position only (time stays fixed)
        # Clamp to valid range [-10, 10]
        new_y = np.clip(event.ydata, -10, 10)
        self.y = new_y
        
        # Show preview point (hollow) at new position
        self.preview_point.set_data([self.x], [self.y])
        self.preview_point.set_visible(True)
        
        # Keep original committed point visible
        # (don't move it during drag)
        
        # Call preview callback for live trajectory update
        if self.preview_callback:
            self.preview_callback(self.event_index, self.primitive, self.y)
        
        self.ax.figure.canvas.draw_idle()
    
    def on_release(self, event):
        """Handle mouse button release."""
        if self.dragging:
            self.dragging = False
            
            # Notify callback if value changed (still in preview mode)
            if abs(self.y - self.original_y) > 0.01:  # Tolerance for floating point
                self.callback(self.event_index, self.primitive, self.y)
            else:
                # No change, hide preview
                self.preview_point.set_visible(False)
                self.ax.figure.canvas.draw_idle()
    
    def commit_preview(self):
        """Commit preview: move filled point to preview position, hide preview."""
        if self.preview_point.get_visible():
            # Move committed point to preview position
            self.point.set_ydata([self.y])
            self.original_y = self.y
            # Hide hollow preview
            self.preview_point.set_visible(False)
            self.ax.figure.canvas.draw_idle()
    
    def cancel_preview(self):
        """Cancel preview: restore to original committed value."""
        self.y = self.original_y
        self.preview_point.set_visible(False)
        self.ax.figure.canvas.draw_idle()
    
    def on_double_click(self):
        """Handle double-click: reset to baseline CSV value."""
        if self.reset_callback:
            print(f"Double-click detected: Resetting event {self.event_index}/{self.primitive} to baseline")
            self.reset_callback(self.event_index, self.primitive)
        else:
            # Fallback: just reset locally
            self.y = self.baseline_y
            self.original_y = self.baseline_y
            self.point.set_ydata([self.y])
            self.preview_point.set_visible(False)
            self.ax.figure.canvas.draw_idle()
    
    def update_position(self, x, y):
        """Update point position (called when model changes)."""
        self.x = x
        self.y = y
        self.point.set_data([x], [y])
        
        if self.hatch_patch:
            self.hatch_patch.center = (x, y)
    
    def update_lock_status(self, locked):
        """Update lock visual status."""
        self.locked = locked
        color = 'gray' if locked else 'blue'
        self.point.set_color(color)
        
        if locked and not self.hatch_patch:
            # Add hatching
            import matplotlib.pyplot as plt
            self.hatch_patch = self.ax.add_patch(
                plt.Circle((self.x, self.y), radius=0.3, facecolor='gray',
                          alpha=0.3, hatch='///', zorder=9)
            )
        elif not locked and self.hatch_patch:
            # Remove hatching
            self.hatch_patch.remove()
            self.hatch_patch = None
        
        self.ax.figure.canvas.draw_idle()
    
    def disconnect(self):
        """Disconnect event handlers."""
        self.ax.figure.canvas.mpl_disconnect(self.cidpress)
        self.ax.figure.canvas.mpl_disconnect(self.cidrelease)
        self.ax.figure.canvas.mpl_disconnect(self.cidmotion)
