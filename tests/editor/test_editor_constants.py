# tests/editor/test_editor_constants.py
"""
Unit tests for editor constants.
"""

import pytest
from tools.editor.editor_constants import (
    FLOAT_TOLERANCE,
    TIME_MATCH_TOLERANCE,
    MARKER_SIZE_NORMAL,
    MARKER_SIZE_BASELINE,
    MARKER_SIZE_DIAGNOSTIC,
    MARKER_SIZE_TRAJECTORY_START,
    MARKER_SIZE_TRAJECTORY_END,
    MARKER_SIZE_MODIFIED,
    MARKER_SIZE_ATTRACTOR,
    MARKER_SIZE_PINNED,
    LINE_WIDTH_TRAJECTORY,
    LINE_WIDTH_MODIFIED_MARKER,
    LINE_WIDTH_NORMAL_MARKER,
    LINE_WIDTH_LABEL_BORDER,
    PLOT_PADDING_NONE,
    PLOT_X_MARGIN,
    PRIMITIVE_MIN_VALUE,
    PRIMITIVE_MAX_VALUE
)


class TestToleranceConstants:
    """Test tolerance constants have reasonable values."""
    
    def test_float_tolerance_is_small(self):
        """Test that float tolerance is appropriate for comparisons."""
        assert 0 < FLOAT_TOLERANCE < 0.01
        assert isinstance(FLOAT_TOLERANCE, float)
    
    def test_time_match_tolerance_is_small(self):
        """Test that time match tolerance is appropriate."""
        assert 0 < TIME_MATCH_TOLERANCE < 0.01
        assert isinstance(TIME_MATCH_TOLERANCE, float)


class TestMarkerSizeConstants:
    """Test marker size constants are reasonable."""
    
    def test_marker_sizes_are_positive(self):
        """Test that all marker sizes are positive integers."""
        sizes = [
            MARKER_SIZE_NORMAL,
            MARKER_SIZE_BASELINE,
            MARKER_SIZE_DIAGNOSTIC,
            MARKER_SIZE_TRAJECTORY_START,
            MARKER_SIZE_TRAJECTORY_END,
            MARKER_SIZE_MODIFIED,
            MARKER_SIZE_ATTRACTOR,
            MARKER_SIZE_PINNED
        ]
        
        for size in sizes:
            assert size > 0
            assert isinstance(size, int)
    
    def test_marker_sizes_are_reasonable(self):
        """Test that marker sizes are in reasonable range."""
        sizes = [
            MARKER_SIZE_NORMAL,
            MARKER_SIZE_BASELINE,
            MARKER_SIZE_DIAGNOSTIC,
            MARKER_SIZE_TRAJECTORY_START,
            MARKER_SIZE_TRAJECTORY_END,
            MARKER_SIZE_MODIFIED,
            MARKER_SIZE_ATTRACTOR,
            MARKER_SIZE_PINNED
        ]
        
        for size in sizes:
            assert 5 <= size <= 20  # Reasonable UI sizes


class TestLineWidthConstants:
    """Test line width constants are reasonable."""
    
    def test_line_widths_are_positive(self):
        """Test that all line widths are positive integers."""
        widths = [
            LINE_WIDTH_TRAJECTORY,
            LINE_WIDTH_MODIFIED_MARKER,
            LINE_WIDTH_NORMAL_MARKER,
            LINE_WIDTH_LABEL_BORDER
        ]
        
        for width in widths:
            assert width > 0
            assert isinstance(width, int)
    
    def test_line_widths_are_reasonable(self):
        """Test that line widths are in reasonable range."""
        widths = [
            LINE_WIDTH_TRAJECTORY,
            LINE_WIDTH_MODIFIED_MARKER,
            LINE_WIDTH_NORMAL_MARKER,
            LINE_WIDTH_LABEL_BORDER
        ]
        
        for width in widths:
            assert 1 <= width <= 5  # Reasonable UI widths


class TestPlotConstants:
    """Test plot layout constants."""
    
    def test_plot_padding_is_zero_or_positive(self):
        """Test that padding values are non-negative."""
        assert PLOT_PADDING_NONE >= 0
        assert PLOT_X_MARGIN >= 0
    
    def test_primitive_range_is_valid(self):
        """Test that primitive min/max define valid range."""
        assert PRIMITIVE_MIN_VALUE < PRIMITIVE_MAX_VALUE
        assert isinstance(PRIMITIVE_MIN_VALUE, int)
        assert isinstance(PRIMITIVE_MAX_VALUE, int)
    
    def test_primitive_range_is_symmetric(self):
        """Test that primitive range is symmetric around zero."""
        assert PRIMITIVE_MIN_VALUE == -PRIMITIVE_MAX_VALUE
    
    def test_primitive_range_covers_expected_values(self):
        """Test that primitive range covers expected value range."""
        # Should cover at least -10 to +10
        assert PRIMITIVE_MIN_VALUE <= -10
        assert PRIMITIVE_MAX_VALUE >= 10
