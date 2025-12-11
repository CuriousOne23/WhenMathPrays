# tests/editor/test_editor_utils.py
"""
Unit tests for editor utility functions.
"""

import pytest
import numpy as np
from tools.editor.editor_utils import (
    for_each_primitive,
    for_each_primitive_with_result,
    remove_event_markers,
    clear_modified_primitives_for_event,
    get_all_modified_markers,
    count_modified_markers,
    validate_primitive_value,
    update_baseline_arrays
)


class TestForEachPrimitive:
    """Test primitive iteration utilities."""
    
    def test_for_each_primitive_executes_callback(self):
        """Test that callback is executed for each primitive."""
        visited = []
        
        def collect(prim):
            visited.append(prim)
        
        for_each_primitive(collect)
        
        assert len(visited) == 5
        assert set(visited) == {'v', 'r', 'f', 'a', 'S'}
    
    def test_for_each_primitive_with_result_collects_values(self):
        """Test that results are collected from callback."""
        result = for_each_primitive_with_result(lambda p: p.upper())
        
        assert len(result) == 5
        assert result['v'] == 'V'
        assert result['r'] == 'R'
        assert result['S'] == 'S'


class MockModel:
    """Mock model for testing."""
    
    def __init__(self):
        self.marker_positions = {}
        self.modified_primitives = {}
    
    def is_modified(self, event_idx, prim, perspective):
        """Check if marker is modified."""
        time = event_idx * 10  # Mock time calculation
        return time in self.modified_primitives and prim in self.modified_primitives[time]


class TestRemoveEventMarkers:
    """Test marker removal utilities."""
    
    def test_remove_event_markers_deletes_positions(self):
        """Test that marker positions are removed."""
        model = MockModel()
        model.marker_positions = {
            (10.0, 'v'): (1, 2),
            (10.0, 'r'): (3, 4),
            (10.0, 'f'): (5, 6),
            (20.0, 'v'): (7, 8)
        }
        
        remove_event_markers(model, 10.0)
        
        # All markers at time 10.0 should be removed
        assert (10.0, 'v') not in model.marker_positions
        assert (10.0, 'r') not in model.marker_positions
        assert (10.0, 'f') not in model.marker_positions
        # Markers at other times should remain
        assert (20.0, 'v') in model.marker_positions
    
    def test_remove_event_markers_with_labels(self):
        """Test that labels are removed via callback."""
        model = MockModel()
        model.marker_positions = {(10.0, 'v'): (1, 2)}
        
        removed_labels = []
        
        def remove_label(event_idx, prim):
            removed_labels.append((event_idx, prim))
        
        remove_event_markers(model, 10.0, remove_label_callback=remove_label, event_index=5)
        
        # Should have called callback for all 5 primitives
        assert len(removed_labels) == 5
        assert all(idx == 5 for idx, _ in removed_labels)


class TestClearModifiedPrimitives:
    """Test modified primitives tracking."""
    
    def test_clear_modified_primitives_removes_entry(self):
        """Test that modified primitives entry is removed."""
        model = MockModel()
        model.modified_primitives = {
            10.0: {'v', 'r'},
            20.0: {'f'}
        }
        
        clear_modified_primitives_for_event(model, 10.0)
        
        assert 10.0 not in model.modified_primitives
        assert 20.0 in model.modified_primitives
    
    def test_clear_modified_primitives_handles_missing_time(self):
        """Test that clearing non-existent time doesn't error."""
        model = MockModel()
        model.modified_primitives = {}
        
        # Should not raise exception
        clear_modified_primitives_for_event(model, 10.0)


class TestGetAllModifiedMarkers:
    """Test modified marker state collection."""
    
    def test_get_all_modified_markers_builds_dict(self):
        """Test that modified state dictionary is built correctly."""
        model = MockModel()
        model.modified_primitives = {
            0: {'v', 'r'},
            10: {'f'}
        }
        
        # Mock events (just need count)
        events = [None, None]  # 2 events
        
        result = get_all_modified_markers(model, events, 'baseline')
        
        # Should have entries for modified markers
        assert (0, 'v') in result
        assert (0, 'r') in result
        assert (1, 'f') in result
        assert result[(0, 'v')] is True
    
    def test_get_all_modified_markers_empty_when_no_modifications(self):
        """Test that empty dict is returned when nothing modified."""
        model = MockModel()
        model.modified_primitives = {}
        
        events = [None]
        
        result = get_all_modified_markers(model, events, 'baseline')
        
        assert len(result) == 0


class TestCountModifiedMarkers:
    """Test modified marker counting."""
    
    def test_count_modified_markers_returns_correct_count(self):
        """Test that count matches number of modified markers."""
        model = MockModel()
        model.modified_primitives = {
            0: {'v', 'r', 'f'},
            10: {'a'}
        }
        
        events = [None, None]
        
        count = count_modified_markers(model, events)
        
        # 3 at event 0 + 1 at event 1 = 4 total
        assert count == 4
    
    def test_count_modified_markers_zero_when_none(self):
        """Test that zero is returned when nothing modified."""
        model = MockModel()
        model.modified_primitives = {}
        
        count = count_modified_markers(model, [None])
        
        assert count == 0


class TestValidatePrimitiveValue:
    """Test primitive value validation."""
    
    def test_validate_clamps_to_maximum(self):
        """Test that values above max are clamped."""
        result = validate_primitive_value(15.0, -10.0, 10.0)
        assert result == 10.0
    
    def test_validate_clamps_to_minimum(self):
        """Test that values below min are clamped."""
        result = validate_primitive_value(-15.0, -10.0, 10.0)
        assert result == -10.0
    
    def test_validate_passes_through_valid_values(self):
        """Test that valid values are unchanged."""
        result = validate_primitive_value(5.0, -10.0, 10.0)
        assert result == 5.0
    
    def test_validate_handles_boundary_values(self):
        """Test that boundary values are accepted."""
        assert validate_primitive_value(10.0, -10.0, 10.0) == 10.0
        assert validate_primitive_value(-10.0, -10.0, 10.0) == -10.0


class TestUpdateBaselineArrays:
    """Test baseline array update utilities."""
    
    def test_update_baseline_arrays_insert(self):
        """Test inserting values into baseline arrays."""
        baseline = {
            'v': np.array([1.0, 2.0, 3.0]),
            'r': np.array([4.0, 5.0, 6.0]),
            'f': np.array([7.0, 8.0, 9.0]),
            'a': np.array([10.0, 11.0, 12.0]),
            'S': np.array([13.0, 14.0, 15.0])
        }
        
        values = {'v': 1.5, 'r': 4.5, 'f': 7.5, 'a': 10.5, 'S': 13.5}
        
        update_baseline_arrays(baseline, 'insert', 1, values)
        
        # Check that values were inserted at index 1
        assert len(baseline['v']) == 4
        assert baseline['v'][1] == 1.5
        assert baseline['r'][1] == 4.5
        assert baseline['S'][1] == 13.5
        
        # Check that original values shifted
        assert baseline['v'][2] == 2.0
        assert baseline['v'][3] == 3.0
    
    def test_update_baseline_arrays_insert_defaults_to_zero(self):
        """Test that missing values default to 0.0."""
        baseline = {
            'v': np.array([1.0, 2.0]),
            'r': np.array([3.0, 4.0])
        }
        
        # Don't provide values
        update_baseline_arrays(baseline, 'insert', 0, None)
        
        assert baseline['v'][0] == 0.0
        assert baseline['r'][0] == 0.0
    
    def test_update_baseline_arrays_delete(self):
        """Test deleting values from baseline arrays."""
        baseline = {
            'v': np.array([1.0, 2.0, 3.0]),
            'r': np.array([4.0, 5.0, 6.0]),
            'f': np.array([7.0, 8.0, 9.0]),
            'a': np.array([10.0, 11.0, 12.0]),
            'S': np.array([13.0, 14.0, 15.0])
        }
        
        update_baseline_arrays(baseline, 'delete', 1)
        
        # Check that middle element was removed
        assert len(baseline['v']) == 2
        assert baseline['v'][0] == 1.0
        assert baseline['v'][1] == 3.0  # 2.0 was removed
        
        assert baseline['r'][1] == 6.0  # 5.0 was removed
        assert baseline['S'][1] == 15.0  # 14.0 was removed
    
    def test_update_baseline_arrays_ignores_missing_keys(self):
        """Test that missing keys in dict are skipped."""
        baseline = {
            'v': np.array([1.0, 2.0])
        }
        
        # Should not error even though other primitives missing
        update_baseline_arrays(baseline, 'insert', 0, {'v': 0.5})
        
        assert baseline['v'][0] == 0.5
