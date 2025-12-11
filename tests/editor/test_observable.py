# tests/editor/test_observable.py
"""
Unit tests for observable pattern implementation.
"""

import pytest
from tools.editor.observable import Observable, ObservableDict


class TestObservable:
    """Test basic observable pattern."""
    
    def test_add_observer(self):
        """Test adding observers."""
        obs = Observable()
        called = []
        
        def callback():
            called.append(1)
        
        obs.add_observer(callback)
        obs.notify_observers()
        
        assert len(called) == 1
    
    def test_multiple_observers(self):
        """Test multiple observers are all notified."""
        obs = Observable()
        calls = []
        
        def callback1():
            calls.append('A')
        
        def callback2():
            calls.append('B')
        
        obs.add_observer(callback1)
        obs.add_observer(callback2)
        obs.notify_observers()
        
        assert len(calls) == 2
        assert 'A' in calls
        assert 'B' in calls
    
    def test_remove_observer(self):
        """Test removing observers."""
        obs = Observable()
        called = []
        
        def callback():
            called.append(1)
        
        obs.add_observer(callback)
        obs.remove_observer(callback)
        obs.notify_observers()
        
        assert len(called) == 0
    
    def test_notify_with_arguments(self):
        """Test passing arguments to observers."""
        obs = Observable()
        received = []
        
        def callback(*args, **kwargs):
            received.append((args, kwargs))
        
        obs.add_observer(callback)
        obs.notify_observers('test', 123, key='value')
        
        assert len(received) == 1
        assert received[0] == (('test', 123), {'key': 'value'})


class TestObservableDict:
    """Test observable dictionary."""
    
    def test_setitem_notifies(self):
        """Test that setting items notifies observers."""
        obs_dict = ObservableDict()
        notifications = []
        
        def callback(*args, **kwargs):
            notifications.append(('setitem', args, kwargs))
        
        obs_dict.add_observer(callback)
        obs_dict['key'] = 'value'
        
        assert len(notifications) == 1
        assert notifications[0][0] == 'setitem'
        assert 'setitem' in notifications[0][1]
    
    def test_delitem_notifies(self):
        """Test that deleting items notifies observers."""
        obs_dict = ObservableDict({'key': 'value'})
        notifications = []
        
        def callback(*args, **kwargs):
            notifications.append(('delitem', args, kwargs))
        
        obs_dict.add_observer(callback)
        del obs_dict['key']
        
        assert len(notifications) == 1
        assert notifications[0][0] == 'delitem'
        assert 'delitem' in notifications[0][1]
    
    def test_clear_notifies(self):
        """Test that clear notifies observers."""
        obs_dict = ObservableDict({'a': 1, 'b': 2})
        notifications = []
        
        def callback(*args, **kwargs):
            notifications.append(('clear', args, kwargs))
        
        obs_dict.add_observer(callback)
        obs_dict.clear()
        
        assert len(notifications) == 1
        assert notifications[0][0] == 'clear'
    
    def test_pop_notifies(self):
        """Test that pop notifies observers."""
        obs_dict = ObservableDict({'key': 'value'})
        notifications = []
        
        def callback(*args, **kwargs):
            notifications.append(args)
        
        obs_dict.add_observer(callback)
        result = obs_dict.pop('key')
        
        assert result == 'value'
        assert len(notifications) == 1
        assert 'delitem' in notifications[0]
    
    def test_update_notifies(self):
        """Test that update notifies observers."""
        obs_dict = ObservableDict()
        notifications = []
        
        def callback(*args, **kwargs):
            notifications.append(('update', args, kwargs))
        
        obs_dict.add_observer(callback)
        obs_dict.update({'a': 1, 'b': 2})
        
        assert len(notifications) == 1
        assert notifications[0][0] == 'update'
    
    def test_observable_dict_maintains_dict_behavior(self):
        """Test that ObservableDict still works as a normal dict."""
        obs_dict = ObservableDict({'a': 1, 'b': 2})
        
        assert obs_dict['a'] == 1
        assert obs_dict['b'] == 2
        assert len(obs_dict) == 2
        assert 'a' in obs_dict
        
        obs_dict['c'] = 3
        assert obs_dict['c'] == 3
        assert len(obs_dict) == 3
    
    def test_multiple_modifications_multiple_notifications(self):
        """Test that each modification triggers notification."""
        obs_dict = ObservableDict()
        count = [0]
        
        def callback(*args, **kwargs):
            count[0] += 1
        
        obs_dict.add_observer(callback)
        
        obs_dict['a'] = 1
        obs_dict['b'] = 2
        obs_dict['c'] = 3
        
        assert count[0] == 3
        assert len(obs_dict) == 3
