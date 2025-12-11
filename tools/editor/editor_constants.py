# tools/editor/editor_constants.py
"""
Editor-specific constants for the interactive scenario editor.
Centralizes magic numbers and configuration values.
"""

# ===== Numeric Tolerances =====
# Tolerance for floating-point comparisons (e.g., checking if value equals baseline)
FLOAT_TOLERANCE = 0.001

# Tolerance for time matching when finding events in original CSV
TIME_MATCH_TOLERANCE = 0.001

# ===== Visual Style Constants =====
# Marker sizes (in plot units)
MARKER_SIZE_NORMAL = 7          # Regular data points
MARKER_SIZE_BASELINE = 10       # Baseline (original) markers
MARKER_SIZE_DIAGNOSTIC = 14     # Diagnostic "what-if" markers
MARKER_SIZE_TRAJECTORY_START = 12   # Trajectory start point
MARKER_SIZE_TRAJECTORY_END = 10     # Trajectory end point
MARKER_SIZE_MODIFIED = 8        # Modified trajectory points
MARKER_SIZE_ATTRACTOR = 10      # Attractor point
MARKER_SIZE_PINNED = 12         # Pinned trajectory markers

# Line widths (in pixels)
LINE_WIDTH_TRAJECTORY = 2       # Main trajectory line
LINE_WIDTH_MODIFIED_MARKER = 2  # Border of hollow modified markers
LINE_WIDTH_NORMAL_MARKER = 1    # Border of filled normal markers
LINE_WIDTH_LABEL_BORDER = 2     # Border around timestamp labels

# Plot padding
PLOT_PADDING_NONE = 0           # No padding (precise axis limits)
PLOT_X_MARGIN = 1               # Margin added to X axis when auto-ranging

# Primitive value range
PRIMITIVE_MIN_VALUE = -11       # Minimum primitive value for Y-axis
PRIMITIVE_MAX_VALUE = 11        # Maximum primitive value for Y-axis

# ===== Timing Constants =====
# Debounce delay for trajectory recomputation (in milliseconds)
PREVIEW_DEBOUNCE_MS = 150       # Delay before recomputing during drag

# ===== Color Constants =====
# (Already defined in constants.py, but referenced here for completeness)
# PRIMITIVE_COLORS, QUADRANT_COLORS are in tools/editor/constants.py
