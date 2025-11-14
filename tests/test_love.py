# tests/test_love.py
import numpy as np
from core.love import gamma_self, love, DEFAULT_GAMMA


def _assert_close(c1, c2, tol=1e-12):
    assert abs(c1 - c2) < tol


def test_gamma_self_axes():
    assert gamma_self(we_ego_state=-2.0, love_enmity_state=0.0).real == -2.0
    assert gamma_self(we_ego_state=1.0, love_enmity_state=0.0).real == 1.0
    assert gamma_self(we_ego_state=0.0, love_enmity_state=3.0).imag == 3.0
    assert gamma_self(we_ego_state=0.0, love_enmity_state=-2.0).imag == -2.0


def test_love_at_pure_love():
    g = gamma_self(we_ego_state=0.0, love_enmity_state=4.0)
    L = love(W=1.0, gamma_history=[g], tw=0, t=0.0)
    expected_angle = 4.0 % (2 * np.pi)
    if expected_angle > np.pi:
        expected_angle -= 2 * np.pi
    _assert_close(abs(L), 1.0)
    _assert_close(np.angle(L), expected_angle)


def test_love_at_surrender():
    g = gamma_self(we_ego_state=2.0, love_enmity_state=0.0)
    L = love(W=1.0, gamma_history=[g], tw=0, t=0.0)
    expected = np.exp(2.0)
    _assert_close(L, expected)


def test_love_two_people_independent():
    g_alice = gamma_self(we_ego_state=2.0, love_enmity_state=3.0)
    L_alice = love(W=1.0, gamma_history=[g_alice], tw=0, t=0.0)
    
    g_bob = gamma_self(we_ego_state=-1.0, love_enmity_state=2.0)
    L_bob = love(W=1.0, gamma_history=[g_bob], tw=0, t=0.0)
    
    assert abs(L_alice) > 1.0
    assert abs(L_bob) < 1.0
    assert abs(np.angle(L_alice) - 3.0) < 1e-12
    assert abs(np.angle(L_bob) - 2.0) < 1e-12


def test_love_entropy_decay():
    g = gamma_self(we_ego_state=1.0, love_enmity_state=0.0)
    L0 = love(W=1.0, gamma_history=[g], tw=0, t=0.0)
    L1 = love(W=1.0, gamma_history=[g], tw=0, t=365, delta_S=0.001)
    assert abs(L1) < abs(L0) * 0.7


def test_buddhist_stillness():
    L = love(W=1.0, gamma_history=[DEFAULT_GAMMA], tw=0, t=0.0)
    _assert_close(L, 1.0 + 0j)


def test_love_wrap_continuity():
    """
    Test that love_enmity_state wraps continuously around ±π.
    No jumps — smooth rotation.
    """
    g1 = gamma_self(we_ego_state=0.0, love_enmity_state=3.0)
    g2 = gamma_self(we_ego_state=0.0, love_enmity_state=2*np.pi)      # EXACT 2π
    g3 = gamma_self(we_ego_state=0.0, love_enmity_state=2*np.pi + 0.017)

    L1 = love(W=1.0, gamma_history=[g1], tw=0, t=0.0)
    L2 = love(W=1.0, gamma_history=[g2], tw=0, t=0.0)
    L3 = love(W=1.0, gamma_history=[g3], tw=0, t=0.0)

    assert abs(np.angle(L1) - 3.0) < 1e-12
    assert abs(np.angle(L2) - 0.0) < 1e-12
    assert abs(np.angle(L3) - 0.017) < 1e-12

    assert abs(abs(L1) - 1.0) < 1e-12
    assert abs(abs(L2) - 1.0) < 1e-12
    assert abs(abs(L3) - 1.0) < 1e-12


def run_all():
    tests = [
        test_gamma_self_axes,
        test_love_at_pure_love,
        test_love_at_surrender,
        test_love_two_people_independent,
        test_love_entropy_decay,
        test_buddhist_stillness,
        test_love_wrap_continuity,
    ]
    for t in tests:
        t()
    print("All 7 tests PASSED")


if __name__ == "__main__":
    run_all()