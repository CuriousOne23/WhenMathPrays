"""CIE modulation: M' = M + alpha * I."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.vector6 import add_scaled, from_mapping

def modulate(M, alpha, I, clip=True):
    return add_scaled(from_mapping(M), from_mapping(I), float(alpha), clip=clip)
