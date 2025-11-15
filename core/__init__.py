# core/__init__.py

from .love import gamma_self, love, DEFAULT_GAMMA
from .distributions_gamma_self import (
    DISTRIBUTIONS,
    generate_samples,
    plot_map,          # ← NEW NAME
    create_table       # ← NEW NAME
)

__all__ = [
    "gamma_self", "love", "DEFAULT_GAMMA",
    "DISTRIBUTIONS", "generate_samples",
    "plot_map", "create_table"
]