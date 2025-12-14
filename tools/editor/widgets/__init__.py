"""
Editor widgets package.
"""

from .gamma_self0_editor import GammaSelf0Editor
from .insertion_options import InsertionOptionsWidget
from .perspective_switcher import PerspectiveSwitcher
from .name_editor import NameEditor
from .note_editor import NoteEditor
from .entropy_attractor_editor import EntropyAttractorEditor
from .entropy_amount_editor import EntropyAmountEditor

__all__ = [
    'GammaSelf0Editor', 
    'InsertionOptionsWidget', 
    'PerspectiveSwitcher', 
    'NameEditor', 
    'NoteEditor',
    'EntropyAttractorEditor',
    'EntropyAmountEditor'
]
