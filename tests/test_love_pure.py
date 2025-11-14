# tests/test_love_pure.py
import pytest
import numpy as np
from core.love import gamma_self, love

def test_gamma_self_pure_2d():
    g = gamma_self(1.0, 2.0)
    assert np.iscomplexobj(g)
    assert np.isclose(g.real, -1.0)
    assert np.isclose(g.imag, 2.0)
    assert np.abs(g) == np.sqrt(5)

def test_gamma_self_no_death():
    with pytest.raises(ValueError):
        gamma_self(0.0, 0.0)

def test_love_pure_complex():
    history = [gamma_self(1.0, 2.0)]
    L = love(W=1.0, gamma_history=history)
    assert np.iscomplexobj(L)
    assert not np.isclose(L.imag, 0)  # 2D preserved

def test_love_entropy():
    history = [gamma_self(1.0, 2.0)]
    L1 = love(W=1.0, gamma_history=history, t=0)
    L2 = love(W=1.0, gamma_history=history, t=100)
    assert np.abs(L2) < np.abs(L1)