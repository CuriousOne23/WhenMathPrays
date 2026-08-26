"""Slide 01 helper: six geometry IDs -> structural_key. No meaning floats."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.hash_toy import toy_structural_key


def make_structural_key(field, role, obj, gradient, universe, subfield) -> str:
    return toy_structural_key((field, role, obj, gradient, universe, subfield))
