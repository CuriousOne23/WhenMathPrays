"""
Debug script to trace marker update flow in interactive editor.

Set breakpoints at these key locations:
1. Line with "BREAKPOINT 1" - When drag starts (mouse down)
2. Line with "BREAKPOINT 2" - During drag motion
3. Line with "BREAKPOINT 3" - When drag ends (mouse release)
4. Line with "BREAKPOINT 4" - When updating view from model

This will help understand why:
- Hollow markers aren't showing
- Duplicate markers are being left behind
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Simplified version of the key methods to understand the flow
class MockDraggablePoint:
    """Simplified DraggablePoint to understand marker behavior."""
    
    def __init__(self, x, y, event_index, primitive):
        self.x = x
        self.y = y
        self.event_index = event_index
        self.primitive = primitive
        self.dragging = False
        
        # Two separate marker objects
        self.point = {"visible": True, "facecolor": "blue", "position": (x, y)}
        self.preview_point = {"visible": False, "facecolor": "none", "position": (x, y)}
        
        print(f"Created DraggablePoint: event={event_index}, prim={primitive}, y={y}")
        print(f"  - point (filled): visible={self.point['visible']}, facecolor={self.point['facecolor']}")
        print(f"  - preview_point (hollow): visible={self.preview_point['visible']}, facecolor={self.preview_point['facecolor']}")
    
    def on_press(self):
        """BREAKPOINT 1 - Set breakpoint here to see drag start."""
        print(f"\n>>> DRAG START: event={self.event_index}, prim={self.primitive}")
        self.dragging = True
        print(f"  - dragging flag set to: {self.dragging}")
        return self.dragging
    
    def on_motion(self, new_y):
        """BREAKPOINT 2 - Set breakpoint here to see drag motion."""
        if not self.dragging:
            return
        
        print(f"\n>>> DRAG MOTION: event={self.event_index}, prim={self.primitive}, new_y={new_y}")
        self.y = new_y
        
        # Should show preview_point (hollow) and hide/keep original point
        self.preview_point["position"] = (self.x, new_y)
        self.preview_point["visible"] = True
        
        print(f"  - Updated preview_point: visible={self.preview_point['visible']}, position={self.preview_point['position']}")
        print(f"  - Original point: visible={self.point['visible']}, position={self.point['position']}")
        
        return self.preview_point
    
    def on_release(self):
        """BREAKPOINT 3 - Set breakpoint here to see drag end."""
        print(f"\n>>> DRAG RELEASE: event={self.event_index}, prim={self.primitive}")
        self.dragging = False
        
        # What should happen here?
        # Option A: Keep preview_point visible (hollow marker stays)
        # Option B: Hide preview_point, commit to main point
        
        print(f"  - dragging flag: {self.dragging}")
        print(f"  - preview_point visible: {self.preview_point['visible']}")
        print(f"  - point visible: {self.point['visible']}")


class MockPrimitivePanel:
    """Simplified PrimitivePanel to understand view update behavior."""
    
    def __init__(self):
        self.draggable_points = {}
    
    def update_from_model(self, events, modified_primitives):
        """BREAKPOINT 4 - Set breakpoint here to see view updates."""
        print(f"\n>>> UPDATE_FROM_MODEL called")
        print(f"  - Current draggable_points count: {len(self.draggable_points)}")
        print(f"  - Events to render: {len(events)}")
        print(f"  - Modified primitives: {modified_primitives}")
        
        # This is the problem: Creating NEW DraggablePoint objects
        # while old ones might still exist in matplotlib
        
        old_count = len(self.draggable_points)
        self.draggable_points.clear()  # Clear the dict
        print(f"  - Cleared {old_count} old draggable_points from dict")
        
        # Create new points for each event
        for event_idx, event in enumerate(events):
            for prim in ['v', 'r', 'f', 'a', 'S']:
                value = event[prim]
                
                # Check if this primitive was modified
                is_modified = event_idx in modified_primitives and prim in modified_primitives.get(event_idx, set())
                
                # Create new DraggablePoint
                dp = MockDraggablePoint(event['time'], value, event_idx, prim)
                
                # Try to set hollow if modified
                if is_modified:
                    dp.point["facecolor"] = "none"  # Make it hollow
                    print(f"  - Set HOLLOW marker for event={event_idx}, prim={prim}")
                
                self.draggable_points[(event_idx, prim)] = dp
        
        print(f"  - Created {len(self.draggable_points)} new draggable_points")
        print(f"  - WARNING: If old matplotlib artists not removed, duplicates will appear!")


def simulate_drag_scenario():
    """Simulate what happens during a drag operation."""
    print("="*60)
    print("SIMULATING DRAG OPERATION")
    print("="*60)
    
    # Initial state: 2 events, 1 primitive each (just 'v' for simplicity)
    events = [
        {'time': 0, 'v': 5, 'r': 0, 'f': 0, 'a': 0, 'S': 0},
        {'time': 10, 'v': 7, 'r': 0, 'f': 0, 'a': 0, 'S': 0}
    ]
    modified_primitives = {}
    
    panel = MockPrimitivePanel()
    
    # Step 1: Initial load
    print("\n[STEP 1] Initial load")
    panel.update_from_model(events, modified_primitives)
    
    # Step 2: User starts dragging event 1, primitive 'v'
    print("\n[STEP 2] User presses mouse on event 1, 'v'")
    dp = panel.draggable_points[(1, 'v')]
    dp.on_press()
    
    # Step 3: User drags (motion events)
    print("\n[STEP 3] User drags to new value 9")
    dp.on_motion(9)
    
    # Step 4: User releases mouse
    print("\n[STEP 4] User releases mouse")
    dp.on_release()
    
    # Step 5: Controller updates model and calls update_from_model again
    print("\n[STEP 5] Controller updates model and refreshes view")
    events[1]['v'] = 9  # Model updated with new value
    modified_primitives[1] = {'v'}  # Mark as modified
    
    # THIS IS THE PROBLEM: update_from_model creates NEW DraggablePoint objects
    # while the old matplotlib artists from Step 1 might still be visible
    panel.update_from_model(events, modified_primitives)
    
    print("\n" + "="*60)
    print("EXPECTED BEHAVIOR:")
    print("  - Old marker at value=7 should be removed/hidden")
    print("  - New HOLLOW marker at value=9 should be visible")
    print("\nACTUAL BEHAVIOR (BUG):")
    print("  - Old marker at value=7 still visible (duplicate!)")
    print("  - New marker at value=9 is FILLED not HOLLOW")
    print("  - Both markers visible = duplicate problem")
    print("="*60)


if __name__ == "__main__":
    print("Interactive Editor Debug Tracer\n")
    print("This script simulates the marker update flow.")
    print("Set breakpoints at lines marked 'BREAKPOINT' to trace through.\n")
    
    simulate_drag_scenario()
    
    print("\n\nKEY FINDINGS:")
    print("1. Every call to update_from_model() creates NEW DraggablePoint objects")
    print("2. Old matplotlib artists (point, preview_point) are not properly removed")
    print("3. This causes duplicates: old markers remain visible while new ones are created")
    print("4. Hollow marker logic tries to set facecolor='none' but on a freshly created object")
    print("   that doesn't have the preview point visible from the drag")
    print("\nSOLUTION:")
    print("1. Don't recreate DraggablePoint objects on every update")
    print("2. Instead, update existing DraggablePoint positions/styles")
    print("3. OR: Ensure old matplotlib artists are properly removed before creating new ones")
