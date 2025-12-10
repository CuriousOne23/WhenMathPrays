"""
Canvas drawing utilities for Qt backend compatibility.

PySide6/Qt backend requires explicit event processing for immediate canvas updates.
"""


def force_canvas_draw(canvas):
    """
    Force immediate canvas redraw with Qt event processing.
    
    Args:
        canvas: Matplotlib canvas (FigureCanvasQTAgg or similar)
    """
    canvas.draw_idle()
    
    # Qt backend needs flush_events() to process draw queue immediately
    try:
        canvas.flush_events()
    except AttributeError:
        # Not a Qt backend or flush_events not available
        pass
