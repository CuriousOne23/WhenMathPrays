# core/__init__.py

# core/__init__.py
# The core is silent. The core is pure.

from .love import gamma_self, love, DEFAULT_GAMMA
from .revenge_core import sample_N_points, pdf, MU_HIGH_R, MEMORY_THETA_DEG

__all__ = [
    "gamma_self",
    "love",
    "DEFAULT_GAMMA",
    "sample_N_points",
    "pdf",
    "MU_HIGH_R",
    "MEMORY_THETA_DEG"
]