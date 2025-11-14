# tests/test_love_core.py
import pytest
import numpy as np
from core.love import gamma_self, love

def test_gamma_self_pure_2d():
    g = gamma_self(1.0, 2.0)
    assert np.iscomplexobj(g)
    assert np.isclose(g.real, -1.0)
    assert np.isclose(g.imag, 2.0)

def test_gamma_self_ego_zero():
    g = gamma_self(0.0, 0.0)
    assert np.isclose(g, 0.0 + 0j)

def test_love_returns_complex():
    history = [gamma_self(1.0, 2.0)]
    L = love(W=1.0, gamma_history=history)
    assert np.iscomplexobj(L)

def test_love_memory_window():
    history = [gamma_self(i, i) for i in range(1, 10)]
    L = love(W=1.0, gamma_history=history, tw=3)
    expected_avg = np.mean(history[-3:])
    manual = 1.0 * np.exp(expected_avg)
    assert np.abs(L - manual) < 1e-10

def test_love_entropy_decay():
    history = [gamma_self(1.0, 2.0)]
    L1 = love(W=1.0, gamma_history=history, t=0)
    L2 = love(W=1.0, gamma_history=history, t=100, delta_S=0.01)
    assert np.abs(L2) < np.abs(L1)

def test_love_no_work():
    history = [gamma_self(1.0, 2.0)]
    L = love(W=0.0, gamma_history=history)
    assert np.abs(L) < 1e-15

def test_love_death_state():
    history = [
        gamma_self(1.0, 1.0),
        gamma_self(0.0, 0.0),  # death
        gamma_self(1.0, 1.0),
    ]
    with pytest.raises(ValueError, match="death state"):
        love(W=1.0, gamma_history=history)

def test_love_transition_not_death():
    history = [
        gamma_self(1.0, 1.0),
        gamma_self(1.0, 0.0),  # crosses zero
        gamma_self(1.0, -1.0),
    ]
    L = love(W=1.0, gamma_history=history)
    assert np.iscomplexobj(L)