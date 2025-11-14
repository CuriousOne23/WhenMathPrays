# tests/test_love_life.py
import pytest
import numpy as np
from core.love import gamma_self, love

def test_transition_through_zero():
    history = [
        gamma_self(1.0, 1.0),
        gamma_self(1.0, 0.0),   # crosses zero
        gamma_self(1.0, -1.0),
    ]
    L = love(W=1.0, gamma_history=history)  # allowed
    assert np.iscomplexobj(L)

def test_death_stay_at_zero():
    history = [
        gamma_self(1.0, 1.0),
        gamma_self(0.0, 0.0),   # |γ| = 0 → death
        gamma_self(1.0, 1.0),
    ]
    with pytest.raises(ValueError, match="death state"):
        love(W=1.0, gamma_history=history)

def test_gamma_self_ego_zero():
    g = gamma_self(0.0, 0.0)
    assert np.isclose(g, 0.0 + 0j)

def test_love_pure_complex():
    history = [gamma_self(1.0, 2.0)]
    L = love(W=1.0, gamma_history=history)
    assert np.iscomplexobj(L)