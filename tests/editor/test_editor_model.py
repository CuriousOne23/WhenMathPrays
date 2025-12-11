# tests/editor/test_editor_model.py
"""
Unit tests for the editor model.
"""

import pytest
import tempfile
import os
from pathlib import Path
from tools.editor.model import EditorModel


class TestEditorModelBasics:
    """Test basic model operations."""
    
    def test_model_initialization(self):
        """Test that model initializes correctly."""
        model = EditorModel()
        
        assert model.events_m1 == []
        assert model.events_m2 == []
        assert model.marker_positions == {}
        assert model.modified_primitives == {}
        assert model.gamma_self_0 is not None
    
    def test_get_events_returns_correct_perspective(self):
        """Test that get_events returns correct event list."""
        model = EditorModel()
        model.events_m1 = ['event1', 'event2']
        model.events_m2 = ['event3', 'event4']
        
        assert model.get_events('M1') == model.events_m1
        assert model.get_events('M2') == model.events_m2


class TestEditorModelCSVLoading:
    """Test CSV loading functionality."""
    
    def test_load_csv_with_valid_file(self):
        """Test loading a valid CSV file."""
        # Create temporary CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            f.write('day,v,r,f,a,S,notes\n')
            f.write('0,5,0,2,2,0,Initial condition\n')
            f.write('7,5,2,2,3,1,First date\n')
            csv_path = f.name
        
        try:
            model = EditorModel()
            model.load_csv(csv_path, perspective='M1')
            
            # Check that events were loaded
            assert len(model.events_m1) == 2
            assert model.events_m1[0].time == 0.0
            assert model.events_m1[1].time == 7.0
            
            # Check primitive values
            assert model.events_m1[0].markers['v'].value == 5.0
            assert model.events_m1[0].markers['r'].value == 0.0
            assert model.events_m1[1].markers['S'].value == 1.0
        finally:
            os.unlink(csv_path)
    
    def test_load_csv_partner_perspective(self):
        """Test loading CSV into partner perspective."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            f.write('day,v,r,f,a,S,notes\n')
            f.write('0,3,1,1,1,0,Partner initial\n')
            csv_path = f.name
        
        try:
            model = EditorModel()
            model.load_csv(csv_path, perspective='M2')
            
            assert len(model.events_m2) == 1
            assert len(model.events_m1) == 0
            assert model.events_m2[0].markers['v'].value == 3.0
        finally:
            os.unlink(csv_path)


class TestEditorModelModifiedTracking:
    """Test modified marker tracking."""
    
    def test_is_modified_returns_false_initially(self):
        """Test that markers are not modified initially."""
        model = EditorModel()
        
        # Create simple CSV and load it
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            f.write('day,v,r,f,a,S\n')
            f.write('0,0,0,0,0,0\n')
            csv_path = f.name
        
        try:
            model.load_csv(csv_path, perspective='M1')
            
            # Check is_modified (note: uses 'M1' perspective for now)
            assert not model.is_modified(0, 'v', 'M1')
            assert not model.is_modified(0, 'r', 'M1')
        finally:
            os.unlink(csv_path)
    
    def test_is_modified_returns_true_after_marking(self):
        """Test that modified markers are detected."""
        model = EditorModel()
        
        # Create and load CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            f.write('day,v,r,f,a,S\n')
            f.write('10,0,0,0,0,0\n')
            csv_path = f.name
        
        try:
            model.load_csv(csv_path, perspective='M1')
            
            # Mark as modified
            model.modified_primitives[10.0] = {'v', 'r'}
            
            assert model.is_modified(0, 'v', 'M1')
            assert model.is_modified(0, 'r', 'M1')
            assert not model.is_modified(0, 'f', 'M1')
        finally:
            os.unlink(csv_path)
    
    def test_is_modified_handles_out_of_range_index(self):
        """Test that out of range indices return False."""
        model = EditorModel()
        
        # No events
        assert not model.is_modified(0, 'v', 'M1')
        assert not model.is_modified(99, 'r', 'M1')


class TestEditorModelSave:
    """Test CSV saving functionality."""
    
    def test_save_csv_creates_file(self):
        """Test that save_csv creates a valid CSV file."""
        model = EditorModel()
        
        # Load a simple scenario first
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            f.write('day,v,r,f,a,S\n')
            f.write('0,5,2,2,2,2\n')
            f.write('7,5,2,2,2,2\n')
            csv_path_in = f.name
        
        try:
            model.load_csv(csv_path_in, perspective='M1')
            
            # Save to new temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
                csv_path_out = f.name
            
            try:
                model.save_csv(csv_path_out, perspective='M1')
                
                # Verify file exists and has content
                assert os.path.exists(csv_path_out)
                
                with open(csv_path_out, 'r') as f:
                    lines = f.readlines()
                    # Skip metadata lines and find actual header with primitives
                    header_line = [l for l in lines if ('day' in l or 'step' in l) and 'v' in l][0]
                    assert 'v' in header_line
                    # Should have at least metadata + header + 2 events
                    data_lines = [l for l in lines if l.strip() and not l.startswith('time_unit') and not l.startswith('name') and 'day' not in l and 'step' not in l]
                    assert len(data_lines) >= 2
            finally:
                if os.path.exists(csv_path_out):
                    os.unlink(csv_path_out)
        finally:
            os.unlink(csv_path_in)
    
    def test_save_csv_preserves_values(self):
        """Test that saved CSV preserves primitive values."""
        model = EditorModel()
        
        # Create CSV with specific values
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            f.write('day,v,r,f,a,S\n')
            f.write('10,7.5,-3.2,4.8,6.1,8.9\n')
            csv_path_in = f.name
        
        try:
            model.load_csv(csv_path_in, perspective='M1')
            
            # Save and reload
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
                csv_path_out = f.name
            
            try:
                model.save_csv(csv_path_out, perspective='M1')
                
                # Load it back
                model2 = EditorModel()
                model2.load_csv(csv_path_out, perspective='M1')
                
                # Verify values match
                assert model2.events_m1[0].time == 10.0
                assert abs(model2.events_m1[0].markers['v'].value - 7.5) < 0.01
                assert abs(model2.events_m1[0].markers['r'].value - (-3.2)) < 0.01
                assert abs(model2.events_m1[0].markers['S'].value - 8.9) < 0.01
            finally:
                if os.path.exists(csv_path_out):
                    os.unlink(csv_path_out)
        finally:
            os.unlink(csv_path_in)
