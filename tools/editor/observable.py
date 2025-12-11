# tools/editor/observable.py
"""
Observable pattern for automatic cache invalidation.
"""

from typing import Callable, List, Any


class Observable:
    """
    Simple observable that notifies observers when data changes.
    """
    
    def __init__(self):
        self._observers: List[Callable] = []
    
    def add_observer(self, callback: Callable) -> None:
        """
        Add an observer callback that will be called on changes.
        
        Args:
            callback: Function to call when data changes
        """
        if callback not in self._observers:
            self._observers.append(callback)
    
    def remove_observer(self, callback: Callable) -> None:
        """
        Remove an observer callback.
        
        Args:
            callback: Function to remove
        """
        if callback in self._observers:
            self._observers.remove(callback)
    
    def notify_observers(self, *args, **kwargs) -> None:
        """
        Notify all observers of a change.
        
        Args:
            *args, **kwargs: Arguments to pass to observer callbacks
        """
        for observer in self._observers:
            observer(*args, **kwargs)


class ObservableDict(dict, Observable):
    """
    Dictionary that notifies observers when items are added/removed/modified.
    """
    
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        Observable.__init__(self)
    
    def __setitem__(self, key, value):
        """Override to notify observers on item set."""
        dict.__setitem__(self, key, value)
        self.notify_observers('setitem', key, value)
    
    def __delitem__(self, key):
        """Override to notify observers on item delete."""
        dict.__delitem__(self, key)
        self.notify_observers('delitem', key)
    
    def clear(self):
        """Override to notify observers on clear."""
        dict.clear(self)
        self.notify_observers('clear')
    
    def pop(self, *args):
        """Override to notify observers on pop."""
        result = dict.pop(self, *args)
        if len(args) > 0:
            self.notify_observers('delitem', args[0])
        return result
    
    def update(self, *args, **kwargs):
        """Override to notify observers on update."""
        dict.update(self, *args, **kwargs)
        self.notify_observers('update', args, kwargs)
