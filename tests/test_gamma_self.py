# tests/test_gamma_self.py
import numpy as np
import pytest
from numpy.testing import assert_array_equal, assert_allclose

from core.gamma_self import gamma_self
from core.love import love


@pytest.fixture
def time_array():
    dt = 0.1
    t = np.arange(0, 10.0, dt)
    return t, dt

@pytest.fixture
def stable_gamma(time_array):
    t, _ = time_array
    return gamma_self(t, b=0.0, A=0.5)


def test_gamma_self_returns_complex_array(time_array):
    t, _ = time_array
    gamma = gamma_self(t)
    assert gamma.dtype == np.complex128
    assert gamma.shape == t.shape


def test_gamma_self_is_deterministic(time_array):
    t, _ = time_array
    g1 = gamma_self(t, b=0.5, A=1.0)
    g2 = gamma_self(t, b=0.5, A=1.0)
    assert_array_equal(g1, g2)


def test_gamma_self_stability_bounds(stable_gamma):
    mag = np.abs(stable_gamma)
    arg = np.angle(stable_gamma)
    assert np.all(mag < 0.8)
    assert np.all(np.abs(arg - np.pi/2) < 0.8)


def test_gamma_self_extreme_ego_collapse(time_array):
    t, _ = time_array
    gamma = gamma_self(t, b=0.0, A=100.0)
    mag = np.abs(gamma)
    assert np.any(mag > 50)


def test_gamma_self_pure_resonance(time_array):
    t, _ = time_array
    gamma = gamma_self(t, b=0.0, A=0.0, C=1.0)
    assert np.allclose(gamma.real, 0.0, atol=1e-12)
    assert not np.allclose(gamma.imag, 0.0)


# Replace the entire function
def test_love_increases_with_gamma_oscillation(time_array):
    t, dt = time_array
    vis_t = np.ones_like(t) * 0.8
    res_t = np.ones_like(t) * 0.7
    delta_S_t = np.ones_like(t) * 0.02

    # Flat
    gamma_flat = gamma_self(t, A=0.0, C=0.0, b=0.5)
    shared_growth_flat = np.ones_like(t) * 0.5
    love_flat = love(vis_t, res_t, 0.9, 0.6, shared_growth_flat, gamma_flat, delta_S_t, dt, True)

    # Oscillating
    gamma_osc = gamma_self(t, A=0.5, b=0.5)
    shared_growth_osc = 0.5 + 0.5 * np.abs(np.imag(gamma_osc))
    love_osc = love(vis_t, res_t, 0.9, 0.6, shared_growth_osc, gamma_osc, delta_S_t, dt, True)

    assert love_osc > love_flat * 1.2


def test_love_zeros_when_soul_not_locked(time_array):
    t, dt = time_array
    gamma = gamma_self(t)
    vis_t = res_t = shared_growth_t = delta_S_t = np.ones_like(t)
    love_val = love(vis_t, res_t, 1.0, 1.0, shared_growth_t, gamma, delta_S_t, dt, False)
    assert love_val == 0.0